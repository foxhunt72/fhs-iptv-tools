"""Import m3u files."""

import re
from dataclasses import dataclass, field
from .subgroup import subgroup_vod_only
from enum import Enum


class ChannelType(Enum):
    """Channeltypes for M3uChannel."""

    UNKNOWN = 0
    CHANNEL = 1
    EPISODE = 2
    MOVIE = 3


@dataclass
class M3uChannel:
    """Class for M3uChannel."""

    tvg_id: str
    tvg_name: str
    tvg_logo: str
    tvg_group_title: str
    vod: bool = False
    tvg_sources: list = field(default_factory=list)
    tvg_type: ChannelType = ChannelType.UNKNOWN
    fhs_selected: bool = False
    fhs_tags: set = field(default_factory=set)
    fhs_dict: dict = field(default_factory=dict)


def import_m3u_stream(input_str):
    """Import m3u stream.

    Args:
        input_str: file handler to read

    Returns:
        list of m3uchannel
    """
    m3uchannels = []
    # regex found on iptv-filter
    infopattern = re.compile('(?i)#EXTINF:-1 tvg-id="(.*?)" tvg-name="(.*?)" tvg-logo="(.*?)" group-title="(.*?)",(.*?)')  # noqa: E501,BLK100
    urlpattern = re.compile('(?i)^http')
    for line in input_str:
        clean_line = line.rstrip()
        m = infopattern.findall(clean_line)
        if len(m) > 0:
            # #EXTINF line
            tvg_id = m[0][0]
            tvg_name = m[0][1]
            tvg_logo = m[0][2]
            tvg_group_title = m[0][3]
            m3uchannels.append(M3uChannel(tvg_id=tvg_id, tvg_name=tvg_name.strip(), tvg_logo=tvg_logo, tvg_group_title=tvg_group_title.strip()))  # noqa: E501
        else:
            if urlpattern.match(clean_line):
                # This is the URL Line
                m3uchannels[-1].tvg_sources.append(clean_line)
                if clean_line.endswith(('.mkv', '.avi', '.mp4')) is True:
                    m3uchannels[-1].vod = True
    if len(m3uchannels) == 0:
        return None
    return m3uchannels


def import_m3u_file(m3u_file):
    """Import m3u_file.

    Args:
        m3u_file: path to m3u file with channels/vod

    Returns:
        returns list op channnels/vods
    """
    try:
        with open(m3u_file, 'r') as input_stream:
            return (import_m3u_stream(input_stream))
    except FileNotFoundError:
        print(f"file {m3u_file} not found.")
    return None


def export_m3u_file(m3u_file, m3u_channels):
    """Export to m3u file from channels.

    Args:
        m3u_file: path to m3u file to write
        m3u_channels: channels to save to file.

    Returns:
        Result
    """
    try:
        with open(m3u_file, "w") as output_stream:
            print("#EXTM3U", file=output_stream)
            for ch in m3u_channels:
                print(f'#EXTINF:-1 tvg-id="{ch.tvg_id}" tvg-name="{ch.tvg_name}" tvg-logo="{ch.tvg_logo}" group-title="{ch.tvg_group_title}",{ch.tvg_name}', file=output_stream)  # noqa: E501
                for source in ch.tvg_sources:
                    print(source, file=output_stream)
    except PermissionError:
        print('ERROR: no permission.')
        return False
    except OSError as e:
        print(f"ERROR: oserror {e}")
        return False
    return True


def return_tvg_group_titles(m3u_channels, vod_only=False):
    """Extract group titles from m3u_channgels.

    Args:
        m3u_channels: list of M3uChanngels dataclasses
        vod_only: boolean of only wants to return vod rules

    Returns:
        list of group titles
    """
    tvg_groups = set()
    if vod_only is True:
        channels = subgroup_vod_only(m3u_channels)
    else:
        channels = m3u_channels
    for ch in channels:
        tvg_groups.add(ch.tvg_group_title)
    return sorted(tvg_groups)


def serie_regex():
    """Get compiled serie regex.

    Returns:
        Compiled regex
    """
    return re.compile('(.*?) S(\d+) {0,1}E(\d+)')  # noqa: W291,W605


def check_type_channel(m3u_channel, compiled_regex=None):
    """Check the channel type.

    Args:
        m3u_channel: Channel M3uChannel dataclass
        compiled_regex: optional re.compile regex

    Returns:
        ChannelType value

    """
    if compiled_regex is None:
        compiled_regex = serie_regex()

    if m3u_channel.vod is False:
        return ChannelType.CHANNEL
    if compiled_regex.findall(m3u_channel.tvg_name):
        return ChannelType.EPISODE
    return ChannelType.MOVIE


def get_channel_types(m3u_channels):
    """Check types of channels.

    Args:
        m3u_channels: List of M3uChannel dataclass

    Returns:
        list of m3u_channels
    """
    compiled_regex = serie_regex()
    result = []
    for i in m3u_channels:
        if i.tvg_sources == []:
            continue
        value = check_type_channel(i, compiled_regex)
        i.tvg_type = value
        # print(f"{i.tvg_name}: {i.tvg_sources[0]} / {i.tvg_type}")
        result.append(i)
    return result


def return_tvg_group_details(m3u_channels, vod_only=False):
    """Extract group titles from m3u_channgels.

    Args:
        m3u_channels: list of M3uChanngels dataclasses
        vod_only: boolean of only wants to return vod rules

    Returns:
        list of group titles
    """
    tvg_groups = dict()
    if vod_only is True:
        channels = subgroup_vod_only(m3u_channels)
    else:
        channels = m3u_channels
    for ch in get_channel_types(channels):
        group_info = tvg_groups.get(ch.tvg_group_title, {'channels': 0, 'episodes': 0, 'movies': 0})
        if ch.tvg_type == ChannelType.CHANNEL:
            group_info['channels'] += 1
        if ch.tvg_type == ChannelType.EPISODE:
            group_info['episodes'] += 1
        if ch.tvg_type == ChannelType.MOVIE:
            group_info['movies'] += 1
        tvg_groups[ch.tvg_group_title] = group_info
    return tvg_groups
