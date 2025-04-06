from enum import Enum
from typing import Dict, Union, List, Self, Tuple, Optional, Literal, Any
import numpy as np
from pathlib import Path
import json
import warnings
import re
import os
import requests
import zipfile
import io


class COLOR(Enum):
    ZERO = 0  # Background
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9


PALETTE: Dict[COLOR, str] = {
    COLOR.ZERO: "\033[48;5;0m  \033[0m",
    COLOR.ONE: "\033[48;5;20m  \033[0m",
    COLOR.TWO: "\033[48;5;124m  \033[0m",
    COLOR.THREE: "\033[48;5;10m  \033[0m",
    COLOR.FOUR: "\033[48;5;11m  \033[0m",
    COLOR.FIVE: "\033[48;5;7m  \033[0m",
    COLOR.SIX: "\033[48;5;5m  \033[0m",
    COLOR.SEVEN: "\033[48;5;208m  \033[0m",
    COLOR.EIGHT: "\033[48;5;14m  \033[0m",
    COLOR.NINE: "\033[48;5;1m  \033[0m",
}

ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(text: str) -> str:
    """Removes ANSI escape codes from the string for correct width calculation."""
    return ANSI_ESCAPE_PATTERN.sub("", text)


def ansi_width(text: str) -> int:
    """Returns the width of text after removing ANSI escape sequences."""
    return len(strip_ansi(text))


def align_lines(
    lines: List[str],
    target_width: int,
    align: Literal["start", "center", "end"],
) -> List[str]:
    """Aligns lines while preserving ANSI codes."""
    if align == "start":
        return [
            line + " " * (max(target_width - ansi_width(line), 0)) for line in lines
        ]
    elif align == "center":
        return [
            " " * (max(target_width - ansi_width(line), 0) // 2)
            + line
            + " " * ((max(target_width - ansi_width(line), 0) + 1) // 2)
            for line in lines
        ]
    elif align == "end":
        return [" " * max(target_width - ansi_width(line), 0) + line for line in lines]


class Layout:
    def __init__(
        self,
        *elements: Any,
        direction: Literal["horizontal", "vertical"] = "horizontal",
        align: Literal["start", "center", "end"] = "start",
        show_divider: bool = False,
        min_width: int = 0,
    ):
        self.elements = elements
        self.direction = direction
        self.align = align
        self.show_divider = show_divider
        self.min_width = min_width

    @property
    def width(self):
        return max(ansi_width(line) for line in repr(self).splitlines())

    @property
    def height(self):
        return len(repr(self).splitlines())

    def __repr__(self) -> str:
        elements = [
            (element if isinstance(element, str) else repr(element)).splitlines()
            for element in self.elements
        ]

        if self.direction == "horizontal":
            max_height = max(len(element) for element in elements)
            normalized_elements = [
                element + [""] * (max_height - len(element)) for element in elements
            ]
            widths = [max(ansi_width(line) for line in element) for element in elements]
            aligned_elements = [
                align_lines(element, width, self.align)
                for element, width in zip(normalized_elements, widths)
            ]
            divider = " | " if self.show_divider else ""
            return "\n".join(
                align_lines(
                    [
                        divider.join(
                            aligned_elements[col][row]
                            for col in range(len(aligned_elements))
                        )
                        for row in range(max_height)
                    ],
                    self.min_width,
                    self.align,
                )
            )

        elif self.direction == "vertical":
            max_width = max(
                max(ansi_width(line) for line in element) for element in elements
            )
            aligned_elements = [
                align_lines(element, max_width, self.align) for element in elements
            ]
            divider = "\n" + "-" * max_width if self.show_divider else ""
            return f"{divider}\n".join(
                "\n".join(element) for element in aligned_elements
            )

    def __str__(self) -> str:
        elements = [str(element).splitlines() for element in self.elements]

        if self.direction == "horizontal":
            max_height = max(len(element) for element in elements)
            normalized_elements = [
                element + [""] * (max_height - len(element)) for element in elements
            ]
            widths = [max(ansi_width(line) for line in element) for element in elements]
            aligned_elements = [
                align_lines(element, width, self.align)
                for element, width in zip(normalized_elements, widths)
            ]
            divider = " | " if self.show_divider else ""
            return "\n".join(
                divider.join(
                    aligned_elements[col][row] for col in range(len(aligned_elements))
                )
                for row in range(max_height)
            )

        elif self.direction == "vertical":
            max_width = max(
                max(ansi_width(line) for line in element) for element in elements
            )
            aligned_elements = [
                align_lines(element, max_width, self.align) for element in elements
            ]
            divider = "\n" + "-" * max_width if self.show_divider else ""
            return f"{divider}\n".join(
                "\n".join(element) for element in aligned_elements
            )


def download_from_github(
    repo_owner, repo_name, path, branch="main", destination="./downloaded"
):
    """
    Downloads and extracts a specific path from a GitHub repository.

    :param repo_owner: GitHub username or organization.
    :param repo_name: Repository name.
    :param path: Path to the folder inside the repo to extract.
    :param branch: Repo branch (default: "main").
    :param destination: Local destination folder for saving files.
    """
    url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/{branch}.zip"
    print(f"Downloading from {url}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            repo_folder = f"{repo_name}-{branch}/"
            target_folder = f"{repo_folder}{path}/"

            extracted_files = 0

            for file in zip_file.namelist():
                if file.startswith(target_folder) and not file.endswith("/"):
                    relative_path = file[len(target_folder) :]
                    save_path = os.path.join(destination, relative_path)

                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    with zip_file.open(file) as source, open(save_path, "wb") as target:
                        target.write(source.read())

                    extracted_files += 1

            if extracted_files > 0:
                print(
                    f"✅ Successfully downloaded '{path}' from {repo_owner}/{repo_name} into '{destination}'."
                )
            else:
                print(
                    f"⚠️ No files extracted. Check if the path '{path}' exists in the repository."
                )

    else:
        print(f"❌ Failed to download: HTTP {response.status_code}")


class Grid:
    PALETTE = PALETTE

    @classmethod
    def show_palette(cls):
        """Prints the color palette."""
        print(
            " | ".join(
                f"{color}={symbol.value}" for symbol, color in cls.PALETTE.items()
            )
        )

    def __init__(self, array: Union[List[List[int]], np.ndarray, None] = None) -> None:
        """
        Initializes the `Grid` with a 2D array of integers.

        Args:
            array (Union[List[List[int]], np.ndarray, None]): A 2D list of int or numpy ndarray representing the grid.
            If None, a default 1x1 `Grid` of `COLOR.ZERO` is used.

        Raises:
            ValueError: If the input array is not a 2D list or numpy ndarray of integers.
            ValueError: If any element in the array is not a value of `COLOR` (values of `COLOR` is 0~9 integers by default if `COLOR` is not modified. )

        Returns:
            None

        """
        if not array:
            array = [[0]]

        if not isinstance(array, (np.ndarray, list)):
            raise ValueError("Input array must be a 2D list or numpy ndarray.")

        if not all(item in COLOR for row in array for item in row):
            raise ValueError("Array elements must be values of `COLOR`")

        self._array = array if isinstance(array, np.ndarray) else np.array(array)

    @classmethod
    def from_json(cls, file_path: Union[str, Path]) -> Self:
        """
        Creates a `Grid` instance from a JSON file at a given path.

        Args:
            file_path (Union[str, Path]): File path of the JSON file to be loaded.

        Raises:
            ValueError: If the string format is incorrect or if any element is not a valid `COLOR` value.

        Returns:
            Grid: A `Grid` instance created from the JSON file.
        """
        try:
            with open(file_path) as f:
                array = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format.")

        return cls(array)

    @classmethod
    def from_npy(cls, filePath: Union[str, Path]) -> Self:
        return cls(np.load(filePath))

    def save_as_json(self, path: Union[str, Path]) -> None:
        with open(path, "w") as f:
            json.dump(self.to_list(), f)

    def save_as_npy(self, path: str | Path) -> None:
        np.save(path, self.to_numpy())

    def to_list(self) -> List[List[int]]:
        return self._array.tolist()

    def to_numpy(self) -> np.ndarray:
        return self._array

    @property
    def shape(self) -> Tuple[int, int]:
        return self.to_numpy().shape

    def __repr__(self) -> str:
        return (
            "\n".join(
                "".join(self.PALETTE[COLOR(value)] for value in row)
                for row in self.to_numpy()
            )
            + "\n"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Grid):
            raise ValueError(
                "Cannot compare with non-`Grid` object. "
                "If the object is 2d list or numpy array, try converting it to `Grid` and then compare. "
            )
        return bool((self.to_numpy() == other.to_numpy()).all())

    def __sub__(self, other: object) -> int:
        """Number of different pixels"""
        if not isinstance(other, Grid):
            raise NotImplementedError(
                "Cannot compare with non-`Grid` object. "
                "If the object is 2d list or numpy array, try converting it to `Grid` and then compare. "
            )
        if self.shape != other.shape:
            raise ValueError(
                f"Connot compare `Grid`s of different shape. {self.shape} != {other.shape}"
            )
        return np.sum(self.to_numpy() != other.to_numpy())


class Pair:
    def __init__(
        self,
        input: Union[Grid, List[List[int]]],
        output: Union[Grid, List[List[int]]],
        censor: bool = False,
    ) -> None:
        self._input = input if isinstance(input, Grid) else Grid(input)
        self._output = output if isinstance(output, Grid) else Grid(output)
        self._is_censored = censor

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, grid: Union[Grid, List[List[int]]]):
        self._input = grid if isinstance(grid, Grid) else Grid(grid)
        return self._input

    @property
    def output(self):
        if self._is_censored:
            warnings.warn(
                "Access to `output` is censored. Call `.uncensor()` to gain access. ",
                UserWarning,
            )
            return None
        return self._output

    @output.setter
    def output(self, grid: Union[Grid, List[List[int]]]):
        if self._is_censored:
            warnings.warn(
                "Access to `output` is censored. Call `.uncensor()` to gain access. ",
                UserWarning,
            )
            return None
        self._output = grid if isinstance(grid, Grid) else Grid(grid)
        return self._output

    def censor(self):
        self._is_censored = True

    def uncensor(self):
        self._is_censored = False

    def __repr__(self):
        return repr(
            Layout(
                Layout(
                    "INPUT",
                    self.input,
                    direction="vertical",
                    align="center",
                ),
                "->",
                Layout(
                    "OUTPUT",
                    self.output if self.output else "*CENSORED*",
                    direction="vertical",
                    align="center",
                ),
                align="center",
            )
        )

    def to_dict(self):
        return {"input": self.input.to_list(), "output": self.output.to_list()}


class Task:
    def __init__(
        self,
        train: Union[
            List[Pair],
            List[Tuple[List[List[int]], List[List[int]]]],
            List[Tuple[Grid, Grid]],
        ],
        test: Union[
            List[Pair],
            List[Tuple[List[List[int]], List[List[int]]]],
            List[Tuple[Grid, Grid]],
        ],
        task_id: Optional[str] = None,
    ):
        self.train = [pair if isinstance(pair, Pair) else Pair(*pair) for pair in train]
        self.test = [pair if isinstance(pair, Pair) else Pair(*pair) for pair in test]
        self.task_id = task_id

    @classmethod
    def from_dict(
        cls,
        task_dict: Dict[
            Literal["train", "test"],
            List[Dict[Literal["input", "output"], List[List[int]]]],
        ],
        task_id: Optional[str] = None,
    ):
        train = [Pair(pair["input"], pair["output"]) for pair in task_dict["train"]]
        test = [Pair(pair["input"], pair["output"]) for pair in task_dict["test"]]

        return cls(train, test, task_id)

    def to_dict(self):
        return {
            "train": [pair.to_dict() for pair in self.train],
            "test": [pair.to_dict() for pair in self.test],
        }

    @classmethod
    def from_json(cls, file_path: Union[str, Path]):
        file_path = file_path if isinstance(file_path, Path) else Path(file_path)
        task_id = file_path.stem

        task = None
        try:
            with file_path.open() as f:
                task = json.load(f)
                # TODO: validate schema
        except Exception as e:
            raise RuntimeError(
                f"Failed to load and parse task json file at '{file_path}: {e}"
            )

        return cls.from_dict(task, task_id)

    @property
    def inputs(self):
        return [pair.input for pair in self.train + self.test]

    @property
    def outputs(self):
        return [pair.output for pair in self.train + self.test]

    def __repr__(self):
        train = Layout(
            *[
                Layout(
                    Layout(
                        f"INPUT {i}",
                        pair.input,
                        direction="vertical",
                        align="center",
                    ),
                    " -> ",
                    Layout(
                        f"OUTPUT {i}",
                        pair.output if pair.output else "*CENSORED*",
                        direction="vertical",
                        align="center",
                    ),
                )
                for i, pair in enumerate(self.train)
            ],
            direction="vertical",
        )
        test = Layout(
            *[
                Layout(
                    Layout(
                        f"INPUT {i}",
                        pair.input,
                        direction="vertical",
                        align="center",
                    ),
                    " -> ",
                    Layout(
                        f"OUTPUT {i}",
                        pair.output if pair.output else "*CENSORED*",
                        direction="vertical",
                        align="center",
                    ),
                )
                for i, pair in enumerate(self.test)
            ],
            direction="vertical",
        )
        width = max(train.width, test.width)
        return repr(
            Layout(
                f"< Task{' ' + self.task_id if self.task_id else ''} >".center(
                    width, "="
                ),
                " Train ".center(width, "-"),
                train,
                " Test ".center(width, "-"),
                test,
                direction="vertical",
            )
        )

    def __str__(self):
        return str(repr(self))

    def censor_outputs(self):
        for pair in self.train + self.test:
            pair.censor()

    def uncensor_outputs(self):
        for pair in self.train + self.test:
            pair.uncensor()

    def censor_test_outputs(self):
        for pair in self.test:
            pair.censor()

    def uncensor_test_outputs(self):
        for pair in self.test:
            pair.uncensor()


class ARC1:
    def __init__(
        self, dataset_path: Union[str, Path], train: bool = True, download: bool = True
    ):
        self._tasks: List[Task] = list()
        self._tasks_map: Dict[str, int] = dict()
        self._dataset_path = (
            dataset_path if isinstance(dataset_path, Path) else Path(dataset_path)
        )
        self._train = train

        if download:
            self.download()

        self.load()

    def load(self):
        if not self._dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset path '{self._dataset_path}' does not exist. "
            )
        if not self._dataset_path.is_dir():
            raise NotADirectoryError(
                f"Dataset path '{self._dataset_path}' is not a directory. "
            )

        for file_path in self._dataset_path.glob("*.json"):
            task = Task.from_json(file_path)
            self._tasks.append(task)

    def download(self):
        download_from_github(
            "fchollet",
            "ARC-AGI",
            f"data/{'training' if self._train else 'evaluation'}",
            "master",
            self._dataset_path,
        )

    def __contains__(self, task_id: str) -> bool:
        return any(task.task_id == task_id for task in self._tasks)

    def get(self, task_id: str) -> Task:
        if task_id not in self:
            raise KeyError(f"Task with task id: {task_id} is not in this dataset. ")
        return next((task for task in self._tasks if task.task_id == task_id), None)

    def __getitem__(self, i: int) -> Task:
        return self._tasks[i]

    def __len__(self) -> int:
        return len(self._tasks)


class ARC2(ARC1):
    def download(self):
        download_from_github(
            "arcprize",
            "ARC-AGI-2",
            f"data/{'training' if self._train else 'evaluation'}",
            "main",
            self._dataset_path,
        )
