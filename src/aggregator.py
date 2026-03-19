import logging

from src.task import Task, StatusEnum
from src.source import Source

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

    def run(self) -> None:
        """
        Запуск агрегатора. Агрегирует задачи и обрабатывает их

        :return: Список задач, выданных источниками
        """
        tasks: list[Task] = self.aggregate_tasks()
        logger.info("Начало обработки задач")
        for task in tasks:
            self.handle_task(task)
        logger.info("Обработка задач окончена")

    def aggregate_tasks(self) -> list[Task]:
        """
        Агрегатор задач. Запрашивает задачи из всех источников

        :return: Список задач, выданных источниками
        """
        logger.info("Запуск получения задач из источников")
        tasks: list[Task] = []
        for source in self.sources:
            for payload in source.get_tasks():
                # создание класса Task для каждой задачи
                self.id_count += 1
                task = Task(
                    id=self.id_count,
                    payload=payload,
                )
                tasks.append(task)
        logger.info(f"Сбор задач завершен. Количество задач: {len(tasks)}")
        return tasks

    def handle_task(self, task: Task) -> None:
        """
        Обработчик задачи. Печатает payload задачи

        :param task: Задача
        """
        if task.status != StatusEnum.NOT_STARTED:
            raise ValueError("Нельзя обработать задачу, которая уже начата или завершена")

        task.status = StatusEnum.PROCESSING
        # проверка payload
        if not isinstance(task.payload, str):
            task.status = StatusEnum.CANCELLED
            raise RuntimeError("payload неподходящего типа")
        print(task)
        task.status = StatusEnum.COMPLETED
