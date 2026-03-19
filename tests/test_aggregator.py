import pytest

from src.aggregator import Aggregator
from src.source import GeneratorSource
from src.task import Task, StatusEnum
from src.constants import DEFAULT_PRIORITY


def test_aggregator():
    aggregator = Aggregator()
    aggregator.bind_source(GeneratorSource())
    tasks = aggregator.aggregate_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1
    assert tasks[0].status == StatusEnum.NOT_STARTED
    assert tasks[0].priority == DEFAULT_PRIORITY
    aggregator.run()


def test_empty_aggregator():
    aggregator = Aggregator()
    aggregator.run()


def test_incorrect_payload():
    aggregator = Aggregator()
    incorrect_payload_task = Task(
        id=1,
        payload=67
    )
    with pytest.raises(RuntimeError):
        aggregator.handle_task(incorrect_payload_task)
    assert incorrect_payload_task.status == StatusEnum.CANCELLED


def test_incorrect_status():
    aggregator = Aggregator()
    incorrect_status_task = Task(
        id=1,
        payload="test payload"
    )
    aggregator.handle_task(incorrect_status_task)
    assert incorrect_status_task.status == StatusEnum.COMPLETED
    with pytest.raises(ValueError):
        aggregator.handle_task(incorrect_status_task)
