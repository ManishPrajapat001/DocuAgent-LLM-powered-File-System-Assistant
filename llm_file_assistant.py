import json
from openai import OpenAI
from fs_tools import (
    read_file,
    list_files,
    search_in_file,
    write_file,
    generate_summary_filename
)
from dotenv import load_dotenv
import os

load_dotenv()


client = OpenAI()


# 🔹 SYSTEM PROMPT (Mapped cleanly)
SYSTEM_PROMPT = """
You are an intelligent resume file assistant operating over a file system.

You have access to tools for:
- listing files
- reading files
- searching content
- writing files

Strict Rules:
- ALWAYS use tools when information can be retrieved from files. Never guess file content.
- NEVER fabricate file names or content.
- For multi-step tasks (e.g., summarizing a resume):
  1. Identify file
  2. Read file
  3. Process content
  4. Write output if required
- When searching:
  - include file names
  - include short evidence snippets
- When creating files:
  - generate clean professional content
  - use meaningful file names
- If file/directory does not exist → return clear error
- If ambiguous → choose safest reasonable interpretation

Output Guidelines:
- Be clear and structured
- Reference file names used
- Avoid unnecessary verbosity
"""


# 🔹 TOOL DEFINITIONS
tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {"type": "string"},
                    "extension": {"type": "string"}
                },
                "required": ["directory"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read file content",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Search keyword inside a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "keyword": {"type": "string"}
                },
                "required": ["file_path", "keyword"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write content to a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["file_path", "content"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "create_summary",
        "description": "Create a professional summary of a resume file and save it",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string"}
            },
            "required": ["file_path"]
        }
    }
}
]


# 🔹 TOOL EXECUTOR
def execute_tool(tool_name, arguments):
    try:
        if tool_name == "list_files":
            return list_files(**arguments)

        elif tool_name == "read_file":
            return read_file(**arguments)

        elif tool_name == "search_in_file":
            return search_in_file(**arguments)

        elif tool_name == "write_file":
            return write_file(**arguments)
        
        elif tool_name == "create_summary":
            return create_summary(**arguments)

        else:
            return {"status": "error", "error": "Unknown tool"}

    except Exception as e:
        return {"status": "error", "error": str(e)}


# 🔹 AGENT LOOP
def run_agent():
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    while True:
        user_input = input("\nUser: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        messages.append({"role": "user", "content": user_input})

        # 🔁 Inner loop for tool chaining
        while True:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=tools,
                temperature=0
            )

            msg = response.choices[0].message

            # 🔧 Tool Call Case
            if msg.tool_calls:
                messages.append(msg)

                for tool_call in msg.tool_calls:

                    tool_name = tool_call.function.name

                    arguments = json.loads(tool_call.function.arguments)

                    print(f"\n[Tool Call] → {tool_name}")

                    print(f"[Arguments] → {arguments}")

                    result = execute_tool(tool_name, arguments)

                    messages.append({

                        "role": "tool",

                        "tool_call_id": tool_call.id,

                        "content": json.dumps(result)

                    })

            else:
                # ✅ Final response
                print("\nAssistant:\n", msg.content)
                messages.append(msg)
                break



def create_summary(file_path: str):
    # Step 1: read file
    file_data = read_file(file_path)

    if file_data["status"] == "error":
        return file_data

    content = file_data["data"]["content"]

    if not content.strip():
        return {"status": "error", "error": "Empty file content"}

    # Step 2: call LLM to summarize
    summary_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a professional resume summarizer. Create a concise, high-quality summary highlighting skills, experience, and key strengths."
            },
            {
                "role": "user",
                "content": f"Summarize this resume:\n\n{content[:4000]}"
            }
        ],
        temperature=0
    )

    summary = summary_response.choices[0].message.content

    # Step 3: generate filename
    filename = generate_summary_filename(file_path)
    output_path = f"output/{filename}"

    # Step 4: write file
    write_result = write_file(output_path, summary)

    if write_result["status"] == "error":
        return write_result

    return {
        "status": "success",
        "summary_file": output_path,
        "preview": summary[:200]
    }


if __name__ == "__main__":
    run_agent()