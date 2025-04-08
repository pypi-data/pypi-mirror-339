#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : files
# @Time         : 2025/4/2 10:40
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *


file = "/Users/betterme/PycharmProjects/AI/QR.png"
#
# file_object = client.files.upload(file=file)
# prompt = "一句话总结"

file_object = client.aio.files.upload(file=file)