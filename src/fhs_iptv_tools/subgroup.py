"""Subgroup m3u"""

def subgroup_m3uchannels(m3uchannels, subgroup_name):
    """Subgroup m3u stream."""

    result = filter(lambda d: d.tvg_group_title == subgroup_name, m3uchannels)
    return result


def subgroup_vod_only(m3uchannels, include_vod=True):
    result = filter(lambda d: d.vod is include_vod, m3uchannels)
    return result

