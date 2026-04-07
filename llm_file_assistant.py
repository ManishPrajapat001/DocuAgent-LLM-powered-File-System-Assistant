from fs_tools import read_file, list_files, search_in_file

tools = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files in a directory with optional extension filter",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "extension": {"type": "string"}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read content of a file",
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
            "description": "Search for a keyword in a file",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "keyword": {"type": "string"}
                },
                "required": ["file_path", "keyword"]
            }
        }
    }

]