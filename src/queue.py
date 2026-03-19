from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import overload

from src.task import Task


class TaskQueue(Sequence):
    """
    Класс очереди задач. Имплементирует ленивые фильтры по статусу и приоритету
    """

    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add(self, task: Task) -> None:
        self.tasks.append(task)

    def dequeue(self) -> Task:
        if not len(self):
            raise IndexError("Очередь пустая")
        return self.tasks.pop(0)

    def extend(self, other: object) -> None:
        if isinstance(other, TaskQueue):
            self.tasks.extend(other)
        elif isinstance(other, Iterator):
            for task in other:
                self.add(task)
        else:
            raise TypeError(f"Нельзя итерировать {other}")

    # yield реализует поддержку протокола итерации
    def __iter__(self) -> Iterator[Task]:
        for i in range(len(self)):
            yield self[i]

    @overload
    def __getitem__(self, index: int) -> Task:
        ...

    @overload
    def __getitem__(self, index: slice) -> TaskQueue:
        ...

    def __getitem__(self, index: int | slice) -> Task | TaskQueue:
        if isinstance(index, int):
            if index >= len(self) or index < -len(self):
                raise IndexError("Индекс вне предела очереди")
            return self.tasks[index]

        slice_queue = TaskQueue()

        start, stop, step = index.indices(len(self))
        for i in range(start, stop, step):
            slice_queue.add(self[i])

        return slice_queue

    def __len__(self) -> int:
        return len(self.tasks)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TaskQueue):
            raise ValueError("Можно сравнить только с TaskQueue")
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] is not other[i]:
                return False
        return True
