import os
from datetime import datetime
import pdfplumber
import docx


def list_files(directory: str, extension: str = None) -> dict:
    try:
        if not os.path.exists(directory):
            return {
                "status": "error",
                "error": f"Directory '{directory}' does not exist"
            }

        files_data = []

        for file in os.listdir(directory):
            filepath = os.path.join(directory, file)

            if os.path.isfile(filepath):
                if extension and not file.endswith(extension):
                    continue

                stat = os.stat(filepath)

                files_data.append({
                    "name": file,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat()
                })

        return {
            "status": "success",
            "data": files_data
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    
def read_file(filepath: str) -> dict:
    try:
        if not os.path.exists(filepath):
            return {
                "status": "error",
                "error": f"File '{filepath}' not found"
            }
        # .txt files are supported for now, can add more types later
        if filepath.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            return {
                "status": "success",
                "data": {
                    "content": content,
                    "type": "txt"
                }
            }
        
        # PDF
        elif filepath.endswith(".pdf"):
            content = ""
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    content += page.extract_text() or ""

            return {
                "status": "success",
                "data": {
                    "content": content,
                    "type": "pdf"
                }
            }

        # DOCX
        elif filepath.endswith(".docx"):
            doc = docx.Document(filepath)
            content = []                           #"\n".join([para.text for para in doc.paragraphs])


        # Extract paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                content.append(para.text)

        # Extract tables (IMPORTANT)
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        content.append(cell.text)
            return {
                "status": "success",
                "data": {
                    "content": "\n".join(content),
                    "type": "docx"
                }
            }

        else:
            return {
                "status": "error",
                "error": "Unsupported file type "
            }


       

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
    

def search_in_file(file_path: str, keyword: str) -> dict:
    try:
        # Step 1: read file using existing function
        file_result = read_file(file_path)

        if file_result["status"] == "error":
            return file_result

        content = file_result["data"]["content"]

        # Step 2: split into lines
        lines = content.split("\n")

        matches = []

        # Step 3: search (case-insensitive)
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                matches.append({
                    "line_number": i + 1,
                    "match": line.strip()
                })

        return {
            "status": "success",
            "data": matches
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }