from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

ollama_model = LiteLlm(
    model="openai/indian-law-llm",  # This should match the 'model_name' in your config.yaml
    #api_base="http://localhost:4000" # Crucial: Point to your LiteLLM proxy
)

root_agent = Agent(
    model=ollama_model,
    name="MyLawAgent",
    description="You are an exeprt in answering questions about the Indian Law & Constitution.",
    tools=[],
    instruction="You will get proper formatted response from the underlying litellm layer which uses Ollama LLM model behind the scene.",
)
