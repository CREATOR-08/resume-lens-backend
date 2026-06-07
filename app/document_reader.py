from fastapi import UploadFile, HTTPException


async def read_document(upload_file: UploadFile) -> str:
    """
    Reads PDF, DOCX, TXT, or MD files uploaded through FastAPI
    and returns extracted text.
    """

    if not upload_file.filename:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file has no filename."
        )

    suffix = upload_file.filename.lower().split(".")[-1]

    try:
        content = await upload_file.read()

        # TXT / MD
        if suffix in {"txt", "md"}:
            try:
                return content.decode("utf-8")
            except UnicodeDecodeError:
                raise HTTPException(
                    status_code=400,
                    detail="Text file must be UTF-8 encoded."
                )

        # PDF
        if suffix == "pdf":
            try:
                import fitz
            except ImportError:
                raise HTTPException(
                    status_code=500,
                    detail="PDF support requires PyMuPDF."
                )

            try:
                document = fitz.open(
                    stream=content,
                    filetype="pdf"
                )

                text = "\n".join(
                    page.get_text()
                    for page in document
                )

                document.close()

                return text

            except Exception as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to read PDF file: {str(exc)}"
                )

        # DOCX
        if suffix == "docx":
            try:
                from docx import Document
                from io import BytesIO
            except ImportError:
                raise HTTPException(
                    status_code=500,
                    detail="DOCX support requires python-docx."
                )

            try:
                document = Document(BytesIO(content))

                return "\n".join(
                    paragraph.text
                    for paragraph in document.paragraphs
                )

            except Exception as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to read DOCX file: {str(exc)}"
                )

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Supported formats: PDF, DOCX, TXT, MD."
            )
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected document processing error: {str(exc)}"
        )