import pytest

from src.task import Task, StatusEnum
from src.queue import TaskQueue
from src.aggregator import Aggregator


def test_queue():
    queue = TaskQueue()
    assert len(queue) == 0
    test_task = Task(
        id=1,
        payload="test payload"
    )
    test_task_2 = Task(
        id=2,
        payload="test payload 2"
    )
    test_task_3 = Task(
        id=3,
        payload="test payload 3"
    )

    queue.add(test_task)
    assert len(queue) == 1
    assert queue[0] == test_task
    assert queue[-1] == test_task
    assert queue.dequeue() == test_task
    assert len(queue) == 0

    with pytest.raises(IndexError):
        _ = queue[5]
    with pytest.raises(IndexError):
        _ = queue[-5]

    queue.add(test_task)
    queue.add(test_task_2)
    assert queue.dequeue() == test_task
    assert queue.dequeue() == test_task_2
    with pytest.raises(IndexError):
        queue.dequeue()

    queue.add(test_task)
    queue.extend([test_task_2, test_task_3])
    assert queue[-1] == test_task_3
    queue.clear()
    assert len(queue) == 0


def test_filter():
    queue = TaskQueue()
    test_task = Task(
        id=1,
        payload="test payload",
        priority=2
    )
    test_task_2 = Task(
        id=2,
        payload="test payload 2",
        priority=1
    )
    test_task_3 = Task(
        id=3,
        payload="test payload 3",
        priority=1
    )
    queue += [test_task, test_task_2, test_task_3]
    filtered_queue = TaskQueue()
    filtered_queue.extend(queue.filter(priority=1))
    queue.dequeue()
    assert queue == filtered_queue
    filtered_queue.clear()
    filtered_queue.extend(queue.filter(priority=10))
    assert len(filtered_queue) == 0

    aggregator = Aggregator()
    aggregator.handle_task(test_task_2)
    filtered_queue.clear()
    filter_generator = queue.filter(StatusEnum.COMPLETED)
    assert next(filter_generator) == test_task_2
    with pytest.raises(StopIteration):
        next(filter_generator)
