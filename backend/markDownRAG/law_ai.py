from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from litellm import CustomLLM, completion, acompletion
from litellm.types.utils import GenericStreamingChunk, ModelResponse
from typing import Iterator, AsyncIterator

from vector import md_rag
import os

ollama_url = os.environ.get("OLLAMA_API_BASE", "http://localhost:11434")
model = OllamaLLM(model="llama3.2", base_url=ollama_url)

template = """
You are an exeprt in answering questions about the Indian Law & Constitution which are in the Markdown files.

Here are some relevant documents: {documents}

Here is the question to answer: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

md_files = "./markdown_files"
retriever = md_rag(file_path=md_files, db_path="chroma_md_db", collection_name="law_files")
print("Retriever ready.")

def ask_law_llm(question):
    documents = retriever.invoke(question)
    result = chain.invoke({"documents": documents, "question": question})
    return result

class MyCustomLLM(CustomLLM):
    def completion(self, *args, **kwargs) -> ModelResponse:
        messages = kwargs.get("messages", [])
        #max_tokens = kwargs.get("max_tokens", 1000)
        prompt = messages[-1]["content"] if messages else "hi"
        return completion(
            model="law-llm/indian",
            mock_response=ask_law_llm(question=prompt),
        )

    async def acompletion(self, *args, **kwargs) -> ModelResponse:
        messages = kwargs.get("messages", [])
        #max_tokens = kwargs.get("max_tokens", 1000)
        prompt = messages[-1]["content"] if messages else "hi"
        return await acompletion(
            model="law-llm/indian",
            mock_response=ask_law_llm(question=prompt),
        )
    
    def streaming(self, *args, **kwargs) -> Iterator[GenericStreamingChunk]:
        messages = kwargs.get("messages", [])
        #max_tokens = kwargs.get("max_tokens", 1000)
        prompt = messages[-1]["content"] if messages else "hi"
        generic_streaming_chunk: GenericStreamingChunk = {
            "finish_reason": "stop",
            "index": 0,
            "is_finished": True,
            "text": ask_law_llm(question=prompt),
            "tool_use": None,
            "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0},
        }
        return generic_streaming_chunk # type: ignore

    async def astreaming(self, *args, **kwargs) -> AsyncIterator[GenericStreamingChunk]:
        messages = kwargs.get("messages", [])
        #max_tokens = kwargs.get("max_tokens", 1000)
        prompt = messages[-1]["content"] if messages else "hi"
        generic_streaming_chunk: GenericStreamingChunk = {
            "finish_reason": "stop",
            "index": 0,
            "is_finished": True,
            "text": ask_law_llm(question=prompt),
            "tool_use": None,
            "usage": {"completion_tokens": 0, "prompt_tokens": 0, "total_tokens": 0},
        }
        yield generic_streaming_chunk # type: ignore

law_llm = MyCustomLLM()
