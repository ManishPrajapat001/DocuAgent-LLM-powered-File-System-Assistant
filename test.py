from fs_tools import read_file
from fs_tools import search_in_file

files = [
    "test_files/sample.txt",
    "test_files/harshibar_s_resume.pdf",
    "test_files/Resume.docx"
]

print(search_in_file("test_files/harshibar_s_resume.pdf", "python"))
print(search_in_file("test_files/Resume.docx", "Python"))

for file in files:
    print(f"\n--- Testing: {file} ---")
    result = read_file(file)
    
    
    print("Status:", result["status"])
    
    if result["status"] == "success":
        content = result["data"]["content"]
        print("Type:", result["data"]["type"])
        print("Content Preview:", content[:200])  # first 200 chars only
    else:
        print("Error:", result["error"])