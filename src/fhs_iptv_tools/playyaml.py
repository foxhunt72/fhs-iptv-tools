"""Playyaml file."""


import sys
from . import config
from .playyaml_lib import play as play_lib


def play_command_load_m3u_file(task):
    """Play command load_m3u_file.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task["store"]
    task_file = task["file"]
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    with config.CONSOLE.status(f"Loading m3u file: {task_file}  to store: {task_store}", spinner="dots"):
        config.STORE[task_store].load_m3u_file(task_file)
    return True


def play_command_count_channels(task):
    """Play command count channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    count = config.STORE[task_store].count_channels()
    print(f"amount of channels: {count}")
    return True


def play_command_probe_scan(task):
    """Play command probe scan

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    delay = int(task['delay'])
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    with config.CONSOLE.status(f"Probe scan channel list from store: {task_store} with delay {delay}", spinner="dots"):
        config.STORE[task_store].probe_scan(delay)
    return True


def play_command_list_groups(task):
    """Play command list groups.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    groups = config.STORE[task_store].list_groups()
    for i in groups:
        print(i)
    return True


def play_command_group_channels(task):
    """Play command group channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    channels = config.STORE[task_store].group_channels(task['group'])
    for ch in channels:
        print(ch.tvg_name)
    return True


def play_command_filter_channels(task):
    """Play command filter channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import LoadType, ProbeInfoList

    task_store = task['store']
    task_type = task['type']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    if task_type == 'channels':
        with config.CONSOLE.status(f"Filter m3u list on channels to store: {task_store}", spinner="dots"):
            config.STORE[task_store].filter_lijst(LoadType.CHANNELS)
        return True
    if task_type == 'vod':
        with config.CONSOLE.status(f"Filter m3u list on vod to store: {task_store}", spinner="dots"):
            config.STORE[task_store].filter_lijst(LoadType.VOD)
        return True
    sys.stderr.write(f"ERROR: unknown filter options '{task_type}' and not channels or vod")
    return True


funcdict = {
    "load_m3u": {
        "args": [{"name": "file"}, {"name": "store", "help": "store name", "default": "default"}],
        "func": play_command_load_m3u_file,
        "help": "loading m3u file from disk."
    },
    "count_channels": {
        "args": [{"name": "store", "help": "store name", "default": "default"}],
        "func": play_command_count_channels,
        "help": "count amount of channels in m3u list."
    },
    "list_groups": {
        "args": [{"name": "store", "help": "store name", "default": "default"}],
        "func": play_command_list_groups,
        "help": "list groups."
    },
    "group_channels": {
        "args": [{"name": "store", "help": "store name", "default": "default"},{"name": "group"}],
        "func": play_command_group_channels,
        "help": "list channels for a group."
    },
    "probe_scan": {
        "args": [{"name": "store", "help": "store name", "default": "default"},{"name": "delay", "help": "delay between probing channels", "default": "5"}],
        "func": play_command_probe_scan,
        "help": "probe scanning the list of channels."
    },
    "filter_channels": {
        "args": [{"name": 'type', "help": "type to filter, channels or vod"}, {"name": "store", "help": "store name", "default": "default"}],
        "func": play_command_filter_channels,
        "help": "filter channels."
    }
}


def play(commandfile, include_tags=None, exclude_tags=None):
    """Play commandfile.

    Args:
        commandfile: yaml file with instructions
        include_tags: list of tags to run
        exclude_tags: list of tags to skip

    Returns:
        None
    """
    play_lib(commandfile, include_tags=include_tags, exclude_tags=exclude_tags, funcdict=funcdict)

    return None


def interactive_run_cmd2():
    """Play interactive

    """
    from .interactive_cmd2 import run_cmd2

    run_cmd2(funcdict=funcdict)
