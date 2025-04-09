#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : openai_siliconflow
# @Time         : 2024/6/26 10:42
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import os

from meutils.pipe import *
from openai import OpenAI
from openai import OpenAI, APIStatusError
from meutils.schemas.openai_types import ChatCompletionRequest
from meutils.llm.openai_utils import to_openai_completion_params
from meutils.io.files_utils import to_base64

# base64_audio = arun(to_base64("https://oss.ffire.cc/files/lipsync.mp3"))
# base64_image = arun(to_base64("https://oss.ffire.cc/cdn/2025-04-01/duTeRmdE4G4TSdLizkLx2B", content_type="image/jpg"))

client = OpenAI(
    # api_key=os.getenv("GOOGLE_API_KEY"),
    api_key="AIzaSyDwniwFLwE-XBaerff7PltxC39DHq1dW4o",
    base_url=os.getenv("GOOGLE_BASE_URL"),
)



response = client.embeddings.create(
    input="Your text string goes here",
    model="gemini-embedding-exp-03-07" # text-embedding-004
)

print(response.data[0].embedding)

print(client.models.list().model_dump_json(indent=4))

# {
#     "gemini-2.0-pro-exp": "models/gemini-2.0-pro-exp",
#     "gemini-2.0-pro-exp-02-05": "models/gemini-2.0-pro-exp-02-05",
#     "gemini-2.5-pro-exp-03-25": "models/gemini-2.5-pro-exp-03-25",
#     "gemini-2.0-flash-thinking-exp": "models/gemini-2.0-flash-thinking-exp",
#     "gemini-2.0-flash": "models/gemini-2.0-flash"
#
# }

import base64
import requests
from openai import OpenAI


# Fetch the audio file and convert it to a base64 encoded string
url = "https://cdn.openai.com/API/docs/audio/alloy.wav"
response = requests.get(url)
response.raise_for_status()
wav_data = response.content
encoded_string = base64.b64encode(wav_data).decode('utf-8')

# completion = client.chat.completions.create(
#     model="gemini-2.0-flash",
#     stream=True,
#     modalities=["text", "audio"], # todo gemini规避掉
#     # audio={"voice": "alloy", "format": "wav"},
#     messages=[
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "What is in this recording?"
#                 },
#                 {
#                     "type": "input_audio",
#                     "input_audio": {
#                         "data": encoded_string,
#                         "format": "wav"
#                     }
#                 }
#             ]
#         },
#     ]
# )

# gemini-2.0-flash-audio
# completion = client.chat.completions.create(
#     model="gemini-2.0-flash",
#     # modalities=["text", "audio"],
#     audio={"voice": "alloy", "format": "wav"},
#     messages=[
#         {
#             "role": "user",
#             "content": "Is a golden retriever a good family dog?"
#         }
#     ]
# )
print(completion.choices[0].message)
# if __name__ == '__main__':
#     messages = [
#
#         {
#             "role": "user", "content": [
#             {
#                 "type": "text",
#                 "text": "一句话总结"
#             },
#             # {
#             #     "type": "image_url",
#             #     "image_url": {
#             #         "url": base64_image
#             #     }
#             # }
#         ]
#         }
#
#     ]
#     # messages = [
#     #     {
#     #         "role": "user",
#     #         "content": [
#     #             {
#     #                 "type": "text",
#     #                 "text": "一句话总结",
#     #             },
#     #             {
#     #                 "type": "input_audio",
#     #                 "input_audio": {
#     #                     "data": base64_audio,
#     #                     "format": "wav"
#     #                 }
#     #             }
#     #         ],
#     #     }
#     # ]
#
#     # messages = [
#     #     {
#     #         "role": "user",
#     #         "content": [
#     #             {
#     #                 "type": "text",
#     #                 "text": "画条狗",
#     #             }
#     #         ],
#     #     }
#     # ]
#     #
#     try:
#         completion = client.chat.completions.create(
#             # model="models/gemini-2.5-pro-preview-03-25",
#             model="models/gemini-2.5-pro-exp-03-25",
#             # model="models/gemini-2.0-flash",
#             # model="models/gemini-2.0-flash-exp-image-generation",
#             messages=messages,
#             # top_p=0.7,
#             top_p=None,
#             temperature=None,
#             # stream=True,
#             stream=False,
#
#             max_tokens=None,
#             # extra_body=dict(response_modalities = ['Text', 'Image'],)
#
#         )
#     except APIStatusError as e:
#         print(e.status_code)
#
#         print(e.response)
#         print(e.message)
#         print(e.code)
#     print(completion)
#     for chunk in completion:  # 剔除extra body
#         print(chunk)
#         if chunk.choices:
#             print(chunk.choices[0].delta.content)
