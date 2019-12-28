#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@package
@brief
@author Dan SASAI (YCJ,RDD)
"""

from scrapy.contrib.exporter import JsonLinesItemExporter


class NonEscapeJsonLinesExporter(JsonLinesItemExporter):
    def __init__(self, filepath, **kwargs):
        super().__init__(filepath, ensure_ascii=False, indent=2)
