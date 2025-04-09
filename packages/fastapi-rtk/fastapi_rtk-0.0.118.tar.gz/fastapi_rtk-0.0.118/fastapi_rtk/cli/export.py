import json
import typing

import typer

from ..api.model_rest_api import ModelRestApi
from ..db import db
from ..globals import g
from .commands import version_callback
from .const import logger
from .decorators import ensure_fastapi_rtk_tables_exist
from .utils import run_in_current_event_loop

export_app = typer.Typer(rich_markup_mode="rich")


@export_app.callback()
@ensure_fastapi_rtk_tables_exist
def callback(
    version: typing.Annotated[
        typing.Union[bool, None],
        typer.Option(
            "--version", help="Show the version and exit.", callback=version_callback
        ),
    ] = None,
) -> None:
    """
    FastAPI RTK Export CLI - The [bold]fastapi-rtk export[/bold] command line app. 😎

    Export your [bold]FastAPI React Toolkit[/bold] data easily with this CLI.
    """


@export_app.command()
def api_schema(
    apis: typing.Annotated[
        str | None,
        typer.Option(
            ...,
            help="The APIs to export. Can be a list of APIs separated by '|' or based on the separator set in the parameter. It can also be a single API name. If not provided, all APIs will be exported. E.g: 'UsersApi|ProductsApi' or 'UsersApi'.",
        ),
    ] = None,
    filename: typing.Annotated[
        str,
        typer.Option(
            ...,
            help="The filename to export the schema to.",
        ),
    ] = "api_schema.json",
    separator: typing.Annotated[
        str,
        typer.Option(
            ...,
            help="The separator to use for the exported schema.",
        ),
    ] = "|",
):
    """
    Export the JSONForms schema from the APIs to a file.
    """
    api_classes = g.current_app.apis
    if apis:
        # Split the APIs based on the separator
        api_names = apis.split(separator)
        # Filter the APIs based on the provided names
        api_classes = [
            api for api in api_classes if api.__class__.__name__ in api_names
        ]
        # Throws error if APIs contains `BaseApi`
        if any(not isinstance(api, ModelRestApi) for api in api_classes):
            raise ValueError("You cannot export APIs that are not ModelRestApi.")
    else:
        api_classes = [api for api in api_classes if isinstance(api, ModelRestApi)]

    result = run_in_current_event_loop(_export_api_schema(api_classes), 100)
    # Save the result to a file
    with open(filename, "w") as f:
        f.write(json.dumps(result, indent=2))
    logger.info(f"Exported API schema to {filename}.")


async def _export_api_schema(apis: list[ModelRestApi]):
    result = {}
    for api in apis:
        async with db.session(
            getattr(api.datamodel.obj, "__bind_key__", None)
        ) as session:
            info = await api._generate_info_schema([], session)
            result[api.__class__.__name__] = {}
            result[api.__class__.__name__]["add"] = {
                "schema": info.add_schema,
                "ui_schema": info.add_uischema,
            }
            result[api.__class__.__name__]["edit"] = {
                "schema": info.edit_schema,
                "ui_schema": info.edit_uischema,
            }
    return result
