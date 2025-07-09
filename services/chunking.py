# from typing import List
# import re

# def semantic_chunking(text: str, max_chunk_size: int = 800, min_chunk_size: int = 300, overlap: int = 100) -> List[str]:
#     """
#     Enhanced semantic chunking:
#     - Splits by paragraphs and sections
#     - Adds overlap between chunks for better context retention
#     - Preserves more document structure
#     """
#     # Split by paragraphs (preserve newlines for structure)
#     paragraphs = re.split(r'\n\s*\n', text)
#     chunks = []
#     current_chunk = ""
#     i = 0
#     while i < len(paragraphs):
#         paragraph = paragraphs[i].strip()
#         if not paragraph:
#             i += 1
#             continue
#         # If adding this paragraph would exceed max size, finalize current chunk
#         if current_chunk and len(current_chunk) + len(paragraph) > max_chunk_size:
#             chunks.append(current_chunk)
#             # Overlap: start new chunk with last N chars of previous chunk
#             if overlap > 0 and len(current_chunk) > overlap:
#                 current_chunk = current_chunk[-overlap:]
#             else:
#                 current_chunk = ""
#         if current_chunk:
#             current_chunk += "\n\n" + paragraph
#         else:
#             current_chunk = paragraph
#         i += 1
#     # Add the last chunk if it's not empty and large enough
#     if current_chunk and len(current_chunk) >= min_chunk_size:
#         chunks.append(current_chunk)
#     return chunks

# ------------------------------------------------------------------------------------


from typing import List
import nltk

# Download the punkt tokenizer if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def semantic_chunking(
    text: str,
    max_chunk_size: int = 800,
    min_chunk_size: int = 300,
    overlap: int = 100
) -> List[str]:
    """
    Sentence-based chunking using NLTK for robust sentence splitting.
    Uses a sliding window with overlap for high semantic coherence.
    """
    sentences = nltk.sent_tokenize(text)
    chunks = []
    current_chunk = ""
    i = 0
    while i < len(sentences):
        sentence = sentences[i]
        if current_chunk and len(current_chunk) + len(sentence) > max_chunk_size:
            chunks.append(current_chunk)
            # Overlap: start new chunk with last N chars of previous chunk
            if overlap > 0 and len(current_chunk) > overlap:
                current_chunk = current_chunk[-overlap:]
            else:
                current_chunk = ""
        if current_chunk:
            current_chunk += " " + sentence
        else:
            current_chunk = sentence
        i += 1
    # Add the last chunk if it's not empty and large enough
    if current_chunk and len(current_chunk) >= min_chunk_size:
        chunks.append(current_chunk)
    return chunks
