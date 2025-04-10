"""
# File       : 试试_LLM异步.py
# Time       ：2024/9/15 下午7:39
# Author     ：xuewei zhang
# Email      ：shuiheyangguang@gmail.com
# version    ：python 3.12
# Description：
"""
"""
import os
import asyncio
from openai import AsyncOpenAI
import platform

client = AsyncOpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

async def main():
    response = await client.chat.completions.create(
        messages=[{"role": "user", "content": "你是谁"}],
        model="qwen-plus",
    )
    print(response.model_dump_json())

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
"""
from typing import Optional
from openai import OpenAI, NOT_GIVEN
from openai import AsyncOpenAI
from ai_tools_zxw.LLM_API import LLM
from ai_tools_zxw.LLM_API.config import 通义千问
from enum import Enum


class LLM_Model(str, Enum):
    qwen_plus = "qwen-plus"  # 输入：¥0.0008元/千tokens；输出：¥0.002元/千tokens
    qwen_turbo = "qwen-turbo"  # 输入：¥0.0003元/千tokens；输出：¥0.0006元/千tokens


model_price = {
    "qwen-plus": {"input": 0.0008, "output": 0.002},
    "qwen-turbo": {"input": 0.0003, "output": 0.0006},
}


class ChatToLLM(LLM):
    chat_history = [
        # {"role": "system", "content": "你现在扮演李白，你豪情万丈，狂放不羁；接下来请用李白的口吻和用户对话。"} , # 设置对话背景或者模型角色
        # {"role": "user", "content": "你是谁"},  # 用户的历史问题
        # {"role": "assistant", "content": "....."} , # AI的历史回答结果
        # # ....... 省略的历史对话
        # {"role": "user", "content": "你会做什么"}  # 最新的一条问题，如无需上下文，可只传最新一条问题
    ]

    usage_statistic = [
        # {'prompt_tokens': 6, 'completion_tokens': 348, 'total_tokens': 354},
    ]

    def __init__(self,
                 api_key: str = 通义千问.api_key,
                 model: LLM_Model = LLM_Model.qwen_plus,
                 base_url: str = 通义千问.base_url,
                 system_role_prompt: Optional[str] = None):

        self.system_role_prompt = system_role_prompt
        self.set_system_role()
        self.model = model.value

        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url,
        )

        self.client_async = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
        )

    def __del__(self):
        del self.client

    def chat(
            self,
            input_content: str,
            single_chat=False,
            model: str = "default",
            temperature: Optional[float] | NOT_GIVEN = NOT_GIVEN,
            timeout: int = NOT_GIVEN
    ) -> str:
        """
        resp["body"] 值示例：
        {
            "id: "xxx",
            "object": "chat.completion",
            "created": 1719051799,
            "result": "xxx",
            "is_truncated": false,
            "need_clear_history": false,
            "finish_response": 'normal',
            'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        }
        :param input_content:
        :param single_chat: 是否为单次对话
        :param model: default使用初始化时传入的模型, 或直接传入模型值
        :param temperature:  采样温度，用于控制模型生成文本的多样性。
               temperature越高，生成的文本更多样，反之，生成的文本更确定。
               取值范围： [0, 2)
               由于temperature与top_p均可以控制生成文本的多样性，因此建议您只设置其中一个值。
               更多说明，请参见Temperature 和 top_p。

               qwen-max系列、qwen-plus系列、qwen-turbo系列以及qwen开源系列：0.7；
               qwen-long：1.0；
               qwen-vl系列：0.01；
               qwen-audio系列：0.7；
               qwen-math系列：0；
               qwen-coder系列：0.7。
        :param timeout: 超时时间
        :return:
        """
        # 1. 设置聊天记录
        chat_history = self._check_length(self._set_text("user", input_content))
        if single_chat is True:
            chat_history = chat_history[-1:]
            # print("采用单次对话模式: ", len(chat_history))

        # 2. 对话
        print("发起LLM 通义千问 对话")
        self.set_system_role()
        resp = self.client.chat.completions.create(
            model=model if model != "default" else self.model,
            temperature=temperature,
            messages=chat_history,
            timeout=timeout
        )

        # 3. 设置聊天记录
        res = self._set_text("assistant", resp.choices[0].message.content)
        self._set_usage(resp.usage.to_dict())

        return res[-1]["content"]

    async def chat_async(
            self,
            input_content: str,
            single_chat=False,
            model: str = "default",
            temperature: Optional[float] | NOT_GIVEN = NOT_GIVEN,
            timeout: int = NOT_GIVEN) -> str:
        """
        resp["body"] 值示例：
        {
            "id: "xxx",
            "object": "chat.completion",
            "created": 1719051799,
            "result": "xxx",
            "is_truncated": false,
            "need_clear_history": false,
            "finish_response": 'normal',
            'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        }
        :param input_content:
        :param single_chat: 是否为单次对话
        :param model: default使用初始化时传入的模型, 或直接传入模型值
        :param temperature:  采样温度，用于控制模型生成文本的多样性。
               temperature越高，生成的文本更多样，反之，生成的文本更确定。
               取值范围： [0, 2)
               由于temperature与top_p均可以控制生成文本的多样性，因此建议您只设置其中一个值。
               更多说明，请参见Temperature 和 top_p。

               qwen-max系列、qwen-plus系列、qwen-turbo系列以及qwen开源系列：0.7；
               qwen-long：1.0；
               qwen-vl系列：0.01；
               qwen-audio系列：0.7；
               qwen-math系列：0；
               qwen-coder系列：0.7。
        :param timeout:
        :return:
        """
        # 1. 设置聊天记录
        chat_history = self._check_length(self._set_text("user", input_content))
        if single_chat is True:
            chat_history = chat_history[-1:]
            # print("采用单次对话模式: ", len(chat_history))

        # 2. 对话
        self.set_system_role()
        resp = await self.client_async.chat.completions.create(
            model=model if model != "default" else self.model,
            temperature=temperature,
            messages=chat_history,
            timeout=timeout
        )

        # 3. 设置聊天记录
        res = self._set_text("assistant", resp.choices[0].message.content)
        self._set_usage(resp.usage.to_dict())

        return res[-1]["content"]

    def chat_stream(
            self,
            input_content: str,
            single_chat=False,
            model: str = "default",
            temperature: Optional[float] | NOT_GIVEN = NOT_GIVEN,
            timeout: int = NOT_GIVEN
    ) -> str:
        """
        resp["body"] 值示例：
        {
            "id: "xxx",
            "object": "chat.completion",
            "created": 1719051799,
            "result": "xxx",
            "is_truncated": false,
            "need_clear_history": false,
            "finish_response": 'normal',
            'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        }
        :param input_content:
        :param single_chat: 是否为单次对话
        :param model: default使用初始化时传入的模型, 或直接传入模型值
        :param temperature:  采样温度，用于控制模型生成文本的多样性。
               temperature越高，生成的文本更多样，反之，生成的文本更确定。
               取值范围： [0, 2)
               由于temperature与top_p均可以控制生成文本的多样性，因此建议您只设置其中一个值。
               更多说明，请参见Temperature 和 top_p。

               qwen-max系列、qwen-plus系列、qwen-turbo系列以及qwen开源系列：0.7；
               qwen-long：1.0；
               qwen-vl系列：0.01；
               qwen-audio系列：0.7；
               qwen-math系列：0；
               qwen-coder系列：0.7。
        :param timeout: 超时时间
        :return:
        """
        # 1. 设置聊天记录
        chat_history = self._check_length(self._set_text("user", input_content))
        if single_chat is True:
            chat_history = chat_history[-1:]
            # print("采用单次对话模式: ", len(chat_history))

        # 2. 对话
        print("发起LLM 通义千问 对话")
        self.set_system_role()
        resp = self.client.chat.completions.create(
            model=model if model != "default" else self.model,
            temperature=temperature,
            messages=chat_history,
            timeout=timeout,
            stream=True
        )

        # 3. 接受完整消息
        full_content = ""
        for chunk in resp:
            full_content += chunk.choices[0].delta.content

        # 4. 设置聊天记录
        res = self._set_text("assistant", full_content)

        return res[-1]["content"]

    def chat_stream_yield(
            self,
            input_content: str,
            single_chat=False,
            model: str = "default",
            temperature: Optional[float] | NOT_GIVEN = NOT_GIVEN,
            timeout: int = NOT_GIVEN
    ) -> str:
        """
        resp["body"] 值示例：
        {
            "id: "xxx",
            "object": "chat.completion",
            "created": 1719051799,
            "result": "xxx",
            "is_truncated": false,
            "need_clear_history": false,
            "finish_response": 'normal',
            'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
        }
        :param input_content:
        :param single_chat: 是否为单次对话
        :param model: default使用初始化时传入的模型, 或直接传入模型值
        :param temperature:  采样温度，用于控制模型生成文本的多样性。
               temperature越高，生成的文本更多样，反之，生成的文本更确定。
               取值范围： [0, 2)
               由于temperature与top_p均可以控制生成文本的多样性，因此建议您只设置其中一个值。
               更多说明，请参见Temperature 和 top_p。

               qwen-max系列、qwen-plus系列、qwen-turbo系列以及qwen开源系列：0.7；
               qwen-long：1.0；
               qwen-vl系列：0.01；
               qwen-audio系列：0.7；
               qwen-math系列：0；
               qwen-coder系列：0.7。
        :param timeout: 超时时间
        :return:
        """
        # 1. 设置聊天记录
        chat_history = self._check_length(self._set_text("user", input_content))
        if single_chat is True:
            chat_history = chat_history[-1:]
            # print("采用单次对话模式: ", len(chat_history))

        # 2. 对话
        print("发起LLM 通义千问 对话")
        self.set_system_role()
        resp = self.client.chat.completions.create(
            model=model if model != "default" else self.model,
            temperature=temperature,
            messages=chat_history,
            timeout=timeout,
            stream=True
        )

        # 3. 接受完整消息
        full_content = ""
        for chunk in resp:
            yield chunk.choices[0].delta.content
            full_content += chunk.choices[0].delta.content

        # 4. 设置聊天记录
        res = self._set_text("assistant", full_content)

        return res[-1]["content"]


if __name__ == '__main__':
    from asyncio import run

    # General
    bot = ChatToLLM("...", LLM_Model.qwen_plus)
    resp = bot.chat("你好啊", single_chat=True)
    print(resp)

    print(bot.usage_statistic)

    a = run(bot.chat_async("请帮我写一份情书", single_chat=True))
    print(a)
    print(bot.usage_statistic)
