**Problem Analysis:**

The error message states:
```
This is a chat model and not supported in the v1/completions endpoint. Did you mean to use v1/chat/completions?
```

This happens because `gpt-4` is a chat-based model, and the current `OpenAI` wrapper you are using (from `langchain_openai`) expects to use the older completions endpoint. For newer chat models like `gpt-4` or `gpt-3.5-turbo`, you need to use the `ChatOpenAI` class from `langchain.chat_models` instead of `OpenAI`.

**Key Points:**
- `OpenAI` (from older integrations) typically targets completion-style endpoints.
- `gpt-4` and `gpt-3.5-turbo` are chat-based models that require the chat completion endpoint.
- `ChatOpenAI` in LangChain supports chat endpoints directly, allowing the use of `gpt-4` and `gpt-3.5-turbo`.

**How to Fix:**

1. Import `ChatOpenAI` from `langchain.chat_models` instead of `OpenAI`.
2. In `chroma_utils.py`, replace the `OpenAI(...)` instance with `ChatOpenAI(...)` and specify `model_name="gpt-4"`.
3. The chain type "refine" or "stuff" works similarly, but `ChatOpenAI` is specifically for chat models.
4. Ensure `api_key=openai_api_key` and `model_name="gpt-4"` are passed to `ChatOpenAI`.

**Example Code Change in chroma_utils.py:**

```python
from langchain.chat_models import ChatOpenAI  # <-- Import ChatOpenAI

def get_qa_chain(chroma_db_path: str, collection_name: str):
    embeddings = SentenceTransformerEmbeddings()

    vectorstore = Chroma(
        collection_name=collection_name,
        persist_directory=chroma_db_path,
        embedding_function=embeddings
    )

    # Define prompts as before
    template = """You are a helpful assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say so.

Context:
{context}

Question: {question}
"""
    PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])

    refine_template = """You are a helpful assistant refining your previous answer with more context.
If you don't know the answer, just say so.

Existing answer:
{existing_answer}

Additional context:
{context}

Question: {question}

Refine the original answer based on the new context.
"""
    REFINE_PROMPT = PromptTemplate(
        template=refine_template,
        input_variables=["existing_answer", "context", "question"]
    )

    openai_api_key = current_app.config.get('OPENAI_API_KEY')
    print(f"Debug - Using API key (first 10 chars): {openai_api_key[:10] if openai_api_key else 'None'}")

    # Use ChatOpenAI instead of OpenAI
    llm = ChatOpenAI(api_key=openai_api_key, model_name="gpt-4", temperature=0)

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="refine",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type_kwargs={
            "question_prompt": PROMPT,
            "refine_prompt": REFINE_PROMPT,
            "document_variable_name": "context"
        }
    )

    return qa
```

**After these changes:**
- The code will now query the chat completion endpoint compatible with `gpt-4`.
- The `ChatOpenAI` model supports chat-based models and avoids the `NotFoundError` or `invalid_request_error` related to endpoint mismatches.
- You should now be able to ask questions and receive answers from GPT-4 using the vectorstore context.

**Summary:**
Switching from `OpenAI` to `ChatOpenAI` and specifying the `model_name="gpt-4"` resolves the endpoint mismatch error and allows the retrieval + refinement logic to work as intended with a chat-based model.