from datetime import datetime
from enum import Enum
from src.constants import DEFAULT_PRIORITY


class StatusEnum(Enum):
    NOT_STARTED = "Not started"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Task():
    """
    Класс задачи
    """

    def __init__(self,
                 id: int,
                 payload: object,
                 priority: int = DEFAULT_PRIORITY,
                 ) -> None:
        if id < 0:
            raise ValueError("id не может быть отрицательным")
        self._id = id
        self._payload = payload
        if priority < 0:
            raise ValueError("Приоритет не может быть отрицательным")
        self._priority = priority
        self._status: StatusEnum = StatusEnum.NOT_STARTED
        self._time_created: datetime = datetime.now()

    def __str__(self):
        return f"Task(id='{self.format_id(self.id)}', payload={repr(self.payload)}, priority={self.priority}, status={repr(self.status.value)}, time_created='{str(self.time_created)}')"

    @staticmethod
    def format_id(id: int) -> str:
        return f"task_{id}"

    # id является примером non-data descriptor
    # имеет только __get__
    @property
    def id(self) -> int:
        return self._id

    # payload является примером non-data descriptor
    # имеет только __get__
    @property
    def payload(self) -> object:
        return self._payload

    # priority является примером data descriptor
    # имеет __get__ и __set__
    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, value: int) -> None:
        if value < 0:
            raise ValueError("Приоритет не может быть отрицательным")
        self._priority = value

    # time_created является примером non-data descriptor
    # имеет только __get__
    @property
    def time_created(self) -> datetime:
        return self._time_created

    # status является примером data descriptor
    # имеет __get__ и __set__
    @property
    def status(self) -> StatusEnum:
        return self._status

    @status.setter
    def status(self, value: StatusEnum) -> None:
        if self._status != StatusEnum.NOT_STARTED and value == StatusEnum.NOT_STARTED:
            raise ValueError(f"Нельзя поменять статус {self._status} на {StatusEnum.NOT_STARTED}")
        if self._status in [StatusEnum.CANCELLED, StatusEnum.COMPLETED]:
            raise ValueError(f"Нельзя менять статус {self._status}")
        self._status = value
