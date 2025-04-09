#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : common
# @Time         : 2025/4/2 13:03
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://ai.google.dev/gemini-api/docs/openai?hl=zh-cn

# https://googleapis.github.io/python-genai/genai.html#module-genai.models


from meutils.pipe import *
from meutils.llm.clients import AsyncOpenAI
from meutils.io.files_utils import to_url, to_bytes, guess_mime_type
from meutils.str_utils.regular_expression import parse_url

from meutils.schemas.openai_types import chat_completion, chat_completion_chunk, CompletionRequest, CompletionUsage

from meutils.config_utils.lark_utils import get_next_token_for_polling
from google import genai
from google.genai import types
from google.genai.types import HttpOptions, GenerateContentConfig, Content, HarmCategory, HarmBlockThreshold, Part
from google.genai.types import UserContent, ModelContent

FEISHU_URL = "https://xchatllm.feishu.cn/sheets/Bmjtst2f6hfMqFttbhLcdfRJnNf?sheet=MJw6hI"

"""
Gemini 1.5 Pro 和 1.5 Flash 最多支持 3,600 个文档页面。文档页面必须采用以下文本数据 MIME 类型之一：

PDF - application/pdf
JavaScript - application/x-javascript、text/javascript
Python - application/x-python、text/x-python
TXT - text/plain
HTML - text/html
CSS - text/css
Markdown - text/md
CSV - text/csv
XML - text/xml
RTF - text/rtf

- 小文件
- 大文件: 需要等待处理
"""


class GeminiClient(object):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key  # or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)
        self.base_url = "https://all.chatfire.cc/genai"

    async def create(self, request: CompletionRequest):
        client = await self.get_client()

        if any(i in request.model for i in ("image",)):
            messages = await self.to_image_messages(request)

            if len(messages) > 1:
                history = messages[:-1]
                message = messages[-1].parts
            else:
                history = []
                message = messages[-1].parts

            chat = client.aio.chats.create(  # todo: system_instruction
                model=request.model,
                config=GenerateContentConfig(
                    response_modalities=['Text', 'Image'],
                ),
                history=history
            )

            logger.debug(message)

            # message = [
            #     Part.from_text(text="画条狗")
            # ]

            for i in range(5):
                try:
                    chunks = await chat.send_message_stream(message)
                    async for chunk in chunks:

                        if chunk.candidates:
                            parts = chunk.candidates[0].content.parts or []
                            for part in parts:
                                # logger.debug(part)
                                if part.text:
                                    yield part.text

                                if part.inline_data:
                                    image_url = await to_url(
                                        part.inline_data.data,
                                        mime_type=part.inline_data.mime_type
                                    )
                                    yield f"![image_url]({image_url})"
                    break

                except Exception as e:
                    logger.debug(f"重试{i}: {e}")
                    if "The model is overloaded." in str(e):
                        await asyncio.sleep(1)
                        continue
                    else:
                        yield e
                        raise e

    async def to_image_messages(self, request: CompletionRequest):
        # 两轮即可连续编辑图片

        messages = []
        for m in request.messages:
            contents = m.get("content")
            if m.get("role") == "assistant":
                assistant_content = str(contents)
                if urls := parse_url(assistant_content):  # assistant
                    datas = await asyncio.gather(*map(to_bytes, urls))

                    parts = [
                        Part.from_bytes(
                            data=data,
                            mime_type="image/png"
                        )
                        for data in datas
                    ]
                    parts += [
                        Part.from_text(
                            text=request.last_assistant_content
                        ),
                    ]
                    messages.append(ModelContent(parts=parts))

            elif m.get("role") == "user":
                if isinstance(contents, list):
                    parts = []
                    for content in contents:
                        if content.get("type") == "image_url":
                            image_url = content.get("image_url", {}).get("url")
                            data = await to_bytes(image_url)

                            parts += [
                                Part.from_bytes(data=data, mime_type="image/png")
                            ]

                        elif content.get("type") == "text":
                            text = content.get("text")
                            if text.startswith('http'):
                                image_url, text = text.split(maxsplit=1)
                                data = await to_bytes(image_url)

                                parts += [
                                    Part.from_bytes(data=data, mime_type="image/png"),
                                    Part.from_text(text=text)
                                ]
                            else:
                                parts += [
                                    Part.from_text(text=text)
                                ]

                    messages.append(UserContent(parts=parts))

                else:  # str
                    if str(contents).startswith('http'):  # 修正提问格式， 兼容 url
                        image_url, text = str(contents).split(maxsplit=1)
                        data = await to_bytes(image_url)
                        parts = [
                            Part.from_bytes(data=data, mime_type="image/png"),
                            Part.from_text(text=text)
                        ]
                    else:
                        parts = [
                            Part.from_text(text=str(contents)),
                        ]
                    messages.append(UserContent(parts=parts))

        return messages

    async def upload(self, files: Union[str, List[str]]):  # => openai files
        client = await self.get_client()

        if isinstance(files, list):
            return await asyncio.gather(*map(self.upload, files))

        file_config = {"name": f"{shortuuid.random().lower()}", "mime_type": guess_mime_type(files)}
        return await client.aio.files.upload(file=io.BytesIO(await to_bytes(files)), config=file_config)

    @alru_cache()
    async def get_client(self):
        api_key = self.api_key or await get_next_token_for_polling(feishu_url=FEISHU_URL, from_redis=True)

        logger.info(f"GeminiClient: {api_key}")

        return genai.Client(
            api_key=api_key,
            http_options=HttpOptions(
                base_url=self.base_url
            )
        )


if __name__ == '__main__':
    file = "https://oss.ffire.cc/files/kling_watermark.png"

    api_key = os.getenv("GOOGLE_API_KEY")

    # arun(GeminiClient(api_key=api_key).upload(file))
    # arun(GeminiClient(api_key=api_key).upload([file] * 2))
    # arun(GeminiClient(api_key=api_key).create())

    content = [

        {"type": "text", "text": "https://oss.ffire.cc/files/nsfw.jpg 移除右下角的水印"},

        # {"type": "text", "text": "总结下"},
        # {"type": "image_url", "image_url": {"url": url}},

        # {"type": "video_url", "video_url": {"url": url}}

    ]

    # content = "https://oss.ffire.cc/files/nsfw.jpg 移除右下角的水印"

    #
    request = CompletionRequest(
        # model="qwen-turbo-2024-11-01",
        # model="gemini-all",
        model="gemini-2.0-flash-exp-image-generation",
        # model="qwen-plus-latest",

        messages=[
            {
                'role': 'user',

                'content': content
            },

        ],
        stream=True,
    )

    # arun(GeminiClient(api_key=api_key).to_image_messages(request))
    arun(GeminiClient(api_key=api_key).create(request))
