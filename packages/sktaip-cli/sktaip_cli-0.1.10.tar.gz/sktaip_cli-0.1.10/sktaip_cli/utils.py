import sys
import click
import json
import yaml
from typing import TypedDict
import os
from pydantic import BaseModel, Field


class LanggraphConfig(BaseModel):
    """graph.yaml 파일의 구조를 정의합니다."""

    package_directory: str = Field(
        description="Root Directory of your package(module)."
    )
    graph_path: str = Field(
        description="Path to the langgraph module.",
        examples=["./react_agent/graph.py:graph"],
    )
    env_file: str | None = None
    requirements_file: str | None = None


def validate_graph_yaml(graph_yaml: str) -> LanggraphConfig:
    with open(graph_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    try:
        return LanggraphConfig.model_validate(config)
    except Exception as e:
        raise click.UsageError(
            f"Invalid graph.yaml. {graph_yaml} 파일을 확인해주세요. : {e}"
        )


class SubappConfig(BaseModel):
    """subapp.yaml 파일의 구조를 정의합니다."""

    package_directory: str = Field(
        description="Root Directory of your package(module)."
    )
    subapp_path: str = Field(
        description="Path to the subapp(FastAPI) module.",
        examples=["./fastapi_example/main.py:app"],
    )
    subapp_target_uri: str = Field(
        description="Target URI of the subapp.", examples=["/simple/chat"]
    )
    env_file: str | None = Field(
        default=None, description="Path to the environment file."
    )
    requirements_file: str | None = Field(
        default=None, description="Path to the requirements file."
    )


def validate_subapp_yaml(subapp_yaml: str) -> SubappConfig:
    with open(subapp_yaml, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    try:
        return SubappConfig.model_validate(config)
    except Exception as e:
        raise click.UsageError(
            f"Invalid subapp.yaml. {subapp_yaml} 파일을 확인해주세요: {e}"
        )


def get_python_version() -> str:
    if sys.version_info < (3, 10) or sys.version_info > (3, 12):
        py_version_msg = (
            "\n\nNote: The in-mem server requires Python 3.10 ~ 3.12."
            f" You are currently using Python {sys.version_info.major}.{sys.version_info.minor}."
            ' Please upgrade your Python version before installing "sktaip_api".'
        )
        raise click.UsageError(py_version_msg)

    return ".".join(map(str, sys.version_info[:2]))


def save_docker_credentials(username, password):
    """Docker 로그인 정보를 .docker_auth.json에 저장합니다."""
    credentials = {"username": username, "password": password}
    with open(".docker_auth.json", "w") as f:
        json.dump(credentials, f)


def load_docker_credentials():
    """저장된 Docker 로그인 정보를 로드합니다."""
    if not os.path.exists(".docker_auth.json"):
        raise FileNotFoundError("Docker credentials not found. Please login first.")

    with open(".docker_auth.json", "r") as f:
        credentials = json.load(f)
    return credentials.get("username"), credentials.get("password")
