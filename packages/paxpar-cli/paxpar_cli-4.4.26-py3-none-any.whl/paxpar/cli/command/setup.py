from abc import abstractmethod
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
from typing import Callable

import typer
from rich.console import Console
from packaging.specifiers import SpecifierSet
from packaging.version import Version

from paxpar.cli.tools import PaxparCLI_ObjCtx, call, root_command_callback

console = Console()

app = typer.Typer(
    help="Setup/clean pp env",
    callback=root_command_callback(),
)


def call_output(
    cmd: str | None,
    ctx_obj: PaxparCLI_ObjCtx | None = None,
) -> str:
    if cmd is None:
        return ""

    query = call(
        cmd,
        stdout=subprocess.PIPE,
        ctx_obj=ctx_obj,
        executable='/bin/bash',
    )
    #output = query.decode()
    output = query.stdout.decode()
    return output


# cf https://peps.python.org/pep-0440/#version-specifiers
SPEC_SPECIAL_CHARS = "~=!<>"
# ~=: Compatible release clause
# ==: Version matching clause
# !=: Version exclusion clause
# <=, >=: Inclusive ordered comparison clause
# <, >: Exclusive ordered comparison clause
# ===: Arbitrary equality clause
def _version_strip(version: str) -> str:
    for char in SPEC_SPECIAL_CHARS:
        version = version.replace(char, "")
    return version

@dataclass
class SetupTool:
    name: str
    version: str | None = None
    # version_get: Callable[[], str | None]
    # install: Callable[[], None]
    version_get: str | None = None
    install: str | None = None

    # @abstractmethod
    # def install(self): ...

    # @abstractmethod
    # def version_get(self) -> str | None: ...

    def _current_version_extract(self) -> str:
        if self.version_get is None:
            return ""
        version_current = call_output(
            self.version_get,
            #ctx_obj=ctx_obj,
        )
        #print('version_current====', version_current)
        match = re.search(r'(\d+\.\d+\.\d+)', version_current)
        return match.group(0) if match else '0.0.0'


    # see https://packaging.pypa.io/en/stable/specifiers.html#usage
    def _version_valid(self, version: str) -> bool:
        if self.version:
            if self.version[0] in SPEC_SPECIAL_CHARS:
                v = Version(version)
                v_spec = SpecifierSet(self.version or '0.0.0')
                return v in v_spec
            else:
                return self.version in version
        else:
            return True        

    def setup(
        self,
        ctx_obj: PaxparCLI_ObjCtx,
    ):
        version_current = self._current_version_extract()
        # if version_current is None:
        if not self._version_valid(version_current) and self.install:
            call(
                self.install.format(version=_version_strip(self.version)),
                ctx_obj=ctx_obj,
                executable='/bin/bash',
            )
            version_current = self._current_version_extract()

        if self._version_valid(version_current) or self.version is None:
            print(f"{self.name}{self.version} ok (found {version_current})")
        else:
            print(f"{self.name}{self.version} not found ! (found {version_current})")


tools: list[SetupTool] = [
    SetupTool(
        name="nvm",
        version="==0.40.2",
        install="""curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v{version}/install.sh | bash""",
        version_get="""
            . $HOME/.nvm/nvm.sh
            nvm --version
        """,
    ),
    SetupTool(
        name="npx",
        version="==10.9.2",
        install="""
            . $HOME/.nvm/nvm.sh
            nvm install --lts
            nvm use --lts
        """,
        version_get="""
            . $HOME/.nvm/nvm.sh
            npx --version
        """,
    ),
    SetupTool(
        name="podman",
        version=">=4.3.1",
        install="""
            apt update
            apt install --yes podman
        """,
        version_get="""podman --version""",
    ),
    SetupTool(
        name="kubectl",
        # curl -L -s https://dl.k8s.io/release/stable.txt
        version=">=1.32.3",
        install="""
            curl -LO "https://dl.k8s.io/release/v{version}/bin/linux/amd64/kubectl"
            chmod a+x kubectl
            mv kubectl /usr/local/bin/
        """,
        version_get="""kubectl version --client""",
    ),
    SetupTool(
        name="helm",
        version="==3.17.2",
        install="""
            wget --quiet -nv https://get.helm.sh/helm-v{version}-linux-amd64.tar.gz
            tar -xf helm-*.tar.gz
            mv linux-amd64/helm /usr/local/bin/helm
            rm -R helm-*.tar.gz* linux-amd64
            helm init --stable-repo-url=https://charts.helm.sh/stable --client-only
            helm repo update
        """,
        version_get="""helm version""",
    ),
    SetupTool(
        name="zellij",
        version="==0.42.1",
        install="""
            wget --quiet -nv https://github.com/zellij-org/zellij/releases/download/v{version}/zellij-x86_64-unknown-linux-musl.tar.gz
            tar -xvf zellij*.tar.gz
            rm zellij*.tar.gz
            chmod +x zellij
            mv zellij /usr/local/bin/
        """,
        version_get="""zellij --version""",
    ),
    SetupTool(
        name="java",
        version=">=17.0.0",
        install="""
            apt update
            apt install --yes openjdk-17-jre
        """,
        version_get="""java --version""",
    ),
    SetupTool(
        name="minio",
        # wget -q -O - https://dl.min.io/server/minio/release/linux-amd64/ | grep -Eo 'minio_[^"]*_amd64\.deb' | sort -u
        # version= 'RELEASE.2025-03-12T18-04-18Z',
        # RUN MINIO_FILENAME=`wget -q -O - https://dl.min.io/server/minio/release/linux-amd64/ | grep -Eo 'minio_[^"]*_amd64\.deb' | sort -u` \
        #    && wget --quiet https://dl.min.io/server/minio/release/linux-amd64/$MINIO_FILENAME \
        #    && dpkg -i minio_*_amd64.deb \
        #    && rm *.deb
        install="""
            wget --quiet https://dl.min.io/server/minio/release/linux-amd64/minio_20250312180418.0.0_amd64.deb
            dpkg -i minio_*_amd64.deb
            rm minio_*_amd64.deb
        """,
        version_get="""minio --version""",
    ),
]



@app.command()
def tool(
    ctx: typer.Context,
    tool: str,
):
    for t in tools:
        if tool in (t.name, ''):
            t.setup(ctx_obj = ctx.obj)


@app.command()
def all(
    ctx: typer.Context,
):
    """
    Setup all paxpar tools
    """
    tool(ctx, '')


@app.command()
def clean():
    """
    Clean paxpar env
    """
    # for svc in (
    #    "paxpar/services/core",
    #    "paxpar/services/forge",
    # ):
    #    call("""rm -Rf .venv""", cwd=svc)
    call("""find . -type d -name "__pycache__" | xargs rm -rf {}""")
    call("""rm -Rf node_modules .coverage .mypy_cache""")
    # for svc in ("front",):
    #    call("""rm -Rf node_modules""", cwd=f"services/{svc}")
    call("""rm -Rf .venv""")
    call("""rm -Rf ~/.pyenv""")


@app.command()
def registry_reset():
    """
    Reset the microk8s registry
    """

    """
    TODO: other hints :

        microk8s disable storage:destroy-storage
        microk8s enalbe storage

        microk8s.ctr images list -q | grep paxpa
        microk8s.ctr images remove ###ref
        docker image rm ###
        ctr images remove
    """
    call(
        """
        docker system prune -a -f --volumes
        microk8s.disable registry
        sleep 3
        microk8s.enable registry
    """
    )
