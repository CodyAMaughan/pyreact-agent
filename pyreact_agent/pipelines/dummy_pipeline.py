"""
title: PyReAct Coding Agent Manifold Pipeline
author: Cody Maughan
date: 2024-11-25
version: 1.0
license: MIT
description: A pipeline for running a simple ReAct agent with tools pyreact_agent-agent library.
"""


from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
import os


class Pipeline:

    class Valves(BaseModel):
        CONTAINER_NAME: str
        OLLAMA_BASE_URL: str
        OLLAMA_MODEL_NAME: str

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
                "CONTAINER_NAME": os.getenv("CONTAINER_NAME", "my-python-container"),
                "OLLAMA_BASE_URL": os.getenv("OLLAMA_BASE_URL", "http://192.168.86.23:11434"),
                "OLLAMA_MODEL_NAME": os.getenv("OLLAMA_MODEL_NAME", "qwen2.5-coder:32b"),
            }
        )
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
            # for message in self.agent.reason_and_act(user_message):
            #     pass
            return "This is a test..."
        except Exception as e:
            return f"Error: {e}"
