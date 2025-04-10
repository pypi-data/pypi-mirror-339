import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

import toml
import typer
from tabulate import tabulate

from relycomply_client.cli import RelyComplyCLI
from relycomply_client.exceptions import (
    RelyComplyClientException,
    RelyComplyCliException,
)
from relycomply_client.relycomply_gql_client import RelyComplyGQLClient


@contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)


class RelySync:
    def __init__(
        self,
        location,
        recursive,
        interactive,
        cli: RelyComplyCLI = None,
        break_on_error=True,
        create_only=False,
        debug=False,
    ):
        if debug:
            logging.root.setLevel(logging.DEBUG)
            logging.root.addHandler(logging.StreamHandler())

        self.location = location or Path(".")
        self.recursive = recursive
        self.interactive = interactive
        self.break_on_error = break_on_error
        self.create_only = create_only

        self.cli: RelyComplyCLI = cli or RelyComplyCLI()
        self.gql: RelyComplyGQLClient = self.cli.gql

        self.sync_order: list[str] = self.gql.templates["TypeRelationships"][
            "SyncOrder"
        ]
        self.sync_order_upper: list[str] = [item.upper() for item in self.sync_order]

        self.implementations: list[str] = self.gql.templates["TypeRelationships"][
            "Implementations"
        ]

    def run_cli(self):
        self.locate_files()
        self.display_locations()

        if not self.with_metadata:
            return

        self.schedule_actions()

        self.display_schedule()

        if self.interactive and not typer.prompt(
            "Are you sure you would like to continue (yes/no)?", type=bool
        ):
            return

        self.execute_schedule()

    def locate_files(self):
        # These are the supported types

        if isinstance(self.location, list):
            toml_files = [Path(raw_path) for raw_path in self.location]
        elif self.location.is_dir():
            glob_pattern = "**/*.toml" if self.recursive else "*.toml"
            toml_files = list(self.location.glob(glob_pattern))
        elif self.location.is_file():
            toml_files = [self.location]

        self.no_metadata = set()
        self.incorrect_metadata = []
        self.with_metadata = []
        for path in toml_files:
            with open(path) as f:
                lines = f.readlines()

                # Clear empty lines
                lines = [line.strip() for line in lines if line.strip()]

                # Strip preceeding normal comments
                lines = [
                    line
                    for line in lines
                    if not (line[0] == "#" and not line.startswith("#%"))
                ]

                # Has no fore-matter
                if not lines or not lines[0].startswith("#%"):
                    self.no_metadata.add(path)

                fore_lines = []
                for line in lines:
                    if line.startswith("#%"):
                        fore_lines.append(line[2:].strip())
                    else:
                        break

                metadata_str = "\n".join(fore_lines)

                try:
                    metadata = toml.loads(metadata_str)
                    if not metadata:
                        self.no_metadata.add(path)
                    elif "type" not in metadata:
                        self.incorrect_metadata.append((path, "No type information"))
                    elif (
                        "type" in metadata
                        and metadata["type"].upper() not in self.sync_order_upper
                    ):
                        self.incorrect_metadata.append(
                            (
                                path,
                                f"Type '{metadata['type']}' is not support for syncing",
                            )
                        )
                    else:
                        self.with_metadata.append((path, metadata))

                except Exception as e:
                    self.incorrect_metadata.append(
                        (path, f"Metadata TOML error: {str(e)}")
                    )

    def display_locations(self):
        if self.no_metadata:
            typer.secho("Found the following files with no metadata")
            for path in self.no_metadata:
                typer.secho("  - " + str(path))
            typer.echo()

        if self.incorrect_metadata:
            typer.secho(
                "Found the following files with incorrect metadata", fg=typer.colors.RED
            )
            for path, error in self.incorrect_metadata:
                typer.secho(f"  - {path} [{error}]", fg=typer.colors.RED)
            typer.echo()

        if self.with_metadata:
            typer.secho(
                "Found the following files with type information", fg=typer.colors.GREEN
            )
            for path, metadata in sorted(self.with_metadata):
                typer.secho(
                    f"  - {path} [type = {metadata['type']}]", fg=typer.colors.GREEN
                )
            typer.echo()

    def get_rank(self, path, metadata):
        return self.sync_order_upper.index(metadata["type"].upper()), path

    def schedule_actions(self):
        self.with_metadata.sort(key=lambda t: self.get_rank(*t))

        implements_map = {
            implementor: implemented
            for implemented, implementors in self.implementations.items()
            for implementor in implementors
        }

        for path, metadata in self.with_metadata:
            metadata["implements"] = implements_map.get(
                metadata["type"], metadata["type"]
            )

        self.schedule = [
            dict(path=path, metadata=metadata, variables=toml.load(path))
            for path, metadata in self.with_metadata
        ]

        for item in self.schedule:
            create = False

            try:
                if "name" in item["variables"]:
                    key = "name"
                elif "identifier" in item["variables"]:
                    key = "identifier"
                else:
                    key = None

                item["metadata"]["key"] = key

                if key:
                    existing = self.cli.execute(
                        item["metadata"]["implements"],
                        "retrieve",
                        {key: item["variables"][key]},
                    )
                    item["action"] = "update"
                    item["existing"] = existing
                else:
                    create = True
            except RelyComplyCliException:
                create = True

            if create:
                item["action"] = "create"
                item["existing"] = None

    def display_schedule(self):
        to_create = [item for item in self.schedule if item["action"] == "create"]
        to_update = [item for item in self.schedule if item["action"] == "update"]

        def display_schedule_table(items, message):
            if items:
                typer.secho(message)
                typer.echo()
                typer.echo(
                    tabulate(
                        [
                            [
                                item["metadata"]["type"],
                                item["variables"].get("name"),
                                item["path"],
                            ]
                            for item in items
                        ],
                        headers=["Type", "name", "path"],
                    )
                )
                typer.echo()

        display_schedule_table(to_create, "The following items will be created:")
        if not self.create_only:
            display_schedule_table(to_update, "The following items may be updated:")

    def execute_schedule(self):
        for item in self.schedule:
            try:
                with pushd(str(item["path"].parent)):
                    if item["action"] == "create":
                        typer.echo(
                            f'rely {item["metadata"]["type"]} {item["action"]} {item["path"]}'
                        )
                        self.cli.execute(
                            item["metadata"]["type"], item["action"], item["variables"]
                        )
                    elif item["action"] == "update" and not self.create_only:
                        typer.echo(
                            f'rely {item["metadata"]["type"]} {item["action"]} --id={item["variables"][item["metadata"]["key"]]} {item["path"]}'
                        )

                        self.cli.execute(
                            item["metadata"]["type"],
                            item["action"],
                            {
                                "id": item["variables"][item["metadata"]["key"]],
                                **item["variables"],
                            },
                        )
            except RelyComplyClientException as e:
                typer.secho(str(e), fg=typer.colors.RED)
                if self.break_on_error:
                    break
            except FileNotFoundError as e:
                typer.secho(f"File not found: {e.filename}", fg=typer.colors.RED)
                typer.secho(f"Referenced in file: {item['path']}", fg=typer.colors.RED)
                if self.break_on_error:
                    break


def sync(
    location: Optional[Path] = typer.Argument(
        Path("."), help="The location to look for configuration files"
    ),
    recursive: bool = typer.Option(
        False,
        help="If true will search for files recursively from the given location directory",
    ),
    interactive: bool = typer.Option(
        True, help="If true the will ask for confirmation before taking any action"
    ),
    break_on_error: bool = typer.Option(
        True,
        help="If true the sync will stop on the first error. If false it will attempt to continue.",
    ),
    create_only: bool = typer.Option(False, help="If true will only create new items"),
    debug: bool = typer.Option(False, help="Enable debug logging"),
):
    """
    This will attempt to synchronise the specified configuration files with the relycomply server.
    It will (semi-)intelligently determine if the file should be created or updated based on
    the name/identifier in the file.

    The file should have a fore-matter block at the top of the file that is TOML formatted.
    This fore-matter should specify the type of the object in the format:

    #% type="Type"

    for example:

    #% type="Product"
    name = "bank_account"
    label = "Bank Account"

    """
    rely_sync = RelySync(
        location=location,
        recursive=recursive,
        interactive=interactive,
        break_on_error=break_on_error,
        debug=debug,
        create_only=create_only,
    )
    rely_sync.run_cli()


def main():
    typer.run(sync)


if __name__ == "__main__":
    main()
