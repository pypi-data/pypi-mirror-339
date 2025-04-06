# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from llama_stack_client import LlamaStackClient, AsyncLlamaStackClient
from llama_stack_client.types import (
    BatchInferenceChatCompletionResponse,
)
from llama_stack_client.types.shared import BatchCompletion

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBatchInference:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_chat_completion(self, client: LlamaStackClient) -> None:
        batch_inference = client.batch_inference.chat_completion(
            messages_batch=[
                [
                    {
                        "content": "string",
                        "role": "user",
                    }
                ]
            ],
            model="model",
        )
        assert_matches_type(BatchInferenceChatCompletionResponse, batch_inference, path=["response"])

    @parametrize
    def test_method_chat_completion_with_all_params(self, client: LlamaStackClient) -> None:
        batch_inference = client.batch_inference.chat_completion(
            messages_batch=[
                [
                    {
                        "content": "string",
                        "role": "user",
                        "context": "string",
                    }
                ]
            ],
            model="model",
            logprobs={"top_k": 0},
            response_format={
                "json_schema": {"foo": True},
                "type": "json_schema",
            },
            sampling_params={
                "strategy": {"type": "greedy"},
                "max_tokens": 0,
                "repetition_penalty": 0,
            },
            tool_choice="auto",
            tool_prompt_format="json",
            tools=[
                {
                    "tool_name": "brave_search",
                    "description": "description",
                    "parameters": {
                        "foo": {
                            "param_type": "param_type",
                            "default": True,
                            "description": "description",
                            "required": True,
                        }
                    },
                }
            ],
        )
        assert_matches_type(BatchInferenceChatCompletionResponse, batch_inference, path=["response"])

    @parametrize
    def test_raw_response_chat_completion(self, client: LlamaStackClient) -> None:
        response = client.batch_inference.with_raw_response.chat_completion(
            messages_batch=[
                [
                    {
                        "content": "string",
                        "role": "user",
                    }
                ]
            ],
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_inference = response.parse()
        assert_matches_type(BatchInferenceChatCompletionResponse, batch_inference, path=["response"])

    @parametrize
    def test_streaming_response_chat_completion(self, client: LlamaStackClient) -> None:
        with client.batch_inference.with_streaming_response.chat_completion(
            messages_batch=[
                [
                    {
                        "content": "string",
                        "role": "user",
                    }
                ]
            ],
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_inference = response.parse()
            assert_matches_type(BatchInferenceChatCompletionResponse, batch_inference, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_completion(self, client: LlamaStackClient) -> None:
        batch_inference = client.batch_inference.completion(
            content_batch=["string"],
            model="model",
        )
        assert_matches_type(BatchCompletion, batch_inference, path=["response"])

    @parametrize
    def test_method_completion_with_all_params(self, client: LlamaStackClient) -> None:
        batch_inference = client.batch_inference.completion(
            content_batch=["string"],
            model="model",
            logprobs={"top_k": 0},
            response_format={
                "json_schema": {"foo": True},
                "type": "json_schema",
            },
            sampling_params={
                "strategy": {"type": "greedy"},
                "max_tokens": 0,
                "repetition_penalty": 0,
            },
        )
        assert_matches_type(BatchCompletion, batch_inference, path=["response"])

    @parametrize
    def test_raw_response_completion(self, client: LlamaStackClient) -> None:
        response = client.batch_inference.with_raw_response.completion(
            content_batch=["string"],
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_inference = response.parse()
        assert_matches_type(BatchCompletion, batch_inference, path=["response"])

    @parametrize
    def test_streaming_response_completion(self, client: LlamaStackClient) -> None:
        with client.batch_inference.with_streaming_response.completion(
            content_batch=["string"],
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_inference = response.parse()
            assert_matches_type(BatchCompletion, batch_inference, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBatchInference:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_chat_completion(self, async_client: AsyncLlamaStackClient) -> None:
        batch_inference = await async_client.batch_inference.chat_completion(
            messages_batch=[
                [
                    {
                        "content": "string",
                        "role": "user",
                    }
                ]
            ],
            model="model",
        )
        assert_matches_type(BatchInferenceChatCompletionResponse, batch_inference, path=["response"])

    @parametrize
    async def test_method_chat_completion_with_all_params(self, async_client: AsyncLlamaStackClient) -> None:
        batch_inference = await async_client.batch_inference.chat_completion(
            messages_batch=[
                [
                    {
                        "content": "string",
                        "role": "user",
                        "context": "string",
                    }
                ]
            ],
            model="model",
            logprobs={"top_k": 0},
            response_format={
                "json_schema": {"foo": True},
                "type": "json_schema",
            },
            sampling_params={
                "strategy": {"type": "greedy"},
                "max_tokens": 0,
                "repetition_penalty": 0,
            },
            tool_choice="auto",
            tool_prompt_format="json",
            tools=[
                {
                    "tool_name": "brave_search",
                    "description": "description",
                    "parameters": {
                        "foo": {
                            "param_type": "param_type",
                            "default": True,
                            "description": "description",
                            "required": True,
                        }
                    },
                }
            ],
        )
        assert_matches_type(BatchInferenceChatCompletionResponse, batch_inference, path=["response"])

    @parametrize
    async def test_raw_response_chat_completion(self, async_client: AsyncLlamaStackClient) -> None:
        response = await async_client.batch_inference.with_raw_response.chat_completion(
            messages_batch=[
                [
                    {
                        "content": "string",
                        "role": "user",
                    }
                ]
            ],
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_inference = await response.parse()
        assert_matches_type(BatchInferenceChatCompletionResponse, batch_inference, path=["response"])

    @parametrize
    async def test_streaming_response_chat_completion(self, async_client: AsyncLlamaStackClient) -> None:
        async with async_client.batch_inference.with_streaming_response.chat_completion(
            messages_batch=[
                [
                    {
                        "content": "string",
                        "role": "user",
                    }
                ]
            ],
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_inference = await response.parse()
            assert_matches_type(BatchInferenceChatCompletionResponse, batch_inference, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_completion(self, async_client: AsyncLlamaStackClient) -> None:
        batch_inference = await async_client.batch_inference.completion(
            content_batch=["string"],
            model="model",
        )
        assert_matches_type(BatchCompletion, batch_inference, path=["response"])

    @parametrize
    async def test_method_completion_with_all_params(self, async_client: AsyncLlamaStackClient) -> None:
        batch_inference = await async_client.batch_inference.completion(
            content_batch=["string"],
            model="model",
            logprobs={"top_k": 0},
            response_format={
                "json_schema": {"foo": True},
                "type": "json_schema",
            },
            sampling_params={
                "strategy": {"type": "greedy"},
                "max_tokens": 0,
                "repetition_penalty": 0,
            },
        )
        assert_matches_type(BatchCompletion, batch_inference, path=["response"])

    @parametrize
    async def test_raw_response_completion(self, async_client: AsyncLlamaStackClient) -> None:
        response = await async_client.batch_inference.with_raw_response.completion(
            content_batch=["string"],
            model="model",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        batch_inference = await response.parse()
        assert_matches_type(BatchCompletion, batch_inference, path=["response"])

    @parametrize
    async def test_streaming_response_completion(self, async_client: AsyncLlamaStackClient) -> None:
        async with async_client.batch_inference.with_streaming_response.completion(
            content_batch=["string"],
            model="model",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            batch_inference = await response.parse()
            assert_matches_type(BatchCompletion, batch_inference, path=["response"])

        assert cast(Any, response.is_closed) is True
