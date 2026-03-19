import pytest

from src.task import Task, StatusEnum
from datetime import datetime


def test_task():
    # priority
    with pytest.raises(ValueError):
        _ = Task(
            id=1,
            payload="test",
            priority=-1
        )
    # id
    with pytest.raises(ValueError):
        _ = Task(
            id=-1,
            payload="test",
        )
    task = Task(
        id=1,
        payload="test",
    )
    task.priority = 5
    with pytest.raises(ValueError):
        task.priority = -1

    # non-data descriptor
    with pytest.raises(AttributeError):
        task.time_created = datetime.now()
    with pytest.raises(AttributeError):
        task.id = 10
    with pytest.raises(AttributeError):
        task.payload = "test payload"

    # status
    task.status = StatusEnum.PROCESSING
    with pytest.raises(ValueError):
        task.status = StatusEnum.NOT_STARTED
    task.status = StatusEnum.COMPLETED
    with pytest.raises(ValueError):
        task.status = StatusEnum.PROCESSING
