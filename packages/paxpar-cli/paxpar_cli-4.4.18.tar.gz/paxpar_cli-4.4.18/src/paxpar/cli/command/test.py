import typer
from rich.console import Console
from paxpar.cli.tools import call


console = Console()

app = typer.Typer(help="test related commands")


# pp test core -m blackbox -v tests/
@app.command()
def report():
    # pytest --html=report.html --self-contained-html
    call(
        """poetry run python -m pytest \
            --rootdir . \
            -v \
            --html=tests/report.html \
            --self-contained-html \
            --junitxml=tests/report.xml \
            -m blackbox tests/
        """,
        pythonpath_set=False,
    )


@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def core(ctx: typer.Context):
    """
        Test paxpar core service

        Based on this call made by vscode pytest integration :
        ./.venv/bin/python -m pytest --rootdir . --override-ini junit_family=xunit1 --junit-xml=/tmp/tmp-4387BOK7IHnW32PW.xml ./tests/api/test_core_check.py::test_check
    cwd: .

    """
    extra_args = " ".join(list(ctx.args))
    # poetry run pytest {extra_args}
    call(
        f"""poetry run python -m pytest --rootdir . {extra_args}""",
        pythonpath_set=False,
    )
