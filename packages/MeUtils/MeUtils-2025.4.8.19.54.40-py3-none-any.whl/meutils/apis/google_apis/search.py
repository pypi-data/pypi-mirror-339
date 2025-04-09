#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : search
# @Time         : 2025/4/2 11:19
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch,HttpOptions

client = genai.Client(
    api_key="AIzaSyD19pv1qsYjx4ZKbfH6qvNdYzHMV2TxmPU",
    http_options=HttpOptions(
        base_url="https://all.chatfire.cc/genai"
    )
)


google_search_tool = Tool(
    google_search=GoogleSearch()
)


model_id = "gemini-2.0-flash"

response = client.models.generate_content(
    model=model_id,
    contents="写一首关于牡丹的诗歌",
    config=GenerateContentConfig(
        tools=[google_search_tool],
        # response_modalities=["TEXT"],
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)
# Example response:
# The next total solar eclipse visible in the contiguous United States will be on ...

# To get grounding metadata as web content.
print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)
print(response.candidates[0].grounding_metadata.grounding_chunks)
