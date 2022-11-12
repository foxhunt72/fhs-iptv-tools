import subprocess
import json
import hashlib
import os
from pathlib import Path
from .directories import get_probe_dir
from pprint import pprint


class ProbeInfo:
    def __init__(self, cmdpath="/usr/bin/ffprobe", seed="Pn2OOHXBFjnSqB.Yt", probedir=None):
        """Initiate class.

        Args:
            cmdpath: ffprobe command part
            seed: seed for sha1 function
            probedir: directory to cache probes info
        """
        self._cmdpath = cmdpath
        self._seed = seed
        self._probedir = probedir

    def process_media_info(self, media_info):
        """Cleanup and process media info.

        Args:
            media_info: probe info

        Returns:
            cleaned media_info
        """
        try:
            del media_info['format']['filename']
        except KeyError:
            pass
        return media_info

    def probe(self, source):
        """Probe a source.

        Args:
            source: source to probe

        Returns:
            mediainfo
        """
        cmd = [
            self._cmdpath,
            "-loglevel",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            "-show_error",
            "-show_packets",
            "-count_frames",
            "-read_intervals",
            "%+10",
            "-i",
            source,
        ]  # maybe add -read_intervals  %+10
        try:
            outputBytes = subprocess.check_output(cmd)
        except subprocess.CalledProcessError as e:
            self._last_error = str(e)
            return None

        outputText = outputBytes.decode("utf-8")
        try:
            ffprobe = json.loads(outputText)
        except json.JSONDecodeError as e:
            self._last_error = str(e)
            return None
        return self.process_media_info(ffprobe)

    def get_cache_path(self, source):
        """Get cache path.

        Args:
            source: source to create path from

        Returns:
            path
        """
        if self._probedir is None:
            self._probedir = get_probe_dir()

        hash_string = f"{source}_{self._seed}"
        hash_object = hashlib.sha1(hash_string.encode())
        return os.path.join(self._probedir, f"{hash_object.hexdigest()}.json")

    def load_cache_source(self, source):
        """Get cached probe

        Args:
            source: source to get cache from

        Returns:
            mediainfo
        """
        probe_file = self.get_cache_path(source)
        try:
            with Path(probe_file).open(encoding="UTF-8") as source:
                media_info = json.load(source)
        except FileNotFoundError:
            media_info = None
        return media_info

    def save_cache_source(self, source, media_info):
        """Save probe to cache.

        Args:
            source: source to get cache from
            media_info: probe_info to cache

        Returns:
            Success
        """
        probe_file = self.get_cache_path(source)
        with Path(probe_file).open("w", encoding="UTF-8") as target:
            json.dump(media_info, target)
        return True

    def probe_with_cache(self, source):
        """Probe a source cache to or from disk.

        Args:
            source: source to probe

        Returns:
            mediainfo
        """
        media_info = self.load_cache_source(source)
        if media_info is not None:
            media_info['fhs_source'] = 'cache'
            return media_info

        media_info = self.probe(source)
        if media_info is not None:
            self.save_cache_source(source, media_info)
            media_info['fhs_source'] = 'ffprobe'
        return media_info
 
    def calculate_bitrate(self, media_info, stream):
        """Calculate bitrate.

        Args:
            media_info: ffprobe info
            stream: stream id to check

        Returns:
            calculated bitrate
        """
        total_size = 0
        total_time = float()
        for packet in media_info['packets']:
            if packet['stream_index'] != stream:
                continue
            total_size += int(packet['size'])
            total_time += float(packet.get('duration_time', 0))
        try:
            bitrate = int(((total_size * 8) / total_time))
        except ZeroDivisionError:
            return -1
        return bitrate

    def swap_video_and_audio_in_list(self, result):
        """Reverse list is list consist of audio / video and not video / auto.

        Args:
            result: list of results

        Returns:
            list in order video / audio
        """
        if len(result) != 2:
            return result  # more or less than 2 entries
        if 'audio' in result[0] and 'video' in result[1]:
            result.reverse()
        return result

    def info2str_and_dict(self, media_info):
        """Convert media info to info str.

        Args:
            media_info: ffprobe info

        Returns:
            media_str
        """
        result = []
        dict_result = {}
        for idx, p in enumerate(media_info['streams']):
            codec_type = p.get('codec_type', 'unknown')
            if 'bit_rate' in p:
                bit_rate = p['bit_rate']
            else:
                bit_rate = self.calculate_bitrate(media_info, idx)
            dict_result[codec_type]={
                'codec': p.get('codec_name','codec unknown'),
                'bit_rate': int(bit_rate)
            }
            if codec_type == 'video':
                result.append(f"video: {p.get('codec_name','codec unknown')} bit_rate: {bit_rate} / width: {p.get('width', 'unknown')} / height: {p.get('height', 'unknown')}")  # noqa: E501
                dict_result[codec_type]['with'] = int(p.get('width', -1))
                dict_result[codec_type]['height'] = int(p.get('height', -1))
            if codec_type == 'audio':
                result.append(f"audio: {p.get('codec_name','codec unknown')} bit_rate: {bit_rate}")  # noqa: E501
        result = self.swap_video_and_audio_in_list(result)
        return (", ".join(result), dict_result)
