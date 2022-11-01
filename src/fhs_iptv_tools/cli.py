"""Console script for fhs_iptv_tools."""
import sys

import typer
from .probe import ProbeInfo
from pprint import pprint
from typing import Optional, List, Tuple

from fhs_iptv_tools import config  # noqa: F401

main = typer.Typer()


@main.command()
def probe(source: str = typer.Argument(..., help="Source Probe")):
    """Probe media.

    Args:
        source: source to probe
    """
    pp = ProbeInfo()
    pinfo = pp.probe(source)
    pprint(pinfo)


@main.command()
def probe_with_cache(source: str = typer.Argument(..., help="Source Probe")):
    """Probe media with disk cache.

    Args:
        source: source to probe
    """
    pp = ProbeInfo()
    pinfo = pp.probe_with_cache(source)
    pprint(pinfo)


@main.command()
def probe_info(source: str = typer.Argument(..., help="Source Probe")):
    """Probe media with disk cache.

    Args:
        source: source to probe
    """
    pp = ProbeInfo()
    pinfo = pp.probe_with_cache(source)
    result = pp.info2str(pinfo)
    print(f"result: {result}")


@main.command()
def probe_list(m3u_file: str = typer.Argument(..., help="M3u file")):
    """Probe media.

    Args:
        m3u_list: m3u file
    """
    from .probe_list import ProbeInfoList
    ppl = ProbeInfoList()
    ppl.probe_list(m3u_file)


@main.command()
def m3u_action(action: List[str] = typer.Option(None)):
    """Probe media.

    Args:
        action: actions
    """
    #from .probe_list import ProbeInfoList
    pprint(action)


@main.command()
def run_tasks(
    yaml_command: str = typer.Option(  # noqa: B008
        ..., help="read yaml file", envvar="fhs_xmltv_yaml", prompt=True
    ),
    force_color: bool = typer.Option(  # noqa: B008
        None, "--force-color/--no-color", help="force color in pipelines"
    ),
    include_tag: Optional[List[str]] = typer.Option(None),  # noqa: B008
    exclude_tag: Optional[List[str]] = typer.Option(None),  # noqa: B008
):
    """Run tasks in yaml file.

    Args:
        yaml_command: xmltv file to use
        force_color: force color in pipeline for example
        include_tag: tags from task to include
        exclude_tag: exclude tasks with this tag
    """
    from rich.console import Console
    from .playyaml import play

    config.CONSOLE = Console(force_terminal=force_color)
    play(yaml_command, include_tag, exclude_tag)


@main.command()
def interactive():
    """Run tasks interactive.
    """
    from .playyaml import interactive_run_cmd2

    interactive_run_cmd2()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
