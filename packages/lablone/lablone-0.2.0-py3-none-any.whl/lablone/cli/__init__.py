from pathlib import Path
from urllib.parse import urlencode

import click
import httpx
import trio
from gaveta.files import ensure_dir
from gaveta.time import ISOFormat, now_iso

from lablone import __version__
from lablone.cli.constants import (
    ARCHIVE_FORMAT,
    BASE_OUTPUT_FOLDER,
    BASE_URL,
    DEFAULT_ENV_VARIABLE,
    REPOS_ENDPOINT,
)
from lablone.cli.models import Project, Projects


def get_repos(token: str) -> list[Project]:
    with httpx.Client(
        base_url=BASE_URL,
        params={"private_token": token, "owned": True, "per_page": 100},
    ) as client:
        r = client.get(REPOS_ENDPOINT)

    data = r.json()

    return Projects.validate_python(data)


def save_repos(repos: list[Project], output_folder: Path) -> None:
    output_repos = output_folder / "repos.json"

    with output_repos.open(mode="w", encoding="utf-8") as f:
        f.write(Projects.dump_json(repos, indent=2).decode("utf-8"))
        f.write("\n")

    click.echo(f"{output_repos} ✓")


def generate_archive_endpoint(repo: Project) -> str:
    params = urlencode({"sha": repo.default_branch})
    endpoint = f"/projects/{repo.id}/repository/archive.{ARCHIVE_FORMAT}"

    return f"{endpoint}?{params}"


async def get_single_archive(
    client: httpx.AsyncClient,
    repo: Project,
    output_folder: Path,
    limiter: trio.CapacityLimiter,
) -> None:
    async with limiter:
        archive_url = generate_archive_endpoint(repo)
        filename = f"{repo.name}-{repo.default_branch}.{ARCHIVE_FORMAT}"
        output_archive = output_folder / filename

        r = await client.get(archive_url)

        async with await trio.open_file(output_archive, mode="wb") as f:
            async for chunk in r.aiter_bytes():
                await f.write(chunk)

        click.echo(f"{output_archive} ✓")


async def get_archives(token: str, repos: list[Project], output_folder: Path) -> None:
    limiter = trio.CapacityLimiter(20)

    async with (
        httpx.AsyncClient(base_url=BASE_URL, params={"private_token": token}) as client,
        trio.open_nursery() as nursery,
    ):
        for repo in repos:
            nursery.start_soon(get_single_archive, client, repo, output_folder, limiter)


@click.command()
@click.option(
    "-t",
    "--token",
    type=str,
    metavar="VALUE",
    envvar=DEFAULT_ENV_VARIABLE,
    show_envvar=True,
)
@click.version_option(version=__version__)
def main(token: str) -> None:
    """A CLI to back up all your GitLab repositories."""
    output_folder = BASE_OUTPUT_FOLDER / now_iso(ISOFormat.BASIC)
    ensure_dir(output_folder)

    repos = get_repos(token)
    save_repos(repos, output_folder)

    trio.run(get_archives, token, repos, output_folder)

    click.echo(f"Number of repos: {len(repos)}")
    click.echo(f"Output folder: {output_folder}")
    click.echo("Done!")
