from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import overload

from src.task import Task, StatusEnum


class TaskQueue(Sequence):
    """
    Класс очереди задач. Имплементирует ленивые фильтры по статусу и приоритету
    """

    def __init__(self) -> None:
        self.tasks: list[Task] = []

    def add(self, task: Task) -> None:
        """
        Добавляет задачу в очередь по принципу FIFO

        :param task: Задача
        """
        self.tasks.append(task)

    def dequeue(self) -> Task:
        """
        Убирает задачу из очереди по принципу FIFO

        :return: Задача
        """
        if not len(self):
            raise IndexError("Очередь пустая")
        return self.tasks.pop(0)

    def extend(self, other: Sequence) -> None:
        """
        Добавляет задачи из другой очереди/последовательности в начало

        :param other: Очередь или последовательность
        """
        if isinstance(other, TaskQueue):
            self.tasks.extend(other)
        else:
            for task in other:
                self.add(task)

    def filter(self, status: StatusEnum | None = None, priority: int | None = None) -> Iterator[Task]:
        """
        Фильтр по приоритету и/или по статусу

        :param task: Задача
        :return: Итератор профильтрованых задач
        """
        def filter_function(task: Task) -> bool:
            return (
                (status is None or task.status == status)
                and (priority is None or task.priority == priority)
            )
        return filter(filter_function, self)

    def clear(self) -> None:
        """
        Чистит очередь
        """
        self.tasks.clear()

    def __add__(self, other: object) -> TaskQueue:
        if not isinstance(other, Sequence):
            raise TypeError(f"Нельзя прибавить {type(other)} к очереди")
        sum_queue = TaskQueue()
        sum_queue.extend(self)
        sum_queue.extend(other)
        return sum_queue

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
