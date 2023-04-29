from fastapi import FastAPI, Form, UploadFile, File
import uvicorn
from extractor import extract
import uuid
import os
import webbrowser

app = FastAPI()

# Use an absolute path for the uploads folder
UPLOADS_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "uploads")


@app.post("/extract_from_doc")
def extract_from_doc(
        file_format: str = Form(...),
        file: UploadFile = File(...),
):
    contents = file.file.read()

    # Use a context manager for file operations
    file_path = os.path.join(UPLOADS_FOLDER, f"{uuid.uuid4()}.pdf")
    with open(file_path, "wb") as f:
        f.write(contents)

    try:
        data = extract(file_path, file_format)
    except Exception as e:
        data = {
            'error': str(e)
        }

    # Use os.path.join to join paths
    os.remove(file_path)

    return data


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:8000/docs#/default/extract_from_doc_extract_from_doc_post")
    uvicorn.run(app, host="127.0.0.1", port=8000)

