import PyPDF2
import docx
from fastapi import UploadFile, HTTPException
from io import BytesIO


async def extract_text(file: UploadFile) -> str:
    filename = file.filename.lower()

    # Read file bytes
    content = await file.read()

    # Handle TXT files
    if filename.endswith(".txt"):
        return content.decode("utf-8", errors="ignore")

    # Handle PDF files
    elif filename.endswith(".pdf"):
        try:
            text = ""
            reader = PyPDF2.PdfReader(BytesIO(content))
            for page in reader.pages:
                text += page.extract_text() or ""
            return text.strip()
        except PyPDF2.errors.PdfReadError:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is either corrupted or not a valid PDF. Please upload a valid file.",
            )

    # Handle DOCX files
    elif filename.endswith(".docx"):
        try:
            doc = docx.Document(BytesIO(content))
            return "\n".join([para.text for para in doc.paragraphs]).strip()
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="The uploaded DOCX file appears to be corrupted. Please save it again and re-upload.",
            )

    # Unsupported format
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format ({filename}). Please upload a TXT, DOCX, or PDF file.",
        )
