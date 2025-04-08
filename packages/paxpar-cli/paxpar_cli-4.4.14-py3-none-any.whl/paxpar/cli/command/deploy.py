import typer
from rich.console import Console
from paxpar.cli.tools import call


console = Console()

app = typer.Typer(
    name="pp deploy", add_completion=False, help="pp deploy related commands"
)

"""
❯ scw container container list
ID                                    NAME                      NAMESPACE ID                          STATUS  MIN SCALE  MAX SCALE  MEMORY LIMIT  CPU LIMIT  TIMEOUT    ERROR MESSAGE  PRIVACY
6b0e651b-cc7e-4255-9264-013d1ebb8066  proxy                     8080c26f-515c-40c7-b388-fb168520207c  ready   0          1          2048          1120       5 minutes  -              public
36a7a4e1-dd3e-47d1-b381-ae003518b832  container-stoic-herschel  8080c26f-515c-40c7-b388-fb168520207c  ready   0          5          2048          1120       5 minutes  -              public
5a6669b7-cfd2-4076-809e-8a5dd14d7bea  gotenberg6-phentz         8080c26f-515c-40c7-b388-fb168520207c  ready   0          5          2048          1120       5 minutes  -              public
9645138c-a20a-4f4f-ac9b-be79a2d9f01f  gotenberg8                8080c26f-515c-40c7-b388-fb168520207c  ready   0          5          2048          1120       5 minutes  -              public
f8801dd4-a65b-44d6-b888-9aba928cad2e  simple-web                8080c26f-515c-40c7-b388-fb168520207c  ready   0          5          256           250        5 minutes  -              public
30a89147-362d-44aa-a961-7f3a158dbab9  paxpar-core-2c48f2d6      8080c26f-515c-40c7-b388-fb168520207c  ready   0          5          3072          1000       5 minutes  -              public
"""


@app.command()
def list():
    """
    List deployed containers
    """
    # TODO: get JSON with "-o"
    call("""scw container container list""")
