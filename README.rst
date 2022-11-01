fhs_iptv_tools
==============


foxhunt software iptv tools, making iptv easier

Initial version, docs need to go, for now

- load m3u file
- probe stream sources
- run tasks from script
- use interactive mode


Usage
-----

.. code-block:: bash
   
   fhs-iptv-tools interactive
   (fhs_iptv_tools) load_m3u --file=./m3u
   (fhs_iptv_tools) count_channels
   (fhs_iptv_tools) save_tasks --file=/tmp/tasks.yaml

   # then run it as
   fhs-iptv-tools run-tasks --yaml-command /tmp/tasks.yaml


Installation
------------

.. code-block:: bash

  git clone https://github.com/foxhunt72/fhs-iptv-tools
  cd fhs-iptv-tools
  pip3 install .

  pipx install fhs_iptv_tools
  or
  pip3 install fhs_iptv_tools


Requirements
^^^^^^^^^^^^
- typer[all]
- cmd2
- jinja2
- appdirs

Compatibility
-------------

Licence
-------
MIT license

Authors
-------
Richard de Vos

`fhs_iptv_tools` was written by `Richard de Vos <rdevos72@gmail.com>`_.
