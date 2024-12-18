"""
title: PyReAct Coding Agent Manifold Pipeline
author: Cody Maughan
date: 2024-11-25
version: 1.0
license: MIT
description: A pipeline for running a simple ReAct agent with tools pyreact_agent-agent library.
requirements: pyreact_agent
"""


from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import os

# Imports from pyreact_agent-agent
from pyreact_agent.tools.core import Tools
from pyreact_agent.tools.docker_env import PythonDockerToolSet
from pyreact_agent.clients.ollama import OllamaClient
from pyreact_agent.agent import ReActAgent


class Pipeline:

    class Valves(BaseModel):
        CONTAINER_NAME: str
        OLLAMA_BASE_URL: str
        OLLAMA_MODEL_NAME: str
        DOCKER_URL: str

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "ollama_pipeline"
        self.name = "Ollama React Coding Agent"
        self.agent = None  # Setup in on startup
        pass

    async def on_startup(self):

        self.valves = self.Valves(
            **{
                "CONTAINER_NAME": os.getenv("CONTAINER_NAME", "pyreact-agent-container"),
                "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://192.168.86.23:11434"),
                "OLLAMA_MODEL_NAME": os.getenv("OLLAMA_MODEL_NAME", "qwen2.5-coder:32b"),
                "DOCKER_URL": os.getenv("DOCKER_URL", "unix:///var/run/docker.sock"),
            }
        )

        # Create tools object
        available_tool_sets = [PythonDockerToolSet(container_name=self.valves.CONTAINER_NAME)]
        tools = Tools(tool_list=[], tool_sets=available_tool_sets)

        # Instantiate the LLM client and agent
        llm_client = OllamaClient(base_url=self.valves.OLLAMA_BASE_URL,
                                  model=self.valves.OLLAMA_MODEL_NAME)
        self.agent = ReActAgent(llm_client, tools)

        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict,
        __event_emitter__=None
    ) -> Union[str, Generator, Iterator]:
        stream = body['stream']
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")
        if __event_emitter__ is None:
            print('No Event Emitter Possible!')

        if "user" in body:
            print("######################################")
            print(f'# User: {body["user"]["name"]} ({body["user"]["id"]})')
            print(f"# Message: {user_message}")
            print("######################################")

        try:
            these_messages = []
            # TODO: Refactor agent.py to handle message history within the agent,
            #  then refactor this to pass agent history
            chat_history_message = '\n\n'.join(
                [f'{message["role"]}: \n\n{message["content"]}\n\n' for message in messages]
            )
            for message in self.agent.reason_and_act(chat_history_message):
                if message.role not in ['system', 'user']:
                    if stream:
                        yield f"Role: {message.role}\n\n{message.content}\n\n"
                    else:
                        these_messages.append(message)
            if len(these_messages) == 0:
                if stream:
                    return
                else:
                    yield f"Error: No Messages Collected!"
                    return
            final_message = these_messages[-1].content
            if 'Final Answer:' in final_message:
                split_messages = final_message.split('Final Answer:')
                if len(split_messages) == 1:
                    yield split_messages[0]
                    return
                else:
                    final_message = 'Final Answer:'.join(split_messages[1:])
            if not stream:
                yield final_message
                return
        except Exception as e:
            print(f"Error: {e}")
            yield f"Error: {e}"
        return


# if __name__ == "__main__":
#     import asyncio
#     pipeline = Pipeline()
#     asyncio.run(pipeline.on_startup())
#     test_response = pipeline.pipe(
#         user_message='Hi, what are you supposed to do?',
#         model_id='test',
#         these_messages=[{'user': 'Hi, what are you supposed to do?'}],
#         body={'stream': True, 'user': {'name': 'Test User', 'id': 'test_id'}}
#     )
#     for response in test_response:
#         print(response)
#     asyncio.run(pipeline.on_shutdown())
