import logging

from src.cli import Cli


def main() -> None:
    """
    Запуск Cli
    """
    logging.basicConfig(
        filename='lab_task.log',
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    cli = Cli()
    cli.run()


if __name__ == "__main__":
    main()
