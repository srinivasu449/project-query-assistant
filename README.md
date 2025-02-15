# project-query-assistant# Farmer Project Parser and Embedding Application

This application is designed to parse the **Farmer Management Project**, generate embeddings for its code and documentation, 
and provide a Q&A interface to answer user queries based on the parsed content.

---

## Features

- **Code Parsing**: Extracts function and module-level details from the Farmer Management Project.
- **Embeddings Creation**: Generates embeddings for efficient search and retrieval of project-specific information.
- **Q&A System**: Allows users to ask questions about the Farmer Management Project and get precise answers.
- **Enhanced Validations**: Ensures data integrity and supports country-specific rules during parsing and validation.

---

## Workflow

1. **Parse the Farmer Management Project**:
   - The application traverses the project directory, reading all files and extracting function definitions, docstrings, and comments.
   - Key code snippets and metadata are indexed.

2. **Generate Embeddings**:
   - Each code snippet or documentation piece is converted into embeddings for semantic understanding.
   - Enables a question-answering interface for users to query project-specific details.

3. **Ask Questions**:
   - Users can interact with the application by asking questions about the Farmer Management Project.
   - Answers are retrieved based on the embeddings and provided in natural language.

---

## Prerequisites

- Python 3.8 or above
- Virtualenv installed (`pip install virtualenv`)

# Create virtual Environment
$ python -m virtualenv .env
$ source .env/bin/activate
# Install Dependencies
pip install -r requirements.txt

## Run the application

# This command parse the project and store the embedding on the vector DB
python run.py
# This commands launches the Streamlit Q&A interface
streamlit run app/app.py
