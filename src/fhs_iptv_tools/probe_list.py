# probe source

from .probe import ProbeInfo
from .import_m3u import import_m3u_file, return_tvg_group_titles, M3uChannel
from enum import Enum
import time
import copy
from pprint import pprint


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

    def probe_channel(self, *, channel, status_output, max_len=40, delay=5):
        """Probe a channel.

        Args:
            channel: channel array
            status_output: function to output status
            max_len: max len for tvg_name
            delay: sleep delay after scan
        """
        if status_output is not None:
            status_output(f"starting scanning: {channel.tvg_name}")
        if type(channel.tvg_sources) == list:
            for source in channel.tvg_sources:
                result = self.__probe.probe_with_cache(source)
        else:
            result = self.__probe.probe_with_cache(channel.tvg_sources)
        if result is None:
            if status_output is not None:
                status_output(f"no result for: {channel.tvg_name}")
            return

        if status_output is not None:
            status_output(f"ready scanning: {channel.tvg_name}")
        (channel.fhs_info, channel.fhs_dict) = self.__probe.info2str_and_dict(result)
        print(f"{channel.tvg_name:{max_len}}:\t{channel.fhs_info}")
        if result.get('fhs_source', 'unknown') != 'cache':
            time.sleep(delay)
        return



    def probe_scan(self, *, delay=5, status_output=None, with_tag="", without_tag="", with_id="", with_name=""):
        """Probe a m3u file.

        Args:
            delay: delay between channels.
            status_output: function to output status
            with_tag: select on tag set
            without_tag: select on tag not set
            with_id: change only on id
            with_name: change only when name is the same

        Returns:
            Status: None
        """
        max_len = 10
        channels = list(self.get_channels(
            with_tag=with_tag, without_tag=without_tag, with_id=with_id, with_name=with_name))
        print(f"channels: {len(channels)}")
        for ch in channels:
            if len(ch.tvg_name) > max_len:
                max_len = len(ch.tvg_name)
        max_len += 3
        for ch in channels:
            self.probe_channel(channel=ch, status_output=status_output, max_len=max_len, delay=delay)
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
        """Add channel.

        Args:
            tvg_id: channel id
            tvg_name: channel name
            tvg_logo: url to channel logo
            tvg_group_title: channel group
            tvg_source: channel source

        Returns:
            list of channels
        """
        self.__m3u_channels.append(M3uChannel(tvg_id=tvg_id, tvg_name=tvg_name.strip(), tvg_logo=tvg_logo, tvg_group_title=tvg_group_title))
        self.__m3u_channels[-1].tvg_sources.append(tvg_source)
        return self.__m3u_channels

    def add_channel_struct(self, channel):
        """Add channel by struct.

        Args:
            channel: channel struct to add

        Returns:
            list of channels
        """
        self.__m3u_channels.append(channel)
        return self.__m3u_channels

    def select(self, *, with_tag="", without_tag="", tvg_group_title="", tvg_name="", tvg_id="", tvg_source="", set_tag="", clear_tag="", quiet=False):
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
            if quiet is False:
                print(f"{count}: {ch.tvg_name}     /   {ch.tvg_group_title}")
        return count

    def delete_channels(self, *, with_tag="", without_tag="", with_id="", with_name=""):
        """Delete channels.

        Delete channels

        Args:
            with_tag: select on tag set
            without_tag: select on tag not set

        Returns:
            count, amount of
        """

        if with_tag == "" and without_tag == "" and with_id == "" and with_name == "":
            self.write_error("delete_channel needs with_tag, without_tag, with_id or with_name set.")
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
            if with_id != "" and with_id==self.__m3u_channels[p - 1].tvg_id:
                del self.__m3u_channels[p - 1]
                count += 1
                continue
            if with_name != "" and with_name==self.__m3u_channels[p - 1].tvg_name:
                del self.__m3u_channels[p - 1]
                count += 1
                continue
        return count

    def get_channels(self, *, with_tag="", without_tag="", with_id="", with_name=""):
        """Get channels.

        Get channels

        Args:
            with_tag: select on tag set
            without_tag: select on tag not set
            with_id: select on id
            with_name: select on name

        Returns:
            yield of channels
        """

        for ch in self.__m3u_channels:
            if with_id != "" and ch.tvg_id != with_id:
                continue
            if with_name != "" and ch.tvg_name != with_name:
                continue
            if with_tag != "" and with_tag not in ch.fhs_tags:
                continue
            if without_tag != "" and without_tag in ch.fhs_tags:
                continue
            yield ch

    def clear_tag(self, *, tag):
        """Clear tag.

        Args:
            tag: tag to clear

        Returns:
            count: amount of tags removed
        """
        count = 0
        for ch in self.__m3u_channels:
            try:
                ch.fhs_tags.remove(tag)
                count += 1
            except KeyError:
                pass
        return count

    def display_channel(self, channel, *, extra=None):
        """Display channel.

        Args:
            channel: m3uchannel to display
            extra: what extra info to show, future use

        Returns:
            str:channel descriptions as string
        """
        tags = ", ".join(channel.fhs_tags)
        if tags != "":
            display_tags = f" tags: {tags}"
        else:
            display_tags = ""
        return f"<{channel.tvg_id}> {channel.tvg_name}   /   {channel.tvg_group_title}{display_tags}"

    def list_channels(self, *, with_tag="", without_tag="", verbose="no"):
        """List channels.

        List channels

        Args:
            with_tag: select on tag set
            without_tag: select on tag not set
            verbose: verbose output no or yes

        Returns:
            yield of channels
        """

        count = 0
        for ch in self.get_channels(with_tag=with_tag, without_tag=without_tag):
            count += 1
            print(f"{count}: {self.display_channel(ch)}")
            if verbose == 'yes':
                pprint(ch)
        return count

    def save_m3u_file(self, *, file, with_tag="", without_tag=""):
        """List channels.

        List channels

        Args:
            file: filename to save
            with_tag: select on tag set
            without_tag: select on tag not set
        """
        from .import_m3u import export_m3u_file

        channels = self.get_channels(with_tag=with_tag, without_tag=without_tag)
        if export_m3u_file(file, channels) is False:
            print(f"save failed to file: {file}.")
        print(f"channels saved to m3u file {file}")

    def modify_channels(self, *, with_tag="", without_tag="", with_id="", set_id="", set_name="", set_group_title="", set_logo=""):
        """Modify channel.

        Args:
            with_tag: select on tag set
            without_tag: select on tag not set
            with_id: change only on id
            set_id: set new id
            set_name: set_name
            set_group_title: set group title
            set_logo: set logo

        Returns:
            count: channels changed.
        """
        channels = self.get_channels(with_tag=with_tag, without_tag=without_tag, with_id=with_id)
        if set_id != "" or set_name != "" or set_logo != "":
            # this modifications we do only on one channel at a time.
            channels = list(channels)
            if len(channels) != 1:
                self.write_error(f"ERROR: you can only change this type one channel on a time and not for {len(channels)}")
                return -1
        count = 0
        for ch in channels:
            count += 1
            if set_id != "":
                ch.tvg_id = set_id
            if set_name != "":
                ch.tvg_name = set_name
            if set_group_title != "":
                ch.tvg_group_title = set_group_title
            if set_logo != "":
                ch.tvg_logo = set_logo
        return count

    def copy_channels(self, *, with_tag="", without_tag="", with_id="", with_name="", to_store):
        """Copy channel to store.

        Args:
            with_tag: select on tag set
            without_tag: select on tag not set
            with_id: change only on id
            with_name: change only when name is the same
            to_store: store to copy to

        Returns:
            count: channels changed.
        """
        channels = self.get_channels(with_tag=with_tag, without_tag=without_tag, with_id=with_id, with_name=with_name)
        count = 0
        for ch in channels:
            count += 1
            # create a copy of the structure with copy.copy
            to_store.add_channel_struct(copy.copy(ch))
            print(f"copied {ch.tvg_name}")
        return count

    def sort_channels(self, *, sort_key1="", sort_key2=""):
        """Sort channels.

        Args:
            sort_key1: first key to sort on
            sort_key2: second key to sort on

        Returns:
            result: boolean
        """
        if self.__m3u_channels == []:
            return True
        try:
            getattr(self.__m3u_channels[0], sort_key1)
        except AttributeError as e:
            print(f"ERROR: sortkey 1 not found: {e}")
            return False

        if sort_key2 == "":
            sort_key2 = sort_key1
        try:
            getattr(self.__m3u_channels[0], sort_key2)
        except AttributeError as e:
            print(f"ERROR: sortkey 2 not found: {e}")
            return False

        def sorted_key(m3u_info):
            return (getattr(m3u_info, sort_key1), getattr(m3u_info, sort_key2))

        self.__m3u_channels.sort(key=sorted_key)
        return True
