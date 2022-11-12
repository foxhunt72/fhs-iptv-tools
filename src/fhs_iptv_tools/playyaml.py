"""Playyaml file."""


import sys
from . import config
from .playyaml_lib import func_dict_parse, play as play_lib


def play_command_run_tasks(task):
    """Play command load_m3u_file.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_file = task["file"]
    include_tag = task['include_tag']
    if include_tag == "":
        include_tag = None
    exclude_tag = task['exclude_tag']
    if exclude_tag == "":
        exclude_tag = None
    play(task_file, include_tag, exclude_tag)
    return True

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


def play_command_clear_tag(task, quiet=False):
    """Play command clear tag.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    all_stores = task['all_stores']
    tag = task['tag']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    if all_stores != "":
        count = 0
        for store in config.STORE:
            count += config.STORE[store].clear_tag(tag=tag)
    else:
        count = config.STORE[task_store].clear_tag(tag=tag)
    if quiet is False:
        print(f"cleared tag of channels: {count}")
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
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    count = config.STORE[task_store].delete_channels(
        with_tag=task['with_tag'],
        without_tag=task['without_tag'],
        with_id=task['with_id'],
        with_name=task['with_name']
    )
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
    count = config.STORE[task_store].list_channels(with_tag=task['with_tag'], without_tag=task['without_tag'], verbose=task['verbose'])
    print(f"list {count} channels.")
    return True


def play_command_sort_channels(task):
    """Play command sort channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    result = config.STORE[task_store].sort_channels(
        sort_key1=task['sort_key1'],
        sort_key2=task['sort_key2']
    )
    if result:
        print(f"sorted channels with key1: {task['sort_key1']}, key2: {task['sort_key2']}.")
    else:
        print("ERROR: sorted channels failed.")
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


def play_command_copy_channels(task):
    """Play command copy channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    to_store = task['to_store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    if to_store not in config.STORE:
        config.STORE[to_store] = ProbeInfoList()
    count = config.STORE[task_store].copy_channels(
        with_tag=task['with_tag'],
        without_tag=task['without_tag'],
        with_id=task['with_id'],
        with_name=task['with_name'],
        to_store=config.STORE[to_store]
    )

    print(f"copy {count} channels.")
    return True


def play_command_move_channels(task):
    """Play command move channels.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    task_store = task['store']
    to_store = task['to_store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    if to_store not in config.STORE:
        config.STORE[to_store] = ProbeInfoList()
    count = config.STORE[task_store].copy_channels(
        with_tag=task['with_tag'],
        without_tag=task['without_tag'],
        with_id=task['with_id'],
        with_name=task['with_name'],
        to_store=config.STORE[to_store]
    )

    config.STORE[task_store].delete_channels(
        with_tag=task['with_tag'],
        without_tag=task['without_tag'],
        with_id=task['with_id'],
        with_name=task['with_name']
    )
    print(f"moved {count} channels.")
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


def play_command_select_copy(task):
    """Play command select and copy.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    temp_tag = 'select_copy_tmp'
    task_store = task['store']
    to_store = task['to_store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    if to_store not in config.STORE:
        config.STORE[to_store] = ProbeInfoList()
    count = config.STORE[task_store].select(
        with_tag=task['with_tag'],
        without_tag=task['without_tag'],
        tvg_group_title=task['group_title'],
        tvg_name=task['name'],
        tvg_id=task['id'],
        tvg_source=task['source'],
        set_tag=temp_tag, quiet=True)

    config.STORE[task_store].copy_channels(
        with_tag=temp_tag,
        to_store=config.STORE[to_store]
    )
    tmp_task = {'store': task_store, 'all_stores': 'yes', 'tag': temp_tag}
    play_command_clear_tag(tmp_task, quiet=True)

    print(f"selected and copied {count} channels.")
    return True


def play_command_select_move(task):
    """Play command select and move.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    temp_tag = 'select_copy_tmp'
    task_store = task['store']
    to_store = task['to_store']
    if task_store not in config.STORE:
        config.STORE[task_store] = ProbeInfoList()
    if to_store not in config.STORE:
        config.STORE[to_store] = ProbeInfoList()
    count = config.STORE[task_store].select(
        with_tag=task['with_tag'],
        without_tag=task['without_tag'],
        tvg_group_title=task['group_title'],
        tvg_name=task['name'],
        tvg_id=task['id'],
        tvg_source=task['source'],
        set_tag=temp_tag, quiet=True)

    config.STORE[task_store].copy_channels(
        with_tag=temp_tag,
        to_store=config.STORE[to_store]
    )
    config.STORE[task_store].delete_channels(
        with_tag=temp_tag
    )
    tmp_task = {'store': task_store, 'all_stores': 'yes', 'tag': temp_tag}
    play_command_clear_tag(tmp_task, quiet=True)

    print(f"selected and moved {count} channels.")
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
        config.STORE[task_store].probe_scan(
            with_tag=task['with_tag'],
            without_tag=task['without_tag'],
            with_id=task['with_id'],
            with_name=task['with_name'],
            delay=delay
        )
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


def play_command_list_stores(task):
    """Play command list groups.

    Args:
        task: task array

    Returns:
        Good: boolean
    """
    from .probe_list import ProbeInfoList

    for i in config.STORE:
        my_store=config.STORE[i]
        count=my_store.count_channels()
        groups = my_store.list_groups()
        print(f"{i}: {count} channels, {len(groups)} groups.")
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
    "run_tasks": {
        "args": [
            {"name": "file"},
            {"name": "include_tag", "default": ""},
            {"name": "exclude_tag", "default": ""}
        ],
        "func": play_command_run_tasks,
        "help": "run tasks from yaml task file."
    },
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
    "list_stores": {
        "args": [],
        "func": play_command_list_stores,
        "help": "list stores."
    },
    "group_channels": {
        "args": [{"name": "store", "help": "store name", "default": "default"},{"name": "group"}],
        "func": play_command_group_channels,
        "help": "list channels for a group."
    },
    "probe_scan": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "delay", "help": "delay between probing channels", "default": "5"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "with_id", "default": ""},
            {"name": "with_name", "default": ""}
        ],
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
    "clear_tag": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "tag"},
            {"name": "all_stores", "default": "", "help": "set with any value to remove tags from every store."}
        ],
        "func": play_command_clear_tag,
        "help": "clear tag from every channel in store (or all stores)."
    },
    "delete_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "with_id", "default": ""},
            {"name": "with_name", "default": ""},
        ],
        "func": play_command_delete_channels,
        "loop": "channels",
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
    "copy_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "with_id", "default": ""},
            {"name": "with_name", "default": ""},
            {"name": "to_store"},
        ],
        "func": play_command_copy_channels,
        "loop": "channels",
        "help": "copy channels to other store (create store if not exists)."
    },
    "move_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "with_id", "default": ""},
            {"name": "with_name", "default": ""},
            {"name": "to_store"},
        ],
        "func": play_command_move_channels,
        "loop": "channels",
        "help": "move channels to other store (create store if not exists)."
    },
    "list_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "verbose", "default": "no", "help": "verbose: no or yes"},
        ],
        "func": play_command_list_channels,
        "help": "list channels."
    },
    "sort_channels": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "sort_key1", "default": "tvg_group_title", 'help': "sort key 1: tvg_id, tvg_name, tvg_logo, tvg_group_title"},
            {"name": "sort_key2", "default": "tvg_name", 'help': "sort key 2: tvg_id, tvg_name, tvg_logo, tvg_group_title"},
        ],
        "func": play_command_sort_channels,
        "help": "sort channels."
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
    },
    "select_and_copy": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "group_title", "default": ""},
            {"name": "name", "default": ""},
            {"name": "id", "default": ""},
            {"name": "source", "default": ""},
            {"name": "to_store"},
        ],
        "func": play_command_select_copy,
        "help": "select and copy channels."
    },
    "select_and_move": {
        "args": [
            {"name": "store", "help": "store name", "default": "default"},
            {"name": "with_tag", "default": ""},
            {"name": "without_tag", "default": ""},
            {"name": "group_title", "default": ""},
            {"name": "name", "default": ""},
            {"name": "id", "default": ""},
            {"name": "source", "default": ""},
            {"name": "to_store"},
        ],
        "func": play_command_select_move,
        "help": "select and move channels."
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
