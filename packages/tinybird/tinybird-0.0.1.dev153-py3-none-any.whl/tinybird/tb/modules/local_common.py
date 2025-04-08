import hashlib
import logging
import os
import re
from typing import Any, Dict

import requests

from tinybird.tb.client import AuthNoTokenException, TinyB
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLILocalException
from tinybird.tb.modules.feedback_manager import FeedbackManager

TB_IMAGE_NAME = "tinybirdco/tinybird-local:latest"
TB_CONTAINER_NAME = "tinybird-local"
TB_LOCAL_PORT = int(os.getenv("TB_LOCAL_PORT", 7181))
TB_LOCAL_HOST = re.sub(r"^https?://", "", os.getenv("TB_LOCAL_HOST", "localhost"))
TB_LOCAL_ADDRESS = f"http://{TB_LOCAL_HOST}:{TB_LOCAL_PORT}"


async def get_tinybird_local_client(config_obj: Dict[str, Any], test: bool = False, staging: bool = False) -> TinyB:
    """Get a Tinybird client connected to the local environment."""

    config = await get_tinybird_local_config(config_obj, test=test)
    return config.get_client(host=TB_LOCAL_ADDRESS, staging=staging)


async def get_tinybird_local_config(config_obj: Dict[str, Any], test: bool = False) -> CLIConfig:
    """Craft a client config with a workspace name based on the path of the project files

    It uses the tokens from tinybird local
    """
    path = config_obj.get("path")
    config = CLIConfig.get_project_config()

    try:
        # ruff: noqa: ASYNC210
        tokens = requests.get(f"{TB_LOCAL_ADDRESS}/tokens").json()
    except Exception:
        raise CLILocalException(
            FeedbackManager.error(message="Tinybird local is not running. Please run `tb local start` first.")
        )

    user_token = tokens["user_token"]
    admin_token = tokens["admin_token"]
    default_token = tokens["workspace_admin_token"]
    # Create a new workspace if path is provided. This is used to isolate the build in a different workspace.
    if path:
        user_client = config.get_client(host=TB_LOCAL_ADDRESS, token=user_token)
        if test:
            ws_name = get_test_workspace_name(path)
        else:
            ws_name = config.get("name") or config_obj.get("name") or get_build_workspace_name(path)
        if not ws_name:
            raise AuthNoTokenException()

        logging.debug(f"Workspace used for build: {ws_name}")

        user_workspaces = requests.get(
            f"{TB_LOCAL_ADDRESS}/v1/user/workspaces?with_organization=true&token={admin_token}"
        ).json()
        user_org_id = user_workspaces.get("organization_id", {})
        local_workspaces = user_workspaces.get("workspaces", [])

        ws = next((ws for ws in local_workspaces if ws["name"] == ws_name), None)

        # If we are running a test, we need to delete the workspace if it already exists
        if test and ws:
            requests.delete(
                f"{TB_LOCAL_ADDRESS}/v1/workspaces/{ws['id']}?token={user_token}&hard_delete_confirmation=yes"
            )
            ws = None

        if not ws:
            await user_client.create_workspace(
                ws_name, template=None, assign_to_organization_id=user_org_id, version="v1"
            )
            user_workspaces = requests.get(f"{TB_LOCAL_ADDRESS}/v1/user/workspaces?token={admin_token}").json()
            ws = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == ws_name), None)
            if not ws:
                raise AuthNoTokenException()

        ws_token = ws["token"]
        config.set_token(ws_token)
        config.set_token_for_host(TB_LOCAL_ADDRESS, ws_token)
        config.set_host(TB_LOCAL_ADDRESS)
    else:
        config.set_token(default_token)
        config.set_token_for_host(TB_LOCAL_ADDRESS, default_token)

    config.set_user_token(user_token)
    return config


def get_build_workspace_name(path: str) -> str:
    folder_hash = hashlib.sha256(path.encode()).hexdigest()
    return f"Tinybird_Local_Build_{folder_hash}"


def get_test_workspace_name(path: str) -> str:
    folder_hash = hashlib.sha256(path.encode()).hexdigest()
    return f"Tinybird_Local_Test_{folder_hash}"
