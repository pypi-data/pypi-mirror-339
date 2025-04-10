import subprocess
import webbrowser
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.progress import track

from netflix_open_content_helper import CONFIG, __version__


def download_from_s3(
    s3_uri: str, s3_path: str, dest_path: str = ".", dry_run: bool = False
) -> None:
    """
    Download a file from AWS S3.

    Args:
        s3_uri (str): The base S3 URI.
        s3_path (str): The specific path to the file in S3.
        dest_path (str): The destination path for the downloaded file.
        dry_run (bool): If true, show what would be done, but do not do it.
    """
    commands = [
        "aws",
        "s3",
        "cp",
        "--quiet",
        "--no-sign-request",
        f"{s3_uri}/{s3_path}",
        dest_path,
    ]
    if dry_run:
        print(f"dry-run: {' '.join(commands)}")
    else:
        subprocess.run(commands, check=True)


def version_callback(value: bool) -> None:
    """Display the version of the package."""
    if value:
        typer.echo(f"Netflix Open Content Helper, version {__version__}")
        raise typer.Exit()


app = typer.Typer()


@app.callback()
def common(
    version: bool = typer.Option(
        False,
        "--version",
        is_eager=True,
        help="Show the version of the package.",
        callback=version_callback,
    ),
) -> None:
    """A utility for interacting with Netflix Open Content media."""
    pass


@app.command()
def browse() -> None:
    """
    Open a web browser to the Netflix Open Content URL.
    """
    NETFLIX_OPEN_CONTENT_URL = CONFIG["netflix_open_content_url"]
    # Check if the URL is configured
    if not NETFLIX_OPEN_CONTENT_URL:
        raise ValueError(
            "Netflix Open Content URL is not configured. Check the config file."
        )
    # Check if the URL is valid
    if not NETFLIX_OPEN_CONTENT_URL.startswith(("http://", "https://")):
        raise ValueError(
            f"Invalid URL format for url {NETFLIX_OPEN_CONTENT_URL}. Should start with 'http://' or 'https://'."
        )
    # Open the URL in the default web browser
    # This will open the URL in a new tab if the browser is already open
    # or in a new window if the browser is not open
    # Note: This will not work in a headless environment
    # such as a server without a GUI
    # or in a terminal without a web browser
    webbrowser.open_new(NETFLIX_OPEN_CONTENT_URL)


@app.command()
def download(
    name: Annotated[
        str, typer.Argument(help="The name of the project to download from.")
    ],
    frame_start: Annotated[
        int,
        typer.Option("--frame-start", "-fs", help="The start frame for the download."),
    ] = 1,
    frame_end: Annotated[
        int, typer.Option("--frame-end", "-fe", help="The end frame for the download.")
    ] = 1,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Force download/overwrite of files that already exist.",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            "-n",
            help="Show what would be done, but do not do it.",
        ),
    ] = False,
    rename: Annotated[
        Optional[str],
        typer.Option(help="A new name for the downloaded frames. Ex. name.%04d.ext."),
    ] = "",
    renumber: Annotated[
        Optional[int],
        typer.Option(
            help="A new start frame for the downloaded frames (with rename). Ex. 1001."
        ),
    ] = None,
) -> None:
    """Download frames from Netflix Open Content project NAME to the current directory."""

    typer.echo(f"Downloading: {name} frames {frame_start}-{frame_end}")
    # Validate the frame range
    if frame_start < 1 or frame_end < 1:
        raise ValueError(
            f"Frame numbers ({frame_start}, {frame_end}) must be positive integers."
        )
    if frame_start > frame_end:
        raise ValueError(
            f"Start frame ({frame_start}) must be less than or equal to end frame ({frame_end})."
        )

    # Check if the AWS CLI is installed
    test_commands = ["aws", "--version"]
    try:
        subprocess.run(test_commands, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        raise OSError(
            "AWS CLI is not installed. Please install it to use this feature."
        ) from exc

    # Obtain the asset configuration, conform to lower-case name
    assets = [d for d in CONFIG["assets"] if d["name"] == name.lower()]
    if not assets:
        print(f"Asset {name} not found in config.")
        list_assets()
        raise ValueError(f"Asset '{name}' not found in config. Check asset name.")

    asset = assets[0]
    # Check if the S3 URI is configured for the asset
    s3_uri = asset["s3_uri"]

    if not s3_uri:
        raise ValueError(
            f"S3 URI is not configured for '{name}'. Check the config file."
        )
    # Check if the S3 URI is valid
    if not s3_uri.startswith("s3://"):
        raise ValueError(f"Invalid S3 URI format {s3_uri}. Must start with 's3://'.")
    s3_basename = asset["s3_basename"]
    if not s3_basename:
        raise ValueError(
            f"S3 basename is not configured for '{name}'. Check the config file."
        )
    # Check if the S3 basename is valid
    if "%" not in s3_basename:
        raise ValueError(
            f"Invalid S3 basename format '{s3_basename}'. Must contain a frame substitution wildcard like %04d. Check the config file."
        )
    # check if the rename syntax is valid.
    if rename and "%" not in rename:
        raise ValueError(
            f"Invalid rename format '{rename}'. Must contain a frame substitution wildcard like %04d."
        )
    # Generate the S3 path for each frame
    if renumber:
        if not rename:
            raise ValueError("Option --renumber requires --rename.")
        renumber_offset = renumber - frame_start
    for value in track(range(frame_start, frame_end + 1), description="Downloading..."):
        # Generate the S3 path
        s3_path = s3_basename % value
        frame_path = Path(s3_path)
        if rename:
            rename_value = value + renumber_offset if renumber else value
            rename_path = rename % rename_value
            frame_path = Path(rename_path)
        # check if the frame exists on disk already
        if Path(frame_path.name).is_file() and not force:
            print(f"file {frame_path.name} exists, skipping. Use --force to overwrite.")
            continue

        # Download the content from S3, renaming if requested
        dest_path = rename_path if rename else "."
        download_from_s3(s3_uri, s3_path, dest_path=dest_path, dry_run=dry_run)


@app.command("list")
def list_assets(
    only_frames: bool = typer.Option(True, help="Only list assets with frame content."),
) -> None:
    """
    List available Netflix Open Content.

    Some open content assets may not have frame content.

    Args:
        only_frames (bool): If True, only list assets with frames.
    """
    message = "Available content"
    if only_frames:
        message += " with frames:"
    else:
        message += ":"
    typer.echo(message)
    for asset in sorted(CONFIG["assets"], key=lambda x: x["name"]):
        if only_frames and not asset.get("s3_uri"):
            continue
        typer.echo(f"- {asset['name']:<20}: {asset['description']}")


if __name__ == "__main__":
    app()
