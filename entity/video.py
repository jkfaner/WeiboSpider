#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:jkfaner
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/02/12 08:33:36
@Project:WeiboSpider
@File:Video.py
@Desc:
'''
from entity.base import BaseEntity


class Video(BaseEntity):

    def __init__(self):
        self._type = None
        self._mime = None
        self._protocol = None
        self._label = None
        self._url = None
        self._bitrate = None
        self._prefetch_range = None
        self._video_codecs = None
        self._fps = None
        self._width = None
        self._height = None
        self._size = None
        self._duration = None
        self._sar = None
        self._audio_codecs = None
        self._audio_sample_rate = None
        self._quality_label = None
        self._quality_class = None
        self._quality_desc = None
        self._audio_channels = None
        self._audio_sample_fmt = None
        self._audio_bits_per_sample = None
        self._watermark = None
        self._extension = None
        self._video_decoder = None
        self._prefetch_enabled = None
        self._tcp_receive_buffer = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def mime(self):
        return self._mime

    @mime.setter
    def mime(self, mime):
        self._mime = mime

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        self._protocol = protocol

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    @property
    def bitrate(self):
        return self._bitrate

    @bitrate.setter
    def bitrate(self, bitrate):
        self._bitrate = bitrate

    @property
    def prefetch_range(self):
        return self._prefetch_range

    @prefetch_range.setter
    def prefetch_range(self, prefetch_range):
        self._prefetch_range = prefetch_range

    @property
    def video_codecs(self):
        return self._video_codecs

    @video_codecs.setter
    def video_codecs(self, video_codecs):
        self._video_codecs = video_codecs

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, fps):
        self._fps = fps

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def sar(self):
        return self._sar

    @sar.setter
    def sar(self, sar):
        self._sar = sar

    @property
    def audio_codecs(self):
        return self._audio_codecs

    @audio_codecs.setter
    def audio_codecs(self, audio_codecs):
        self._audio_codecs = audio_codecs

    @property
    def audio_sample_rate(self):
        return self._audio_sample_rate

    @audio_sample_rate.setter
    def audio_sample_rate(self, audio_sample_rate):
        self._audio_sample_rate = audio_sample_rate

    @property
    def quality_label(self):
        return self._quality_label

    @quality_label.setter
    def quality_label(self, quality_label):
        self._quality_label = quality_label

    @property
    def quality_class(self):
        return self._quality_class

    @quality_class.setter
    def quality_class(self, quality_class):
        self._quality_class = quality_class

    @property
    def quality_desc(self):
        return self._quality_desc

    @quality_desc.setter
    def quality_desc(self, quality_desc):
        self._quality_desc = quality_desc

    @property
    def audio_channels(self):
        return self._audio_channels

    @audio_channels.setter
    def audio_channels(self, audio_channels):
        self._audio_channels = audio_channels

    @property
    def audio_sample_fmt(self):
        return self._audio_sample_fmt

    @audio_sample_fmt.setter
    def audio_sample_fmt(self, audio_sample_fmt):
        self._audio_sample_fmt = audio_sample_fmt

    @property
    def audio_bits_per_sample(self):
        return self._audio_bits_per_sample

    @audio_bits_per_sample.setter
    def audio_bits_per_sample(self, audio_bits_per_sample):
        self._audio_bits_per_sample = audio_bits_per_sample

    @property
    def watermark(self):
        return self._watermark

    @watermark.setter
    def watermark(self, watermark):
        self._watermark = watermark

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, extension):
        self._extension = extension

    @property
    def video_decoder(self):
        return self._video_decoder

    @video_decoder.setter
    def video_decoder(self, video_decoder):
        self._video_decoder = video_decoder

    @property
    def prefetch_enabled(self):
        return self._prefetch_enabled

    @prefetch_enabled.setter
    def prefetch_enabled(self, prefetch_enabled):
        self._prefetch_enabled = prefetch_enabled

    @property
    def tcp_receive_buffer(self):
        return self._tcp_receive_buffer

    @tcp_receive_buffer.setter
    def tcp_receive_buffer(self, tcp_receive_buffer):
        self._tcp_receive_buffer = tcp_receive_buffer

    def to_dict(self):
        obj_dict = self.__dict__
        cleaned_dict = {}
        for key, value in obj_dict.items():
            if key.startswith('_'):
                key = key[1:]
            cleaned_dict[key] = value
        return cleaned_dict

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False)
