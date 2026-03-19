from typing import Protocol, runtime_checkable

from random import randint
from pathlib import Path
import json
from time import sleep


@runtime_checkable
class Source(Protocol):
    """
    Протокол источника
    """

    def get_tasks(self) -> list:
        """
        Метод, который возращает описание задач

        :return: Список описаний задач
        """
        ...


class GeneratorSource():
    """
    Источник задач. Генератор
    """

    def __init__(self):
        self.count = 0

    def get_tasks(self) -> list:
        self.count += 1

        return [
            f"generated payload {randint(1, 10)}"
        ]


class JsonSource():
    """
    Источник задач. Из Json файла
    """

    def __init__(self, file: str):
        self.file = Path(file)
        if not self.file.exists():
            raise NameError("Файл не существует")

    def get_tasks(self) -> list:
        with open(self.file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Не получилось загрузить Json: {e}")

        return [task["payload"] for task in data]


class ApiSource():
    """
    Источник задач. Api заглушка
    """

    def __init__(self, fake_requests: int):
        self.count = 0
        self.fake_requests = fake_requests

    def get_tasks(self) -> list:
        tasks: list = []
        for i in range(self.fake_requests):
            self.count += 1
            sleep(randint(1, 3))
            tasks.append(
                f"api payload #{i}"
            )
        return tasks
