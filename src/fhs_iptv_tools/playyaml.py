"""Playyaml file."""


import sys
from . import config
from .playyaml_lib import func_dict_parse, play as play_lib


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


def play_command_save_m3u_file(task):
    """Play command save_m3u_file.

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
        config.STORE[task_store].save_m3u_file(file=task_file, with_tag=task['with_tag'], without_tag=task['without_tag'])
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


def play_command_dump_channels(task):
    """Play command dump channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList, LoadType
    from pprint import pprint

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    channels = config.STORE[task_store].filter_lijst(LoadType.ALL)
    pprint(channels)
    return True


def play_command_delete_channels(task):
    """Play command delete channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList, LoadType

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    count = config.STORE[task_store].delete_channels(with_tag=task['with_tag'], without_tag=task['without_tag'])
    print(f"removed {count} channels.")
    return True


def play_command_list_channels(task):
    """Play command list channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    count = config.STORE[task_store].list_channels(with_tag=task['with_tag'], without_tag=task['without_tag'])
    print(f"list {count} channels.")
    return True


def play_command_modify_channels(task):
    """Play command modify channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    count = config.STORE[task_store].modify_channels(
        with_tag=task['with_tag'],
        without_tag=task['without_tag'],
        with_id=task['with_id'],
        set_id=task['set_id'],
        set_name=task['set_name'],
        set_group_title=task['set_group_title'],
        set_logo=task['set_logo'],
    )

    print(f"modified {count} channels.")
    return True


def play_command_select(task):
    """Play command select.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    count = config.STORE[task_store].select(
        with_tag=task['with_tag'],
        without_tag=task['without_tag'],
        tvg_group_title=task['group_title'],
        tvg_name=task['name'],
        tvg_id=task['id'],
        tvg_source=task['source'],
        set_tag=task['set_tag'],
        clear_tag=task['clear_tag'])
    print(f"selected {count} channels.")
    return True


def play_command_add_channel(task):
    """Play command add channel.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    config.STORE[task_store].add_channel(tvg_id=task['id'], tvg_name=task['name'], tvg_logo=task['logo_url'], tvg_group_title=task['group_title'], tvg_source=task['source'])
    print(f"add channel: {task['id']} / {task['name']}")
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
    "dump_channels": {
        "args": [{"name": "store", "help": "store name", "default": "default"}],
        "func": play_command_dump_channels,
        "help": "dump channels using pprint."
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
    },
    "add_channel": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "id"},
            {"name": "name"},
            {"name": "logo_url", "default": ""},
            {"name": "group_title"},
            {"name": "source"}
        ],
        "func": play_command_add_channel,
        "loop": "channels",
        "help": "add channel."
    },
    "delete_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
        ],
        "func": play_command_delete_channels,
        "help": "delete channels."
    },
    "modify_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "with_id", "default": ""},
            {"name": "set_id", "default": ""},
            {"name": "set_name", "default": ""},
            {"name": "set_group_title", "default": ""},
            {"name": "set_logo", "default": ""},
        ],
        "func": play_command_modify_channels,
        "loop": "channels",
        "help": "modify channels."
    },
    "list_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
        ],
        "func": play_command_list_channels,
        "help": "list channels."
    },
    "save_m3u": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "file"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
        ],
        "func": play_command_save_m3u_file,
        "help": "save channels."
    },
    "select": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "group_title", "default": ""},
            {"name": "name", "default": ""},
            {"name": "id", "default": ""},
            {"name": "source", "default": ""},
            {"name": "set_tag", "default": ""},
            {"name": "clear_tag", "default": ""}
        ],
        "func": play_command_select,
        "help": "select channels."
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
    play_lib(commandfile, include_tags=include_tags, exclude_tags=exclude_tags, funcdict=func_dict_parse(funcdict))

    return None


def interactive_run_cmd2():
    """Play interactive

    """
    from .interactive_cmd2 import run_cmd2

    run_cmd2(funcdict=func_dict_parse(funcdict, for_type="interactive"))
