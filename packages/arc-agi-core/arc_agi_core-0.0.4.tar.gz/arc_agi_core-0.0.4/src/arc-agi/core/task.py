from typing import Union, List, Tuple, Optional, Dict, Literal
from pathlib import Path
import json

from .grid import Grid
from .pair import Pair
from .utils import Layout


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
