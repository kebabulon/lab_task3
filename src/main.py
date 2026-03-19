import logging

from src.aggregator import Aggregator
from src.source import GeneratorSource, JsonSource, ApiSource


def main() -> None:
    """
    Запуск аггрегатора, который запрашивает и выполняет задачи
    """
    logging.basicConfig(
        filename='aggregator.log',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    aggregator = Aggregator()
    aggregator.bind_source(GeneratorSource())
    aggregator.bind_source(JsonSource("example_tasks.json"))
    aggregator.bind_source(ApiSource(3))
    aggregator.run()


if __name__ == "__main__":
    main()
