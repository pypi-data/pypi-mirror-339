from typing import Iterable, Optional, Tuple
from warnings import warn

import h5py
import numpy as np
from astropy.table import Column, Table  # type: ignore
from mpi4py import MPI

from opencosmo.file import get_data_structure
from opencosmo.handler import InMemoryHandler
from opencosmo.spatial.tree import Tree
from opencosmo.utils import read_indices


def verify_input(comm: MPI.Comm, require: Iterable[str] = [], **kwargs) -> dict:
    """
    Verify that the input is the same on all ranks.

    If not, use the value from rank 0 if require is false,
    otherwise raise an error.
    """
    output = {}
    for key, value in kwargs.items():
        values = comm.allgather(value)

        if isinstance(value, Iterable):
            sets = [frozenset(v) for v in values]
            if len(set(sets)) > 1:
                if key in require:
                    raise ValueError(
                        f"Requested different values for {key} on different ranks."
                    )
                else:
                    warn(f"Requested different values for {key} on different ranks.")
        elif len(set(values)) > 1:
            if key in require:
                raise ValueError(
                    f"Requested different values for {key} on different ranks."
                )
            else:
                warn(f"Requested different values for {key} on different ranks.")
        output[key] = values[0]
    return output


class MPIHandler:
    """
    A handler for reading and writing data in an MPI context.
    """

    def __init__(
        self,
        file: h5py.File,
        tree: Tree,
        group_name: Optional[str] = None,
        comm=MPI.COMM_WORLD,
        rank_range: Optional[Tuple[int, int]] = None,
    ):
        self.__file = file
        self.__group_name = group_name
        if group_name is None:
            self.__group = file["data"]
        else:
            self.__group = file[f"{group_name}/data"]
        self.__columns = get_data_structure(self.__group)
        self.__comm = comm
        self.__tree = tree
        self.__elem_range = rank_range

    def elem_range(self) -> Tuple[int, int]:
        """
        The full dataset will be split into equal parts by rank.
        """
        if self.__elem_range is not None:
            return self.__elem_range
        nranks = self.__comm.Get_size()
        rank = self.__comm.Get_rank()
        n = self.__group[next(iter(self.__columns))].shape[0]

        if rank == nranks - 1:
            return (rank * (n // nranks), n)
        return (rank * (n // nranks), (rank + 1) * (n // nranks))

    def __len__(self) -> int:
        range_ = self.elem_range()
        return range_[1] - range_[0]

    def __enter__(self):
        return self

    def __exit__(self, *exec_details):
        self.__group = None
        self.__columns = None
        return self.__file.close()

    def collect(self, columns: Iterable[str], indices: np.ndarray) -> InMemoryHandler:
        # concatenate the masks from all ranks
        columns = list(columns)
        columns = verify_input(comm=self.__comm, columns=columns)["columns"]
        range_ = self.elem_range()
        rank_indices = indices + range_[0]

        all_indices = self.__comm.allgather(rank_indices)
        file_path = self.__file.filename
        all_indices = np.concatenate(all_indices)
        with h5py.File(file_path, "r") as file:
            return InMemoryHandler(
                file,
                tree=self.__tree,
                columns=columns,
                indices=all_indices,
                group_name=self.__group_name,
            )

    def write(
        self,
        file: h5py.File,
        indices: np.ndarray,
        columns: Iterable[str],
        dataset_name: Optional[str] = None,
        selected: Optional[np.ndarray] = None,
    ) -> None:
        columns = list(columns)
        input = verify_input(
            comm=self.__comm,
            columns=columns,
            dataset_name=dataset_name,
            require=["dataset_name"],
        )
        columns = input["columns"]

        rank_range = self.elem_range()
        # indices = redistribute_indices(indices, rank_range)

        rank_output_length = len(indices)

        all_output_lengths = self.__comm.allgather(rank_output_length)

        rank = self.__comm.Get_rank()

        # Determine the number of elements this rank is responsible for
        # writing
        if not rank:
            rank_start = 0
        else:
            rank_start = np.sum(all_output_lengths[:rank])

        rank_end = rank_start + rank_output_length

        full_output_length = np.sum(all_output_lengths)
        if dataset_name is None:
            group = file
        else:
            group = file.require_group(dataset_name)
        data_group = group.create_group("data")

        for column in columns:
            # This step has to be done by all ranks, per documentation
            shape: Tuple[int, ...]
            if len(self.__group[column].shape) != 1:
                shape = (full_output_length, self.__group[column].shape[1])
            else:
                shape = (full_output_length,)

            data_group.create_dataset(column, shape, dtype=self.__group[column].dtype)
            if self.__columns[column] is not None:
                data_group[column].attrs["unit"] = self.__columns[column]

        self.__comm.Barrier()

        if rank_output_length != 0:
            for column in columns:
                data = self.__group[column][rank_range[0] : rank_range[1]][()]
                data = data[indices]

                data_group[column][rank_start:rank_end] = data

        mask = np.zeros(len(self), dtype=bool)
        mask[indices] = True

        new_tree = self.__tree.apply_mask(mask, self.__comm, self.elem_range())

        new_tree.write(group)  # type: ignore

        self.__comm.Barrier()

    def get_data(
        self,
        builders: dict,
        indices: np.ndarray,
    ) -> Column | Table:
        """
        Get data from the file in the range for this rank.
        """
        builder_keys = list(builders.keys())
        if self.__group is None:
            raise ValueError("This file has already been closed")

        output = {}

        for column in builder_keys:
            col = read_indices(
                self.__group[column],
                indices,
                self.elem_range(),
            )
            output[column] = builders[column].build(col)
        if len(output) == 1:
            return next(iter(output.values()))
        return Table(output)

    def take_range(self, start: int, end: int, indices: np.ndarray) -> np.ndarray:
        if start < 0 or end > len(indices):
            raise ValueError("Requested range is not within the rank's range.")

        return indices[start:end]

    def take_indices(self, n: int, strategy: str, indices: np.ndarray) -> np.ndarray:
        """
        masks are localized to each rank. For "start" and "end" it's just a matter of
        figuring out how many elements each rank is responsible for. For "random" we
        need to be more clever.
        """

        rank_length = len(indices)
        rank_lengths = self.__comm.allgather(rank_length)

        total_length = np.sum(rank_lengths)
        if n > total_length:
            # All ranks crash
            raise ValueError(
                f"Requested {n} elements, but only {total_length} are available."
            )
            n = total_length

        if self.__comm.Get_rank() == 0:
            if strategy == "random":
                take_indices = np.random.choice(total_length, n, replace=False)
                take_indices = np.sort(take_indices)
            elif strategy == "start":
                take_indices = np.arange(n)
            elif strategy == "end":
                take_indices = np.arange(total_length - n, total_length)
            # Distribute the indices to the ranks
        else:
            take_indices = None
        take_indices = self.__comm.bcast(take_indices, root=0)

        if take_indices is None:
            # Should not happen, but this is for mypy
            raise ValueError("Indices should not be None.")

        rank_start_index = self.__comm.Get_rank()
        if rank_start_index:
            rank_start_index = np.sum(rank_lengths[: self.__comm.Get_rank()])
        rank_end_index = rank_start_index + rank_length

        rank_indicies = take_indices[
            (take_indices >= rank_start_index) & (take_indices < rank_end_index)
        ]
        if len(rank_indicies) == 0:
            # This rank doesn't have enough data
            warn(
                "This take operation will return no data for rank "
                f"{self.__comm.Get_rank()}"
            )
            return np.array([], dtype=int)

        return rank_indicies - rank_start_index
