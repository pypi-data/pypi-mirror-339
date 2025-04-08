class OpenAIProvicderParams(BaseProviderParams, AWSAccountMixin, RateLimiterMixin, RetryConfigMixin):
    """
    Configuration for a Bedrock provider using AWS.

    This class combines AWS account settings with request configuration parameters
    (such as rate limits and retry policies) needed to interact with Bedrock services.
    It mixes in AWS-specific account details, rate limiting, and retry configurations
    to form a complete provider setup.

    Mixes in:
        AWSAccountMixin: Supplies AWS-specific account details (e.g., role ARN, region).
        RateLimiterMixin: Supplies API rate limiting settings.
        RetryConfigMixin: Supplies retry policy settings.
    """
    aliases = ["OPENAI"]

    api_key: str
    base_url: str


{
        "provider_type": "OPENAI",
        "model_id": "anthropic.claude-3-haiku-20240307-v1:0",
        "model_params": {
            "max_tokens": 128,
            "temperature": 0.9,
            "top_p": 1.0,
        },
        "provider_params_list": [
            {
                "api_keyu": "arn:aws:iam::863518436859:role/ModelFactoryBedrockAccessRole",
                "baseUrlk": "us-west-2",
                "rate_limit": {
                    "max_rate": 1,  # Limit to 5 requests per 10 seconds for testing
                    "time_period": 10
                },
                "retries": {
                    "max_retries": 3,
                    "strategy": "constant"
                }
            },
            {
                "role_arn": "arn:aws:iam::863518436859:role/ModelFactoryBedrockAccessRole",
                "region": "us-east-1",
                "rate_limit": {
                    "max_rate": 1,  # Limit to 5 requests per 10 seconds for testing
                    "time_period": 10
                },
                "retries": {
                    "max_retries": 3,
                    "strategy": "constant"
                }
            }]
    }