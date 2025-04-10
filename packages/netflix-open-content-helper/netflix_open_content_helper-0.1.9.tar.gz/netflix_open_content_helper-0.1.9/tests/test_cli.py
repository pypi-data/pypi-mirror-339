"""Tests for the Netflix Open Content Helper package."""

from unittest import mock

import pytest
from typer.testing import CliRunner

from netflix_open_content_helper import CONFIG
from netflix_open_content_helper.cli import app

runner = CliRunner(mix_stderr=False)


def test_app_reports_version() -> None:
    """Test that the version is reported."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "Netflix Open Content Helper, version" in result.stdout


@mock.patch("netflix_open_content_helper.cli.webbrowser.open_new")
def test_app_browse_calls_webbrowser(mock_webbrowser_open: mock.Mock) -> None:
    """Test that the browse action calls webbrowser.open_new."""
    runner.invoke(app, ["browse"])
    assert mock_webbrowser_open.called


@mock.patch.dict(CONFIG, {"netflix_open_content_url": ""})
def test_app_browse_validates_content_url_is_present() -> None:
    """Test that the browse action validates the content URL is present."""
    with pytest.raises(ValueError) as excinfo:
        runner.invoke(app, ["browse"], catch_exceptions=False)
    assert "Netflix Open Content URL is not configured." in str(excinfo.value)


@mock.patch.dict(CONFIG, {"netflix_open_content_url": "opencontent.netflix.com/"})
def test_app_browse_validates_content_url_is_valid() -> None:
    """Test that the browse action validates the content URL has proper syntax."""
    with pytest.raises(ValueError) as excinfo:
        runner.invoke(app, ["browse"], catch_exceptions=False)
    assert "Invalid URL format for url" in str(excinfo.value)


def test_app_lists_frame_content_by_default() -> None:
    """Test that the default list action shows frame content."""
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    assert "with frames" in result.stdout
    assert "chimera" in result.stdout
    assert "cosmoslaundromat" in result.stdout


def test_app_lists_nonframe_content_with_option() -> None:
    """Test that the list action can optionally show non-frame content."""
    result = runner.invoke(app, ["list", "--no-only-frames"])
    assert result.exit_code == 0
    assert "with frames" not in result.stdout
    assert "chimera" in result.stdout
    assert "cosmoslaundromat" in result.stdout
    assert "elfuente" in result.stdout
    assert "nocturne" in result.stdout


def test_app_download_validates_frame_options() -> None:
    """Test that the download frame numbers are validated."""
    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app, ["download", "sparks", "-fs", -1, "-fe", 0], catch_exceptions=False
        )
    assert "must be positive integers." in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app, ["download", "sparks", "-fs", 2, "-fe", 1], catch_exceptions=False
        )
    assert "must be less than or equal to end frame" in str(excinfo.value)


def test_app_download_has_dry_run_option() -> None:
    """Test that the download honors dry-run mode."""
    result = runner.invoke(app, ["download", "sparks", "-n"])
    assert "dry-run" in result.stdout


def test_app_download_validates_rename_option() -> None:
    """Test that the download rename string is validated."""
    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app,
            ["download", "sparks", "-n", "--rename", "newname"],
            catch_exceptions=False,
        )
    assert "contain a frame substitution wildcard like %04d." in str(excinfo.value)


def test_app_download_renumber_option_requires_rename_option() -> None:
    """Test that the download rename string is validated."""
    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app, ["download", "sparks", "-n", "--renumber", 5], catch_exceptions=False
        )
    assert "Option --renumber requires --rename." in str(excinfo.value)


def test_app_download_rename_is_honored() -> None:
    """Test that the download rename string is honored."""
    result = runner.invoke(
        app, ["download", "sparks", "-n", "--rename", "sparks-rename.%05d.exr"]
    )
    assert (
        "sparks/aces_image_sequence_59_94_fps/SPARKS_ACES_00001.exr sparks-rename.00001.exr"
        in result.stdout
    )


def test_app_download_rename_and_renumber_are_honored() -> None:
    """Test that the download rename and renumber parameters are honored."""
    result = runner.invoke(
        app,
        [
            "download",
            "sparks",
            "-n",
            "--rename",
            "sparks-renumber.%04d.exr",
            "--renumber",
            2001,
        ],
    )
    assert (
        "sparks/aces_image_sequence_59_94_fps/SPARKS_ACES_00001.exr sparks-renumber.2001.exr"
        in result.stdout
    )


@mock.patch("netflix_open_content_helper.cli.subprocess.run")
def test_app_download_calls_subprocess(mock_subprocess_run: mock.Mock) -> None:
    """Test that the download action calls subprocess.run."""
    runner.invoke(app, ["download", "sparks"])
    assert mock_subprocess_run.called


def test_app_download_checks_asset_name() -> None:
    """Test that the download action reports when an asset name is not in the config."""
    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app, ["download", "badname", "-n", "--renumber", 5], catch_exceptions=False
        )
    assert "not found in config. Check asset name." in str(excinfo.value)


bad_assets = [
    {"name": "missing_s3_uri", "s3_uri": None},
    {"name": "bad_s3_uri", "s3_uri": "bad_uri"},
    {
        "name": "missing_s3_basename",
        "s3_uri": "s3://download.opencontent.netflix.com/sparks/aces_image_sequence_59_94_fps",
        "s3_basename": None,
    },
    {
        "name": "bad_s3_basename",
        "s3_uri": "s3://download.opencontent.netflix.com/sparks/aces_image_sequence_59_94_fps",
        "s3_basename": "bad_basename",
    },
]


@mock.patch.dict(CONFIG, {"assets": bad_assets})
def test_app_download_validates_asset_config_values() -> None:
    """Test that the download action validates the asset parameters in the config file."""
    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app,
            ["download", "missing_s3_uri", "-n", "--renumber", 5],
            catch_exceptions=False,
        )
    assert "S3 URI is not configured for" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app,
            ["download", "bad_s3_uri", "-n", "--renumber", 5],
            catch_exceptions=False,
        )
    assert "Invalid S3 URI format" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app,
            ["download", "missing_s3_basename", "-n", "--renumber", 5],
            catch_exceptions=False,
        )
    assert "S3 basename is not configured for" in str(excinfo.value)

    with pytest.raises(ValueError) as excinfo:
        runner.invoke(
            app,
            ["download", "bad_s3_basename", "-n", "--renumber", 5],
            catch_exceptions=False,
        )
    assert "Invalid S3 basename format" in str(excinfo.value)
