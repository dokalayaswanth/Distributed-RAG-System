from pathlib import Path
from app.config import settings
from pypdf import PdfReader

def parse_text(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("TXT file must be UTF-8 encoded.") from exc
    except OSError as exc:
        raise ValueError(f"Unable to read TXT file: {path}") from exc
    text = text.strip()
    if not text:
        raise ValueError("Text file is not readable.")
    return text

def parse_pdf(path: Path) -> str:
    try:
        reader = PdfReader(str(path))

        extracted_pages: list[str] = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                extracted_pages.append(page_text)
        text = "\n\n".join(extracted_pages).strip()
        if not text:
            raise ValueError("PDF file has no readable text.")
        return text
    except Exception as exc:
        raise ValueError(f"Unable to read PDF file: {path}") from exc

def parse_document(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File does not exist {path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file {path}")
    
    file_extension = path.suffix.lower()
    if file_extension not in settings.allowed_extensions:
        raise ValueError(
            f"Unsupported file type '{file_extension}'. "
            f"Allowed types: {settings.allowed_extensions}"
        )
            
    if file_extension == ".txt":
        return parse_text(path)
    if file_extension == ".pdf":
        return parse_pdf(path)
