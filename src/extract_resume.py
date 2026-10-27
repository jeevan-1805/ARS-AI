import pymupdf as fitz
from src.reusables import section_headings

def create_embeds(blocks, embedding_model):
    embeds = embedding_model.encode(blocks, convert_to_numpy=True)
    return embeds

def extract_resume_text(file, embedding_model):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    blocks = []
    for page in doc:
        page_block = page.get_text("blocks")
        for block in page_block:
            text = block[4].strip()
            if not text:
                continue
            text = " ".join(text.split())
            if text.lower().rstrip(":") in section_headings:
                continue
            blocks.append(text)
    doc.close()

    embeds = create_embeds(blocks, embedding_model)
    return blocks, embeds

