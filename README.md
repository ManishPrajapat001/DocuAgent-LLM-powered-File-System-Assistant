# 📄 DocuAgent — LLM-Powered File System Assistant

DocuAgent is an intelligent file system assistant that enables users to interact with local files using natural language. It leverages LLM tool-calling to read, search, and process documents such as resumes, and generate structured outputs like summaries.

---

## 🚀 Features

### 🔹 File System Operations
- 📂 List files in a directory with optional filtering
- 📖 Read files (.txt, .pdf, .docx)
- 🔍 Search for keywords with contextual results (case-insensitive)
- ✍️ Write content to files with automatic directory creation

### 🔹 Intelligent LLM Integration
- 🤖 Natural language → tool execution
- 🔁 Multi-step reasoning with agent loop
- 🔧 Dynamic tool selection using function calling
- 📄 Resume summarization with automated file generation

---

## 🧠 System Architecture

text User → LLM → Tool Decision → Execute Tool → Return Result → LLM Response 

The system uses structured tool interfaces and an agent loop to allow the LLM to iteratively decide and execute actions based on user queries.

---

## 📁 Project Structure

project/ │ ├── fs_tools.py              # File system utilities ├── llm_file_assistant.py    # LLM agent and orchestration logic ├── test_files/              # Sample input files (resumes) ├── output/                  # Generated outputs (summaries, etc.) ├── requirements.txt ├── .env └── README.md

---

## ⚙️ Setup

### 1. Create Virtual Environment
python3 -m venv venv source venv/bin/activate

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Configure API Key

Create a .env file:
OPENAI_API_KEY=your_api_key_here

---

## ▶️ Run

python llm_file_assistant.py

---

## 🧪 Example Usage

### 📂 File Operations
List all files in test_files Read test_files/resume_1.txt Search Python in test_files/resume_1.txt

### 🤖 Intelligent Queries
Find resumes mentioning Python experience Read all resumes in test_files

### 📄 Summary Generation
Create a summary file for test_files/resume_1.txt

---

## 🧩 Key Capabilities

- LLM-powered tool orchestration  
- Structured function calling  
- Multi-step reasoning with agent loop  
- File parsing across multiple formats  
- Context-aware search  
- Automated document summarization  

---

## ⚠️ Error Handling

- Handles invalid file paths and directories  
- Gracefully manages empty or unsupported files  
- Returns structured error responses  

---

## 🧑‍💻 Author

Manish Prajapat

---

## ⭐ Overview

This project demonstrates how to build a practical LLM-powered backend system that combines natural language understanding with deterministic tool execution for real-world file processing tasks.
