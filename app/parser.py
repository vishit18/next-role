from pathlib import Path
import docx2txt
import PyPDF2

def extract_text(file_path: Path) -> str:
    if file_path.suffix == ".txt":
        return file_path.read_text(encoding="utf-8")

    elif file_path.suffix == ".pdf":
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif file_path.suffix == ".docx":
        return docx2txt.process(str(file_path))

    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")
