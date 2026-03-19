import logging

from src.task import Task, StatusEnum
from src.queue import TaskQueue
from src.source import Source

from collections.abc import Sequence

logger = logging.getLogger(__name__)


class Aggregator():
    """
    Класс агрегатора. Собирает задачи из источников и обрабатывает их
    """

    def __init__(self) -> None:
        self.sources: list[Source] = []
        self.id_count = 0

    def bind_source(self, source: Source) -> None:
        """
        Добавление источника в список доступных источников.

        :param source: Источник
        """
        # проверка протокола с runtime_checkable
        if not isinstance(source, Source):
            logger.error(f"Ошибка добавления источника {source}")
            raise RuntimeError("Источник не сходится с протоколом")
        logger.info(f"Добавлен источник {source}")
        self.sources.append(source)

    def aggregate_tasks(self) -> TaskQueue:
        """
        Агрегатор задач. Запрашивает задачи из всех источников

        :return: Список задач, выданных источниками
        """
        logger.info("Запуск получения задач из источников")
        tasks = TaskQueue()
        for source in self.sources:
            for payload in source.get_tasks():
                # создание класса Task для каждой задачи
                self.id_count += 1
                task = Task(
                    id=self.id_count,
                    payload=payload,
                )
                tasks.add(task)
        logger.info(f"Сбор задач завершен. Количество задач: {len(tasks)}")
        return tasks

    def handle_tasks(self, tasks: Sequence) -> None:
        """
        Обрабатывает задачи. Работает с очередью и генераторами.

        :param tasks: Задачи, которые нужно обработать
        """
        if not tasks:
            return
        logger.info("Начало обработки задач")
        for task in tasks:
            self.handle_task(task)
        logger.info("Обработка задач окончена")

    def handle_task(self, task: Task) -> None:
        """
        Обработчик задачи. Обрабатывает статус и проверяет тип payload. Запускает .run_task()

        :param task: Задача, которую нужно обработать
        """
        if task.status != StatusEnum.NOT_STARTED:
            raise ValueError("Нельзя обработать задачу, которая уже начата или завершена")

        task.status = StatusEnum.PROCESSING

        # проверка payload
        if not isinstance(task.payload, str):
            task.status = StatusEnum.CANCELLED
            raise RuntimeError("payload неподходящего типа")
        self.handle_task_payload(task)

        task.status = StatusEnum.COMPLETED

    def handle_task_payload(self, task: Task) -> None:
        """
        Запуск задачи. Для примера просто печатает payload

        :param task: Задача
        """
        print(f"Выполнена задача: {task}")
