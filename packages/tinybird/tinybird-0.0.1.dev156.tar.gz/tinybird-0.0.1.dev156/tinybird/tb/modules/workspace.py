# This is a command file for our CLI. Please keep it clean.
#
# - If it makes sense and only when strictly necessary, you can create utility functions in this file.
# - But please, **do not** interleave utility functions and command definitions.

from typing import Any, Dict, List, Optional

import click
from click import Context

from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    _get_workspace_plan_name,
    ask_for_organization,
    coro,
    create_workspace_interactive,
    create_workspace_non_interactive,
    echo_safe_humanfriendly_tables_format_smart_table,
    get_current_main_workspace,
    get_organizations_by_user,
    get_user_token,
    is_valid_starterkit,
    switch_workspace,
    try_update_config_with_remote,
)
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLIWorkspaceException
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.group()
@click.pass_context
def workspace(ctx: Context) -> None:
    """Workspace commands."""


@workspace.command(name="ls")
@click.pass_context
@coro
async def workspace_ls(ctx: Context) -> None:
    """List all the workspaces you have access to in the account you're currently authenticated into."""

    config = CLIConfig.get_project_config()
    client: TinyB = ctx.ensure_object(dict)["client"]

    response = await client.user_workspaces(version="v1")

    current_main_workspace = await get_current_main_workspace(config)
    if not current_main_workspace:
        raise CLIWorkspaceException(FeedbackManager.error_unable_to_identify_main_workspace())

    columns = ["name", "id", "role", "plan", "current"]
    table = []
    click.echo(FeedbackManager.info_workspaces())

    for workspace in response["workspaces"]:
        table.append(
            [
                workspace["name"],
                workspace["id"],
                workspace["role"],
                _get_workspace_plan_name(workspace["plan"]),
                current_main_workspace["name"] == workspace["name"],
            ]
        )

    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@workspace.command(name="use")
@click.argument("workspace_name_or_id")
@click.pass_context
@coro
async def workspace_use(ctx: Context, workspace_name_or_id: str) -> None:
    """Switch to another workspace. Use 'tb workspace ls' to list the workspaces you have access to."""
    config = CLIConfig.get_project_config()
    is_cloud = ctx.ensure_object(dict)["env"] == "cloud"
    if not is_cloud:
        raise CLIWorkspaceException(
            FeedbackManager.error(
                message="`tb workspace use` is not available in local mode. Use --cloud to switch to a cloud workspace and it will be used in Tinybird Local."
            )
        )

    await switch_workspace(config, workspace_name_or_id)


@workspace.command(name="current")
@click.pass_context
@coro
async def workspace_current(ctx: Context):
    """Show the workspace you're currently authenticated to"""
    config = CLIConfig.get_project_config()
    env = ctx.ensure_object(dict)["env"]
    client: TinyB = ctx.ensure_object(dict)["client"]
    if env == "cloud":
        _ = await try_update_config_with_remote(config, only_if_needed=True)

    user_workspaces = await client.user_workspaces(version="v1")
    current_workspace = await client.workspace_info(version="v1")

    def _get_current_workspace(user_workspaces: Dict[str, Any], current_workspace_id: str) -> Optional[Dict[str, Any]]:
        def get_workspace_by_name(workspaces: List[Dict[str, Any]], name: str) -> Optional[Dict[str, Any]]:
            return next((ws for ws in workspaces if ws["name"] == name), None)

        workspaces: Optional[List[Dict[str, Any]]] = user_workspaces.get("workspaces")
        if not workspaces:
            return None

        current: Optional[Dict[str, Any]] = get_workspace_by_name(workspaces, current_workspace_id)
        return current

    current_main_workspace = _get_current_workspace(user_workspaces, config.get("name", current_workspace["name"]))

    assert isinstance(current_main_workspace, dict)

    columns = ["name", "id", "role", "plan", "current"]

    table = [
        (
            current_main_workspace["name"],
            current_main_workspace["id"],
            current_main_workspace["role"],
            _get_workspace_plan_name(current_main_workspace["plan"]),
            True,
        )
    ]

    click.echo(FeedbackManager.info_current_workspace())
    echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)


@workspace.command(name="create", short_help="Create a new Workspace for your Tinybird user")
@click.argument("workspace_name", required=False)
@click.option("--starter_kit", "starter_kit", type=str, required=False, help="Use a Tinybird starter kit as a template")
@click.option("--starter-kit", "starter_kit", hidden=True)
@click.option("--user_token", is_flag=False, default=None, help="When passed, tb won't prompt asking for the token")
@click.option(
    "--fork",
    is_flag=True,
    default=False,
    help="When enabled, tb will share all data sources from the current workspace with the new one",
)
@click.option(
    "--organization-id",
    "organization_id",
    type=str,
    required=False,
    help="When passed, the workspace will be created in the specified organization",
)
@click.pass_context
@coro
async def create_workspace(
    ctx: Context,
    workspace_name: str,
    starter_kit: str,
    user_token: Optional[str],
    fork: bool,
    organization_id: Optional[str],
) -> None:
    if starter_kit and not await is_valid_starterkit(ctx, starter_kit):
        raise CLIWorkspaceException(FeedbackManager.error_starterkit_name(starterkit_name=starter_kit))

    config = CLIConfig.get_project_config()

    user_token = await get_user_token(config, user_token)

    organization_name = None
    organizations = await get_organizations_by_user(config, user_token)

    organization_id, organization_name = await ask_for_organization(organizations, organization_id)
    if not organization_id:
        return

    # If we have at least workspace_name, we start the non interactive
    # process, creating an empty workspace
    if workspace_name:
        await create_workspace_non_interactive(
            ctx, workspace_name, starter_kit, user_token, fork, organization_id, organization_name
        )
    else:
        await create_workspace_interactive(
            ctx, workspace_name, starter_kit, user_token, fork, organization_id, organization_name
        )


@workspace.command(name="delete", short_help="Delete a workspace for your Tinybird user")
@click.argument("workspace_name_or_id")
@click.option("--user_token", is_flag=False, default=None, help="When passed, tb won't prompt asking for the token")
@click.option(
    "--confirm_hard_delete",
    default=None,
    help="Enter the name of the workspace to confirm you want to run a hard delete over the workspace",
    hidden=True,
)
@click.option("--yes", is_flag=True, default=False, help="Don't ask for confirmation")
@click.pass_context
@coro
async def delete_workspace(
    ctx: Context, workspace_name_or_id: str, user_token: Optional[str], confirm_hard_delete: Optional[str], yes: bool
) -> None:
    """Delete a workspace where you are an admin."""

    config = CLIConfig.get_project_config()
    client = config.get_client()

    user_token = await get_user_token(config, user_token)

    workspaces = (await client.user_workspaces(version="v1")).get("workspaces", [])
    workspace_to_delete = next(
        (
            workspace
            for workspace in workspaces
            if workspace["name"] == workspace_name_or_id or workspace["id"] == workspace_name_or_id
        ),
        None,
    )

    if not workspace_to_delete:
        raise CLIWorkspaceException(FeedbackManager.error_workspace(workspace=workspace_name_or_id))

    if yes or click.confirm(
        FeedbackManager.warning_confirm_delete_workspace(workspace_name=workspace_to_delete.get("name"))
    ):
        client.token = user_token

        try:
            await client.delete_workspace(workspace_to_delete["id"], confirm_hard_delete, version="v1")
            click.echo(FeedbackManager.success_workspace_deleted(workspace_name=workspace_to_delete["name"]))
        except Exception as e:
            raise CLIWorkspaceException(FeedbackManager.error_exception(error=str(e)))
