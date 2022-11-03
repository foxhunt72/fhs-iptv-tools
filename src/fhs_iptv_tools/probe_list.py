# probe source

from .probe import ProbeInfo
from .import_m3u import import_m3u_file, return_tvg_group_titles, M3uChannel
from enum import Enum
import time


class LoadType(Enum):
    """LoadTypes from loading m3u channels."""

    ALL = 0
    CHANNELS = 1
    VOD = 2


class ProbeInfoList:
    def __init__(self):
        """Initiate class."""
        self.__probe = ProbeInfo()
        self.__m3u_channels = list()

    def write_error(self, msg):
        """Write error message.

        Args:
            msg: error message
        """
        print(f"ERROR: {msg}")

    def load_m3u_file(self, m3u_file):
        """Load a m3u file.

        Args:
            m3u_file: file to load

        Returns:
            list op m3uchannels
        """
        self.__m3u_channels = import_m3u_file(m3u_file)
        if self.__m3u_channels == None:
            self.write_error(f"can't load m3u_file: {m3u_file}")
        return self.__m3u_channels

    def filter_lijst(self, filter_type):
        """Filter the list based on filter_type.

        Args:
            filter_type: type of LoadType

        Returns:
            filtered list of type.
        """
        include_vod = None
        if filter_type == LoadType.ALL:
            return self.__m3u_channels

        if filter_type == LoadType.CHANNELS:
            include_vod = False

        if filter_type == LoadType.VOD:
            include_vod = True

        if include_vod is None:
            self.write_error(f"unknown type: {filter_type=}")
            return None

        result = list(filter(lambda d: d.vod is include_vod, self.__m3u_channels))
        self.__m3u_channels = result
        return self.__m3u_channels

    def probe_scan(self, delay=5, status_output=None):
        """Probe a m3u file.

        Args: 
            delay: delay between channels.
            status_output: function to output status

        Returns:
            Status: None
        """
        max_len = 10
        for ch in self.__m3u_channels:
            if len(ch.tvg_name) > max_len:
                max_len = len(ch.tvg_name)
        max_len += 3
        for ch in self.__m3u_channels:
            if status_output is not None:
                status_output(f"starting scanning: {ch.tvg_name}")
            if type(ch.tvg_sources) == list:
                for source in ch.tvg_sources:
                    result = self.__probe.probe_with_cache(source)
            else:
                result = self.__probe.probe_with_cache(ch.tvg_sources)
            if result is None:
                if status_output is not None:
                    status_output(f"no result for: {ch.tvg_name}")
                continue

            if status_output is not None:
                status_output(f"ready scanning: {ch.tvg_name}")
            ch.fhs_info = self.__probe.info2str(result)
            print(f"{ch.tvg_name:{max_len}}:\t{ch.fhs_info}")
            if result.get('fhs_source', 'unknown') != 'cache':
                time.sleep(delay)

        return None

    def count_channels(self):
        """Count the channels.

        Returns:
            count of channels
        """
        return len(self.__m3u_channels)

    def list_groups(self, vod_only=False):
        """List the groups.

        Args:
            vod_only: show vod only

        Returns:
            list of groups
        """
        groups = return_tvg_group_titles(self.__m3u_channels, vod_only)
        return groups

    def group_channels(self, group):
        """List the channels in a group.

        Args:
            group: show vod only

        Returns:
            list of channels
        """
        channels = []
        for ch in self.__m3u_channels:
            if ch.tvg_group_title == group:
                channels.append(ch)
        return channels

    def add_channel(self, *, tvg_id, tvg_name, tvg_logo, tvg_group_title, tvg_source):
        """List the channels in a group.

        Args:
            group: show vod only

        Returns:
            list of channels
        """
        self.__m3u_channels.append(M3uChannel(tvg_id=tvg_id, tvg_name=tvg_name.strip(), tvg_logo=tvg_logo, tvg_group_title=tvg_group_title))
        self.__m3u_channels[-1].tvg_sources.append(tvg_source)

    def select(self, *, with_tag="", without_tag="", tvg_group_title="", tvg_name="", tvg_id="", tvg_source="", set_tag="", clear_tag=""):
        """Select channel.

        If multiple filters are used than it is a 'AND'

        Args:
            with_tag: select on tag set
            without_tag: select on tag not set
            tvg_id: select based on tvg_id
            tvg_group_title: select in group_title
            tvg_name: select in tvg_name
            tvg_source: select on source url
            set_tag: set tag
            clear_tag: remove tag

        Returns:
            count, amount of
        """
        from .utils import check_search_filter_in_string

        if set_tag == "" and clear_tag == "":
            self.write_error("ERROR: select needs to set a tag or remove a tag.")
            return -1

        count = 0
        for ch in self.__m3u_channels:
            # check if tag is precent
            if with_tag != "" and with_tag not in ch.fhs_tags:
                continue

            # check if tag is not precent
            if without_tag != "" and without_tag in ch.fhs_tags:
                continue

            if tvg_id != "" and check_search_filter_in_string(ch.tvg_id, tvg_id) is False:
                continue

            if tvg_group_title != "" and check_search_filter_in_string(ch.tvg_group_title, tvg_group_title) is False:
                continue

            if tvg_name != "" and check_search_filter_in_string(ch.tvg_name, tvg_name) is False:
                continue

            if tvg_source != "":
                self.write_error(f"ERROR: tvg_source not implemented: {tvg_source}.")
            count += 1
            if set_tag != "":
                ch.fhs_tags.add(set_tag)
            if clear_tag != "":
                try:
                    ch.fhs_tags.remove(set_tag)
                except KeyError:
                    pass
        return count

    def delete_channels(self, *, with_tag="", without_tag=""):
        """Delete channels.

        Delete channels

        Args:
            with_tag: select on tag set
            without_tag: select on tag not set

        Returns:
            count, amount of
        """

        if with_tag == "" and without_tag == "":
            self.write_error("delete_channel needs with_tag or without_tag set.")
            return -1

        count = 0
        for p in range(len(self.__m3u_channels), 0, -1):
            if with_tag != "" and with_tag in self.__m3u_channels[p - 1].fhs_tags:
                del self.__m3u_channels[p - 1]
                count += 1
                continue
            if without_tag != "" and without_tag not in self.__m3u_channels[p - 1].fhs_tags:
                del self.__m3u_channels[p - 1]
                count += 1
                continue
        return count
