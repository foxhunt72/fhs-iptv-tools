"""Playyaml file."""

import os
import sys

import yaml

from . import config
from pprint import pprint


def check_console():
    """Check if CONFIG.console is not none."""
    if config.CONSOLE is None:
        from rich.console import Console

        config.CONSOLE = Console()


def check_items_in_2_lists(list1, list2):
    """Check items in 2 lists returns True in at least one item matches.

    Args:
        list1: list of strings
        list2: list of strings

    Returns:
        bool: minimal one item matched
    """
    for i in list1:  # noqa:SIM110
        if i in list2:
            return True
    return False


def load_yaml(filename):
    """Load yaml file from disk.

    Args:
        filename: file to load

    Returns:
        struct from yaml file
    """
    try:
        with open(os.path.expanduser(filename), "r") as file:
            data = yaml.safe_load(file)
    except Exception as e:  # noqa:B902
        sys.stderr.write(f"can't open config file: {filename}  {e}")
        exit(1)
    return data


def check_arguments_in_task(task, command_dict):
    """Check arguments in task.

    Args:
        task: task array
        command_dict: command_dict array

    Returns:
        Boolean arguments correct
    """
    if 'args' not in command_dict:
        # no arguments needed for this functions
        return True
    for arg in command_dict['args']:
        argname = arg.get("name", "unknown_name")
        arghelp = arg.get("help", None)
        argdefault = arg.get("default", None)
        if argname in task:
            continue
        if argdefault is not None:
            task[argname] = argdefault
            continue
        # so if here we are missing a argname without a default so mandatoy
        sys.stderr.write(f"ERROR: missing argument {argname} for {arghelp or '<No Help>'} in {str(task)}")
        return False
    return True


def task_check_tag(task, include_tags=None, exclude_tags=None):
    """Check if the task have a tag and if we skip or not this task.

    Args:
        task: task array
        include_tags: list of tags to run
        exclude_tags: list of tags to skip

    Returns:
        RunTask: boolean, True run task, False skip task
    """
    temp_tags = task.get("tags", [])
    tags = temp_tags if isinstance(temp_tags, list) else [temp_tags]

    if include_tags is not None and include_tags != []:  # noqa: SIM102
        # check is include tags in in tags of this task, if false then skip this task
        if check_items_in_2_lists(include_tags, tags) is False:
            return False

    if exclude_tags is not None and exclude_tags != []:  # noqa: SIM102
        # check is exclude tags in in tags of this task, if true then skip this task
        if check_items_in_2_lists(exclude_tags, tags) is True:
            return False

    return True


def play_task(task, *, include_tags=None, exclude_tags=None, funcdict):
    """Play a task.

    Args:
        task: task array
        include_tags: list of tags to run
        exclude_tags: list of tags to skip

    Returns:
        Good: boolean
    """
    check_console()
    task_name = task.get('name', task.get('command', 'unknown'))
    if task_check_tag(task, include_tags=include_tags, exclude_tags=exclude_tags):
        print(f"running task: {task_name}")
    else:
        print(f"skipping task: {task_name}")
        return True

    if "command" not in task:
        sys.stderr.write(f"missing command entry in task {str(task)}")
        exit(3)

    command_dict=funcdict.get(task["command"], None)
    if command_dict is None:
        print("unknown task:  {task['command']}")
        pprint(task)
        return True

    if check_arguments_in_task(task, command_dict) is False:
        print("missing arguments in task.")
        exit(1)

    if 'func' in command_dict:
        command_dict['func'](task)
    return True


def play(commandfile, *, include_tags=None, exclude_tags=None, funcdict):
    """Play commandfile.

    Args:
        commandfile: yaml file with instructions
        include_tags: list of tags to run
        exclude_tags: list of tags to skip
        funcdict: dicts with options

    Returns:
        None
    """
    check_console()
    data = load_yaml(commandfile)

    if "tasks" not in data:
        sys.stderr.write("missing tasks entrie in yaml file")
        exit(2)

    for task in data["tasks"]:
        play_task(task, include_tags=include_tags, exclude_tags=exclude_tags, funcdict=funcdict)

    return None
