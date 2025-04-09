from functools import cache
from openai import AsyncOpenAI
import instructor
from .base import BaseLLM, register_llm
from chan_agent.llm_track import async_wrap_create
from chan_agent.logger import logger
from abc import ABC
from pydantic import BaseModel
from typing import AsyncGenerator, Union, Iterator, List
from chan_agent.logger import logger
import asyncio
from chan_agent.utils.image import async_encode_image_from_url

@cache
def init_openai_client(base_url:str, api_key:str,**kwargs):
    """
    初始化client客户端
    """
    # 定义openai client
    client = AsyncOpenAI(
        base_url=base_url,
        api_key=api_key,
        **kwargs
    )

    client.chat.completions.create = async_wrap_create(create_fn=client.chat.completions.create)

    return client

@register_llm(model_type="async_openai")
class AsyncOpenaiLLM(ABC):
    def __init__(self, model_name: str = 'gpt-4o-mini', base_url:str=None, api_key:str='xxx'):
        super().__init__()
        self.model_name = model_name

        self.client = init_openai_client(base_url = base_url, api_key = api_key)
        if self.model_name is not None and self.model_name.startswith("gpt"):
            instructor_mode = instructor.Mode.TOOLS    
        else:
            # 兼任ollama等openai接口模型的其他模型
            instructor_mode = instructor.Mode.JSON
        self.instructor_client = instructor.from_openai(
            self.client,
            mode=instructor_mode
        )

    def set_model_name(self, model_name: str):
        """
        修改模型名称
        """
        self.model_name = model_name

    async def image_completions(
            self, 
            prompt: str, 
            images: List[str], 
            instructions: str = None, 
            temperature: float = None,
            top_p: float = None,
            max_tokens: int = None,
            timeout: int = 30,
            return_usage: bool = False
        ) -> str | dict:
        """
        图像分析
        """
        if 'gemini' in self.model_name:
            images = await asyncio.gather(*[async_encode_image_from_url(image_url) for image_url in images])

        messages = []
        if instructions:
            messages.append({"role": "system", "content": instructions})

        # 初始化用户内容列表，包含文本提示
        user_content = [{"type": "text", "text": prompt}]
        # 将图片URLs添加到用户内容列表中
        user_content.extend(
            [{"type": "image_url", "image_url": {"url": img_url}} for img_url in images])
        # 构造消息列表，包括系统指令和用户内容
        messages.append({"role": "user", "content": user_content})
        return await self.text_completions_with_messages(messages, temperature=temperature, top_p=top_p, max_tokens=max_tokens, timeout=timeout, return_usage=return_usage)

    async def image_basemodel_completions(
            self, 
            basemodel: type[BaseModel], 
            prompt: str, 
            images: List[str],
            instructions: str = None, 
            timeout:int=30
        )  -> Union[BaseModel,None]:
        """
        使用prompt生成basemodel
        """
        if 'gemini' in self.model_name:
            images = await asyncio.gather(*[async_encode_image_from_url(image_url) for image_url in images])

        messages = []
        if instructions:
            messages.append({"role": "system", "content": instructions})

        # 初始化用户内容列表，包含文本提示
        user_content = [{"type": "text", "text": prompt}]
        # 将图片URLs添加到用户内容列表中
        user_content.extend(
            [{"type": "image_url", "image_url": {"url": img_url}} for img_url in images])
        # 构造消息列表，包括系统指令和用户内容
        messages.append({"role": "user", "content": user_content})

        return await self.basemodel_completions_with_messages(basemodel, messages, timeout)


    async def text_completions_with_messages(
            self, 
            messages: list, 
            temperature: float = None,
            top_p: float = None,
            max_tokens: int = None,
            timeout: int = 30,
            return_usage: bool = False,
        ) -> str | dict:
        """
        使用 messages 列表生成文本 completions。
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=False,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            usage = {
                'completion_tokens': response.usage.completion_tokens,
                'prompt_tokens': response.usage.prompt_tokens,
                'total_tokens': response.usage.total_tokens
            } if response.usage else None
            content = response.choices[0].message.content

            if return_usage:
                return {
                    'content': content,
                    'usage': usage
                }
            else:
                return content
        except Exception as e:
            logger.error(f"text_completions_with_messages | Error: {e}")
            if return_usage:
                return {
                    'content': "error",
                    'usage': None
                }
            else:
                return "error"
    
    async def text_completions_with_messages_stream(
            self, 
            messages: list, 
            temperature: float = None,
            top_p: float = None,
            max_tokens: int = None,
            timeout: int = 30,
            return_usage: bool = False,
        ) -> AsyncGenerator[Union[str, dict], None]:
        """
        使用 messages 列表生成文本 completions。
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=True,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                timeout = timeout,
                stream_options={'include_usage': True}
            )

            full_content = ""
            for chunk in response:
                if chunk.choices:
                    choices = chunk.choices[0]
                    if choices.delta.content:
                        full_content += choices.delta.content
                
                if return_usage:
                    usage = {
                        'completion_tokens': chunk.usage.completion_tokens,
                        'prompt_tokens': chunk.usage.prompt_tokens,
                        'total_tokens': chunk.usage.total_tokens
                    } if chunk.usage else None
                    yield {
                        'content': full_content,
                        'usage': usage
                    }
                else:
                    yield full_content                
        except Exception as e:
            logger.error(f"text_completions_with_messages_stream | Error: {e}")
            if return_usage:
                yield {
                    'content': "error",
                    'usage': None
                }
            else:
                yield "error"
        
    
    async def text_completions(
            self, 
            prompt: str, 
            instructions: str = None, 
            temperature: float = None, 
            top_p: float = None, 
            max_tokens: int = None, 
            timeout: int = 30,
            return_usage: bool = False,
        ) -> str | dict:
        """
        使用prompt生成文本 completions
        """
        messages = []
        if instructions:
            messages.append({"role": "system", "content": instructions})
        messages.append({"role": "user", "content": prompt})

        return await self.text_completions_with_messages(messages, temperature, top_p, max_tokens, timeout, return_usage)
    
    async def text_completions_with_stream(
            self, 
            prompt: str, 
            instructions: str = None, 
            temperature: float = None, 
            top_p: float = None, 
            max_tokens: int = None, 
            timeout: int = 30,
            return_usage: bool = False
        )-> Iterator[Union[str, dict]]:
        """
        使用prompt生成文本 completions 流式返回
        """
        messages = []
        if instructions:
            messages.append({"role": "system", "content": instructions})
        messages.append({"role": "user", "content": prompt})
        return await self.text_completions_with_messages_stream(messages, temperature, top_p, max_tokens, timeout, return_usage)
        
    
    async def basemodel_completions(self, basemodel: type[BaseModel], prompt: str, instructions: str = None, timeout:int=30)  -> Union[BaseModel,None]:
        """
        使用prompt生成basemodel
        """
        messages = [{"role": "user", "content": prompt}]
        if instructions:
            messages.append({"role": "system", "content": instructions})

        return await self.basemodel_completions_with_messages(basemodel, messages, timeout)

    async def basemodel_completions_with_messages(self, basemodel: type[BaseModel], messages: list, timeout:int=30) -> Union[BaseModel,None]:
        """
        使用messages列表生成basemodel
        """
        # BUG 这里可能回卡死
        try:
            res = await self.instructor_client.chat.completions.create(
                model=self.model_name,
                response_model=basemodel,
                messages=messages,
                max_retries=3,
                timeout=timeout  # 内部timeout参数保留，但主要依赖外部超时
            )
            return res
        except TimeoutError:
            logger.error(f'basemodel_completions_with_messages | Timeout after {timeout} seconds')
            return None
        except Exception as e:
            logger.error(f'basemodel_completions_with_messages | Internal Error: {e}')
            return None

    async def fc_completions_with_messages(
        self, 
        messages: list, 
        functions: list,
        temperature: float = None,
        top_p: float = None,
        max_tokens: int = None,
        timeout: int = 30,
        return_usage: bool = False,
    ):
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                functions=functions,
                stream=False,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                timeout=timeout,
            )
            usage = {
                'completion_tokens': response.usage.completion_tokens,
                'prompt_tokens': response.usage.prompt_tokens,
                'total_tokens': response.usage.total_tokens
            } if response.usage else None
            content = response.choices[0].message.content
            function_call = None
            if response.choices[0].message.function_call:
                function_call = {
                    "name": response.choices[0].message.function_call.name,
                    "arguments": response.choices[0].message.function_call.arguments
                }

            if return_usage:
                return {
                    'content': content,
                    'function_call': function_call,
                    'usage': usage
                }
            else:
                return {
                    'content': content,
                    'function_call': function_call
                }
        except Exception as e:
            logger.error(f"text_completions_with_messages | Error: {e}")
            if return_usage:
                return {
                    'content': "error",
                    'function_call': None,
                    'usage': None
                }
            else:
                return {
                    'content': "error",
                    'function_call': None
                }

    async def fc_completions_with_messages_stream(
        self, 
        messages: list, 
        functions: list,
        temperature: float = None,
        top_p: float = None,
        max_tokens: int = None,
        timeout: int = 30,
        return_usage: bool = False,
    ):
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                functions=functions,
                stream=True,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                timeout = timeout,
                stream_options={'include_usage': True}
            )

            full_content = ""
            function_call = None
            function_call_finish = False
            for chunk in response:
                if chunk.choices:
                    choices = chunk.choices[0]
                    if choices.delta.content:
                        full_content += choices.delta.content
                    if choices.delta.function_call:
                        if function_call is None:
                            function_call = {
                                "name": choices.delta.function_call.name,
                                "arguments": choices.delta.function_call.arguments
                            }
                        else:
                            function_call["arguments"] += choices.delta.function_call.arguments
                    if choices.finish_reason == 'function_call':
                        function_call_finish = True

                
                if return_usage:
                    usage = {
                        'completion_tokens': chunk.usage.completion_tokens,
                        'prompt_tokens': chunk.usage.prompt_tokens,
                        'total_tokens': chunk.usage.total_tokens
                    } if chunk.usage else None
                    yield {
                        'content': full_content,
                        'function_call': function_call if function_call_finish else None,
                        'usage': usage
                    }
                else:
                    yield {
                        'content': full_content,
                        'function_call': function_call if function_call_finish else None
                    }                
        except Exception as e:
            logger.error(f"fc_completions_with_messages_stream | Error: {e}")
            if return_usage:
                yield {
                    'content': "error",
                    'function_call': None,
                    'usage': None
                }
            else:
                yield {
                    'content': 'error',
                    'function_call': None
                } 
