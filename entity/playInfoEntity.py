#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Author:liamlee
@Contact:geektalk@qq.com
@Ide:PyCharm
@Time:2022/02/12 08:33:36
@Project:WeiboSpider
@File:playInfoEntity.py
@Desc:
'''

class PlayInfoEntity(object):

	def __init__(self):
		self.__type = None
		self.__mime = None
		self.__protocol = None
		self.__label = None
		self.__url = None
		self.__bitrate = None
		self.__prefetch_range = None
		self.__video_codecs = None
		self.__fps = None
		self.__width = None
		self.__height = None
		self.__size = None
		self.__duration = None
		self.__sar = None
		self.__audio_codecs = None
		self.__audio_sample_rate = None
		self.__quality_label = None
		self.__quality_class = None
		self.__quality_desc = None
		self.__audio_channels = None
		self.__audio_sample_fmt = None
		self.__audio_bits_per_sample = None
		self.__watermark = None
		self.__extension = None
		self.__video_decoder = None
		self.__prefetch_enabled = None
		self.__tcp_receive_buffer = None

	@property
	def type(self):
		return self.__type

	@type.setter
	def type(self, type):
		self.__type = type

	@property
	def mime(self):
		return self.__mime

	@mime.setter
	def mime(self, mime):
		self.__mime = mime

	@property
	def protocol(self):
		return self.__protocol

	@protocol.setter
	def protocol(self, protocol):
		self.__protocol = protocol

	@property
	def label(self):
		return self.__label

	@label.setter
	def label(self, label):
		self.__label = label

	@property
	def url(self):
		return self.__url

	@url.setter
	def url(self, url):
		self.__url = url

	@property
	def bitrate(self):
		return self.__bitrate

	@bitrate.setter
	def bitrate(self, bitrate):
		self.__bitrate = bitrate

	@property
	def prefetch_range(self):
		return self.__prefetch_range

	@prefetch_range.setter
	def prefetch_range(self, prefetch_range):
		self.__prefetch_range = prefetch_range

	@property
	def video_codecs(self):
		return self.__video_codecs

	@video_codecs.setter
	def video_codecs(self, video_codecs):
		self.__video_codecs = video_codecs

	@property
	def fps(self):
		return self.__fps

	@fps.setter
	def fps(self, fps):
		self.__fps = fps

	@property
	def width(self):
		return self.__width

	@width.setter
	def width(self, width):
		self.__width = width

	@property
	def height(self):
		return self.__height

	@height.setter
	def height(self, height):
		self.__height = height

	@property
	def size(self):
		return self.__size

	@size.setter
	def size(self, size):
		self.__size = size

	@property
	def duration(self):
		return self.__duration

	@duration.setter
	def duration(self, duration):
		self.__duration = duration

	@property
	def sar(self):
		return self.__sar

	@sar.setter
	def sar(self, sar):
		self.__sar = sar

	@property
	def audio_codecs(self):
		return self.__audio_codecs

	@audio_codecs.setter
	def audio_codecs(self, audio_codecs):
		self.__audio_codecs = audio_codecs

	@property
	def audio_sample_rate(self):
		return self.__audio_sample_rate

	@audio_sample_rate.setter
	def audio_sample_rate(self, audio_sample_rate):
		self.__audio_sample_rate = audio_sample_rate

	@property
	def quality_label(self):
		return self.__quality_label

	@quality_label.setter
	def quality_label(self, quality_label):
		self.__quality_label = quality_label

	@property
	def quality_class(self):
		return self.__quality_class

	@quality_class.setter
	def quality_class(self, quality_class):
		self.__quality_class = quality_class

	@property
	def quality_desc(self):
		return self.__quality_desc

	@quality_desc.setter
	def quality_desc(self, quality_desc):
		self.__quality_desc = quality_desc

	@property
	def audio_channels(self):
		return self.__audio_channels

	@audio_channels.setter
	def audio_channels(self, audio_channels):
		self.__audio_channels = audio_channels

	@property
	def audio_sample_fmt(self):
		return self.__audio_sample_fmt

	@audio_sample_fmt.setter
	def audio_sample_fmt(self, audio_sample_fmt):
		self.__audio_sample_fmt = audio_sample_fmt

	@property
	def audio_bits_per_sample(self):
		return self.__audio_bits_per_sample

	@audio_bits_per_sample.setter
	def audio_bits_per_sample(self, audio_bits_per_sample):
		self.__audio_bits_per_sample = audio_bits_per_sample

	@property
	def watermark(self):
		return self.__watermark

	@watermark.setter
	def watermark(self, watermark):
		self.__watermark = watermark

	@property
	def extension(self):
		return self.__extension

	@extension.setter
	def extension(self, extension):
		self.__extension = extension

	@property
	def video_decoder(self):
		return self.__video_decoder

	@video_decoder.setter
	def video_decoder(self, video_decoder):
		self.__video_decoder = video_decoder

	@property
	def prefetch_enabled(self):
		return self.__prefetch_enabled

	@prefetch_enabled.setter
	def prefetch_enabled(self, prefetch_enabled):
		self.__prefetch_enabled = prefetch_enabled

	@property
	def tcp_receive_buffer(self):
		return self.__tcp_receive_buffer

	@tcp_receive_buffer.setter
	def tcp_receive_buffer(self, tcp_receive_buffer):
		self.__tcp_receive_buffer = tcp_receive_buffer
