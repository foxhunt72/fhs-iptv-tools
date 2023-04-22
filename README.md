fhs\_iptv\_tools
================

Iptv Tools Version: 0.8.12
--------
#### ** For changes see** [changelog](https://github.com/foxhunt72/fhs-iptv-tools/blob/main/CHANGELOG.md).

## Foxhunt Software IPTV Tools

Making iptv easier

## Index

- [Main features](#main-features)
- [Future features](#future-features)
- [Usage](#usage)
- [Examples](#examples)
- [Installation](#installation)
- [Requirements](#requirements)
- [License](#license)
- [Author](#author)

## Main features

- load any m3u
- remove unused channels
- join multipe m3u files
- edit channels
- scan/probe streams/channels (get resolution, codec and bitrate for channels
- save new m3u file
- do this all interactive
- or run this all automatic with a yaml 

## Future features

- select on codec / bitrate / resolution
- clean probe/scan check
- clean interactive history file (max lines)


Thanks to:
----------

For inspiration and some code
-   <https://github.com/cmcconomy/iptv-filter.git>

## Usage
-----

```shellscript

 # use it with docker like this
 docker run --rm -h fhs-iptv-tools -t -i rdevos72/fhs-iptv-tools --help

 fhs-iptv-tools interactive

 # load m3u file from disk
 (fhs_iptv_tools) load_m3u --file=./m3u

 # count channels, it you want to know, you can also list_channels, list_groups, and more.
 (fhs_iptv_tools) count_channels

 # select channels based on text in group title, more options are on name, id and more see help.
 (fhs_iptv_tools) select --group_title "NL" --set_tag keep
 selected 6 channels.

 # modified the channels, change to group to NL
 (fhs_iptv_tools) modify_channels --with_tag keep --set_group_title NL

 # delete all the channels we didn't tag with the select command.
 (fhs_iptv_tools) delete_channels --without_tag keep
 removed 15 channels.

 # sort all channels
 sort_channels --sort_key1 tvg_group_title --sort_key2 tvg_name

 # probe channels
 probe_scan

 # and save to m3u file, the the delete is not realy needed you can also use --with_tag keep in the save action.
 (fhs_iptv_tools) save_m3u --file m3u.new
 channels saved to m3u file m3u.new

 # save everything you did so that you can repeat it automatically
 (fhs_iptv_tools) save_tasks --file=/tmp/tasks.yaml

 # then run it as
 fhs-iptv-tools run-tasks --yaml-command /tmp/tasks.yaml


 # In interactive mode, try 
 (fhs_iptv_tools) help

 # And try the command with --help to see the options
 (fhs_iptv_tools) select --help
 Usage: select [-h] [--store STORE] [--with_tag WITH_TAG] [--without_tag WITHOUT_TAG]
              [--group_title GROUP_TITLE] [--name NAME] [--id ID] [--source SOURCE] [--set_tag SET_TAG]
              [--clear_tag CLEAR_TAG]

 optional arguments:
  -h, --help            show this help message and exit
  --store STORE         store name
  --with_tag WITH_TAG
  --without_tag WITHOUT_TAG
  --group_title GROUP_TITLE
  --name NAME
  --id ID
  --source SOURCE
  --set_tag SET_TAG
  --clear_tag CLEAR_TAG

```

## Installation
------------

``` {.bash}
git clone https://github.com/foxhunt72/fhs-iptv-tools
cd fhs-iptv-tools
pip3 install .

pipx install fhs_iptv_tools
or
pip3 install fhs_iptv_tools

# install ffprobe
```

##Requirements

- typer[all]
- cmd2
- jinja2
- appdirs

## Compatibility
-------------

## Examples
-----------

- [loop.tasks](https://github.com/foxhunt72/fhs-iptv-tools/blob/main/Examples/loop.tasks).

## Licence
-------

MIT license

## Author
-------

Richard de Vos

[fhs_iptv_tools](https://github.com/foxhunt72/fhs-iptv-tools) was written by [Richard de Vos](rdevos72@gmail.com).
