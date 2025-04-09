import json
import logging
from typing import AsyncGenerator

from .api import Api
from .schemas.agent import (
    AgentCompletionChunk,
    AgentCompletionRequest,
    AgentCompletionResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api/agent")


class Agent:
    def __init__(self, api: Api):
        self.api: Api = api

    async def _stream_response(
        self, completion: AgentCompletionRequest
    ) -> AsyncGenerator[AgentCompletionChunk, None]:
        logger.debug("Starting async stream response")

        async with self.api.authenticated_async_client() as client:
            logger.debug(f"Async Client headers: {client.headers}")

            async with client.stream(
                "POST",
                f"/agent/{completion.persona}",
                json=completion.model_dump(),
                timeout=None,
                headers={"Accept": "text/event-stream"},
            ) as response:
                logger.debug(f"Async Response status: {response.status_code}")
                logger.debug(f"Async Response headers: {response.headers}")
                response.raise_for_status()

                # Process the stream directly and yield chunks instead of returning a function
                event_type = None
                line_count = 0
                async for line in response.aiter_lines():
                    line_count += 1
                    logger.debug(f"Processing async line {line_count}: {line[:100]}...")

                    if line:
                        logger.debug(f"Async Line string: {line[:100]}...")

                        if line.startswith("event:"):
                            event_type = line[6:].strip()
                            logger.debug(f"Found async event: {event_type}")
                        elif line.startswith("data:") and event_type:
                            data = line[5:].strip()
                            logger.debug(
                                f"Found async data for event {event_type}: {data[:100]}..."
                            )
                            if event_type == "chunk":
                                logger.debug("Yielding async chunk")
                                try:
                                    chunk = AgentCompletionChunk.model_validate(
                                        json.loads(data)
                                    )
                                    yield chunk
                                except Exception as e:
                                    logger.error(f"Error parsing async chunk: {e}")

                logger.debug(f"Async stream finished, processed {line_count} lines")

    async def _normal_response(
        self, completion: AgentCompletionRequest
    ) -> AgentCompletionResponse:
        async with self.api.authenticated_async_client() as client:
            response = await client.post(
                f"/agent/{completion.persona}",
                json=completion.model_dump(),
                timeout=None,
            )

            response.raise_for_status()

            return AgentCompletionResponse.model_validate(response.json())

    async def create_completion_async(
        self, completion: AgentCompletionRequest, stream: bool = False
    ):
        if stream:
            return self._stream_response(completion)
        else:
            return await self._normal_response(completion)

    def _stream_response_sync(self, completion: AgentCompletionRequest):
        logger.debug("Starting stream response sync")

        with self.api.authenticated_client() as client:
            logger.debug(f"Client headers: {client.headers}")

            with client.stream(
                "POST",
                f"/agent/{completion.persona}",
                json=completion.model_dump(),
                timeout=None,
                headers={"Accept": "text/event-stream"},
            ) as response:
                logger.debug(f"Response status: {response.status_code}")
                logger.debug(f"Response headers: {response.headers}")
                response.raise_for_status()

                # Process the stream directly and yield chunks instead of returning a function
                event_type = None
                line_count = 0
                for line in response.iter_lines():
                    line_count += 1
                    logger.debug(f"Processing line {line_count}: {line[:100]}...")

                    if line:
                        # Handle line as either bytes or string
                        if isinstance(line, bytes):
                            line_str = line.decode("utf-8")
                        else:
                            line_str = line

                        logger.debug(f"Line string: {line_str[:100]}...")

                        if line_str.startswith("event:"):
                            event_type = line_str[6:].strip()
                            logger.debug(f"Found event: {event_type}")
                        elif line_str.startswith("data:") and event_type:
                            data = line_str[5:].strip()
                            logger.debug(
                                f"Found data for event {event_type}: {data[:100]}..."
                            )
                            if event_type == "chunk":
                                logger.debug("Yielding chunk")
                                try:
                                    chunk = AgentCompletionChunk.model_validate(
                                        json.loads(data)
                                    )
                                    yield chunk
                                except Exception as e:
                                    logger.error(f"Error parsing chunk: {e}")

                logger.debug(f"Stream finished, processed {line_count} lines")

    def _normal_response_sync(self, completion: AgentCompletionRequest):
        with self.api.authenticated_client() as client:
            response = client.post(
                f"/agent/{completion.persona}",
                json=completion.model_dump(),
                timeout=None,
            )

            response.raise_for_status()

            return AgentCompletionResponse.model_validate(response.json())

    def create_completion(
        self, completion: AgentCompletionRequest, stream: bool = False
    ):
        if stream:
            return self._stream_response_sync(completion)
        else:
            return self._normal_response_sync(completion)
