def is_pdf(content: bytes) -> bool:
    return content.startswith(b"%PDF")