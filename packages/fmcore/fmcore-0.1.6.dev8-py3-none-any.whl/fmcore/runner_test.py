import asyncio
from langchain_core.messages import HumanMessage
from fmcore.llm.base_llm import BaseLLM
from fmcore.llm.types.llm_types import LLMConfig

single_config_data = {
    "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
    "model_params": {
        "temperature": 0.5,
        "max_tokens": 1024
    },
    "provider_params": {
        "provider_type": "BEDROCK",
        "role_arn": "arn:aws:iam::<acc>:role/<role>",
        "region": "us-west-2",
        "rate_limit": {
            "max_rate": 1,
            "time_period": 10
        },
        "retries": {
            "max_retries": 3,
            "strategy": "constant"
        }
    }
}

def sync_test(llm):
    """Test synchronous LLM invocation."""
    messages = [HumanMessage(content="Tell me a joke—no questions, no feedback, just the joke!")]
    response = llm.invoke(messages=messages)
    print(f"Sync response: {response.content}")

async def async_test(llm):
    """Test asynchronous LLM invocation."""
    messages = [HumanMessage(content="Tell me a joke—no questions, no feedback, just the joke!")]
    response = await llm.ainvoke(messages=messages)
    print(f"Async response: {response.content}")

def sync_test_stream(llm):
    """Test synchronous stream LLM invocation."""
    messages = [HumanMessage(content="Tell me a joke—no questions, no feedback, just the joke!")]
    response_parts = []
    for token in llm.stream(messages=messages):
        content_list = token.content
        for content in content_list:
            if text := content.get("text"):
                response_parts.append(text)
    print(f"Sync response from Stream: {''.join(response_parts)}")

async def async_test_stream(llm):
    """Test asynchronous stream LLM invocation."""
    messages = [HumanMessage(content="Tell me a joke—no questions, no feedback, just the joke!")]
    response_parts = []
    async for token in await llm.astream(messages=messages):
        content_list = token.content
        for content in content_list:
            if text := content.get("text"):
                response_parts.append(text)
    print(f"Async response from Stream: {''.join(response_parts)}")

async def test_single_llm():
    llm_config = LLMConfig(**single_config_data)
    llm = BaseLLM.of(llm_config=llm_config)

    print("=== Running Single LLM Tests ===")
    sync_test(llm)
    sync_test_stream(llm)
    await async_test(llm)
    await async_test_stream(llm)
    print("=== Single LLM Tests Completed ===")

if __name__ == "__main__":
    asyncio.run(test_single_llm())
