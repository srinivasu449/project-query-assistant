import faiss
import json
import streamlit as st
from sentence_transformers import SentenceTransformer
import torch
import openai
import os

# import warnings

# warnings.filterwarnings(
#     "ignore",
#     message="The current process just got forked, after parallelism has already been used",
# )

# Set OpenAI API key (use your own API key here)
openai.api_key = "<provide-open-ai-api-key>"

# Force models to use CPU
device = torch.device("cpu")
os.environ["TOKENIZERS_PARALLELISM"] = "false"


@st.cache_resource
def load_faiss_index():
    # Load FAISS index
    return faiss.read_index("embeddings/code_index.bin")


@st.cache_resource
def load_metadata():
    # Load metadata
    with open("embeddings/metadata.json", "r") as f:
        return json.load(f)


@st.cache_resource
def load_sentence_transformer():
    # Use a lightweight model for embedding generation
    return SentenceTransformer("all-MiniLM-L6-v2")


# Load models, FAISS index, and metadata
index = load_faiss_index()
metadata = load_metadata()
sentence_model = load_sentence_transformer()


# Streamlit app UI
st.title("Codebase Q&A System")
query = st.text_input("Ask a question about the codebase:")


def get_answer_from_llm(user_query, relevant_context):
    """
    Generate a detailed explanation for the given query using OpenAI's GPT model.
    """
    prompt = f"""
    User Query: {user_query}

    Relevant Code and Context:
    {relevant_context}

    Please provide a clear and concise explanation, focusing on answering the user's query. 
    - If there is relevant code or context, explain how the code works, what the key functionalities are, and how it addresses the query. 
    - If there is no code or relevant context available, try to answer based on the query and available information.
    - If you cannot provide an answer, kindly state that you are unable to help.

    If there is any code, provide it below your explanation. 
    If no code is provided, do not include code in your response.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",  # You can also use gpt-4 or any other available model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,  # You can adjust max tokens depending on response length
            temperature=0.7,  # Control the creativity of the output (adjust as needed)
        )
        print(".....done")
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {e}"


if query:
    try:
        # Encode the user query to get its embedding
        query_embedding = sentence_model.encode([query])
        _, I = index.search(
            query_embedding, k=3
        )  # Search for the top 3 relevant code snippets

        # Collect relevant code, descriptions, and comments
        relevant_context = ""
        for idx in I[0]:
            if idx >= len(metadata):  # Safety check for index out of range
                st.write("No more results.")
                continue
            print("idx...............", idx)
            result = metadata[idx]
            print("result.......", result)
            code_snippet = result.get(
                "code", "No code snippet available"
            )  # Retrieve the code snippet
            description = result.get("docstring", "No docstring available")
            comments = result.get("comments", "No comments available")

            relevant_context += f"**{result['type']} {result['name']}**\n"
            relevant_context += f"Description: {description}\n"
            relevant_context += f"Code:\n{code_snippet}\n"
            relevant_context += f"Comments:\n{comments}\n\n"

        # Use the LLM to generate a detailed explanation
        detailed_answer = get_answer_from_llm(query, relevant_context)
        st.write(f"**Detailed Answer**: {detailed_answer}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
