from src.cli import Cli


def test_cli():
    cli = Cli()

    cli.execute("help")
    cli.execute("aggregate")
    assert len(cli.task_queue) > 0
    cli.execute("print")
    cli.execute("filter priority 1")
    cli.execute("run")
    cli.execute("filter status 'Completed'")
    cli.execute("clear")
    assert len(cli.task_queue) == 0
