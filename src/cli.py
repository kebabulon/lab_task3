import shlex

from src.task import StatusEnum
from src.queue import TaskQueue
from src.aggregator import Aggregator
from src.source import GeneratorSource, JsonSource, ApiSource
from src.constants import DEBUG


class Cli():
    """
    Класс Cli. Позволяет интерактивно запрашивать задачи, печатать, обрабатывать и фильтровать очередь
    """

    def __init__(self):
        self.aggregator = Aggregator()

        self.aggregator.bind_source(GeneratorSource())
        self.aggregator.bind_source(JsonSource("example_tasks.json"))
        self.aggregator.bind_source(ApiSource(2))

        self.task_queue = TaskQueue()

    def cmd_help(self) -> None:
        print("--- Помощь ---")
        print("help - выводит это сообщение")
        print("aggregate - запрашивает задачи и добавляет их в очередь")
        print("print - печатает задачи в очереди")
        print("filter priority <int> - фильтрует задачи в очереде по приоритету. Пример: filter priority 0")
        print("filter status <str> - фильтрует задачи в очереде по статусу. Пример: filter status 'Not started'")
        print("run - запускает обработчик задач для не начатых задач в очереди")
        print("clear - чистит очередь")
        print("--------------")

    def cmd_filter_priority(self, priority: int) -> None:
        filtered_queue = TaskQueue()
        filtered_queue.extend(self.task_queue.filter(priority=priority))
        self.task_queue = filtered_queue

    def cmd_filter_status(self, status: StatusEnum) -> None:
        filtered_queue = TaskQueue()
        filtered_queue.extend(self.task_queue.filter(status=status))
        self.task_queue = filtered_queue

    def execute(self, cmd: str) -> None:
        """
        Запускает команду

        :param cmd: Команда и агрументы к ней
        """
        args = shlex.split(cmd)

        if not args:
            return

        match args[0]:
            case 'help':
                self.cmd_help()
            case 'aggregate':
                self.task_queue.extend(self.aggregator.aggregate_tasks())
            case 'print':
                for task in self.task_queue:
                    print(task)
            case 'filter':
                if len(args) < 3:
                    print('Недостаточно агрументов для сортировки')
                    return
                match args[1]:
                    case 'priority':
                        self.cmd_filter_priority(int(args[2]))
                    case 'status':
                        self.cmd_filter_status(StatusEnum(args[2]))
                    case _:
                        print('Нету такого фильтра')
            case 'run':
                self.aggregator.handle_tasks(self.task_queue.filter(status=StatusEnum.NOT_STARTED))
            case 'clear':
                self.task_queue.clear()
            case _:
                print("Неизвестная команда")

    def run(self) -> None:
        """
        Запуск CLI
        """

        print("--- Для помощи введите команду > help ---")

        try:
            while True:
                cmd = input(" > ")

                if cmd == "exit":
                    break

                try:
                    self.execute(cmd)
                except Exception as e:
                    if DEBUG:
                        raise e
                    print(f"Error: {str(e)}")
                except KeyboardInterrupt:
                    continue
        except KeyboardInterrupt:
            print()
