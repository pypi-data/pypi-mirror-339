import os
import sys
import click
import json
from click import secho
import pathlib
import shutil
from typing import Optional
import tempfile
import subprocess
import requests
from sktaip_cli.docker import (
    generate_subapp_dockerfile,
    dockerfile_build,
    create_dockerfile_and_build,
)
from sktaip_cli.exec import Runner, subp_exec
from sktaip_cli.progress import Progress
from sktaip_cli.utils import (
    get_python_version,
    validate_subapp_yaml,
    SubappConfig,
)
from sktaip_cli.port import docker_login


@click.group()
def subapp():
    """Subapp CLI"""
    pass


# 2. Run API Server on Local
@subapp.command(help="🖥 Run the API server on local")
@click.option("--host", default="127.0.0.1", help="Host address")
@click.option("--port", default=28080, type=int, help="Port number")
@click.option("--subapp_yaml", default="./subapp.yaml", help="Path to subapp.yaml")
def dev(host, port, subapp_yaml):
    """Run the development server."""
    try:
        from sktaip_api.server import run_with_subapp
    except ImportError as e:
        py_version_msg = ""
        if sys.version_info < (3, 10) or sys.version_info > (3, 12):
            py_version_msg = (
                "\n\nNote: The in-mem server requires Python 3.10 ~ 3.12."
                f" You are currently using Python {sys.version_info.major}.{sys.version_info.minor}."
                ' Please upgrade your Python version before installing "sktaip_api".'
            )
        try:
            from importlib import util

            if not util.find_spec("sktaip_api"):
                raise click.UsageError(
                    "Required package 'sktaip_api' is not installed.\n"
                    "Please install it with:\n\n"
                    '    pip install -U "sktaip_api"'
                    f"{py_version_msg}"
                )
        except ImportError:
            raise click.UsageError(
                "Could not verify package installation. Please ensure Python is up to date and\n"
                "Please install it with:\n\n"
                '    pip install -U "sktaip_api"'
                f"{py_version_msg}"
            )
        raise click.UsageError(
            "Could not import run_server. This likely means your installation is incomplete.\n"
            "Please install it with:\n\n"
            '    pip install -U "sktaip_api"'
            f"{py_version_msg}"
        )

    working_dir = os.getcwd()
    working_dir = os.path.abspath(working_dir)

    config_path = os.path.join(working_dir, subapp_yaml)
    config: SubappConfig = validate_subapp_yaml(subapp_yaml)

    # package_directory를 Python 경로에 추가
    package_directory = config.package_directory

    abs_package_dir = os.path.abspath(os.path.join(working_dir, package_directory))
    if abs_package_dir not in sys.path:
        sys.path.append(abs_package_dir)

    subapp_path = config.subapp_path
    abs_subapp_path = os.path.abspath(os.path.join(working_dir, subapp_path))
    subapp_target_uri = config.subapp_target_uri
    abs_subapp_target_uri = os.path.abspath(
        os.path.join(working_dir, subapp_target_uri)
    )
    env_path = config.env_file
    if env_path:
        env_path = os.path.abspath(os.path.join(working_dir, env_path))

    secho(
        f"Starting server at {host}:{port}. SubApp path: {abs_subapp_path}, SubApp target uri: {abs_subapp_target_uri}",
        fg="green",
    )
    run_with_subapp(
        host=host,
        port=port,
        redirect_des_uri=abs_subapp_target_uri,
        subapp_path=abs_subapp_path,
        env_file=env_path,
    )


@subapp.command(help="🐳 Generate a Dockerfile for Agent API Server")
@click.option("--output", default="./sktaip.Dockerfile", help="Path to Dockerfile")
@click.option("--subapp_yaml", default="./subapp.yaml", help="Path to subapp.yaml")
def dockerfile(output: str, subapp_yaml: str) -> None:
    """Dockerfile 내용을 생성합니다."""
    save_path = pathlib.Path(output).absolute()
    secho(f"🔍 Validating configuration at path: {subapp_yaml}", fg="yellow")
    config: SubappConfig = validate_subapp_yaml(subapp_yaml)
    secho("✅ Configuration validated!", fg="green")
    secho(f"📝 Generating Dockerfile at {save_path}", fg="yellow")
    python_version = get_python_version()
    dockerfile_content = generate_subapp_dockerfile(config, python_version)
    with open(str(save_path), "w", encoding="utf-8") as f:
        f.write(dockerfile_content)
    secho(f"✅ Dockerfile Created", fg="green")


@subapp.command(help="🐳 Build a Docker image for Agent API Server")
@click.option(
    "--tag",
    "-t",
    help="""Tag for the docker image.

    \b
    Example:
        langgraph build -t my-image

    \b
    """,
    required=True,
)
@click.option(
    "--dockerfile",
    "-f",
    help="""File path to the Dockerfile. If not provided, a Dockerfile will be generated automatically.
    """,
    required=False,
    default=None,
)
@click.option(
    "--base-image",
    hidden=True,
)
@click.option(
    "--subapp_yaml", "-c", default="./subapp.yaml", help="Path to subapp.yaml"
)
@click.option("--pull", is_flag=True, help="Pull the latest base image")
@click.option("--directory", "-d", help="Directory to build the image", default=".")
@click.argument("docker_build_args", nargs=-1, type=click.UNPROCESSED)
def build(
    subapp_yaml: str,
    docker_build_args: list[str],
    base_image: Optional[str],
    tag: str,
    pull: bool,
    directory: str,
    dockerfile: Optional[str],
):
    # Docker 설치 확인
    if shutil.which("docker") is None:
        raise click.ClickException("Docker가 설치되어 있지 않습니다.")

    secho(f"🔍 Validating configuration at path: {subapp_yaml}", fg="yellow")
    config: SubappConfig = validate_subapp_yaml(subapp_yaml)
    secho("✅ Configuration validated!", fg="green")
    if dockerfile:
        secho(f"📝 Using Dockerfile at {dockerfile}", fg="yellow")
        dockerfile_build(directory, dockerfile, tag, docker_build_args)
    else:
        create_dockerfile_and_build(
            base_image, tag, config, docker_build_args, pull, directory
        )


if __name__ == "__main__":
    subapp()
