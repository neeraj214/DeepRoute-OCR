import re


def clean_text(text: str) -> str:
    """
    Cleans OCR text by handling line fragmentation and noise.
    """
    if not text:
        return ""
        
    # Standardize line endings
    t = text.replace("\r", "\n")
    
    # Heuristic for fragmentation: if many lines are single characters or very short,
    # it might be a vertical layout or mis-segmented blocks.
    lines = [line.strip() for line in t.split("\n") if line.strip()]
    
    if len(lines) > 5:
        avg_len = sum(len(l) for l in lines) / len(lines)
        # If average length is very low (< 3 chars), it's likely fragmented
        if avg_len < 3.0:
            # Join fragments into a single block, potentially separated by spaces
            # if they were meant to be words, or just concatenated.
            # For now, join with spaces to reconstruct words.
            t = " ".join(lines)
    
    # Regular cleanup
    t = re.sub(r"\n{3,}", "\n\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.strip()


def to_structured(text: str):
    lines = [line.strip() for line in text.split("\n")]
    paragraphs = []
    current: list[str] = []
    for line in lines:
        if line == "":
            if current:
                paragraphs.append({"lines": current})
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append({"lines": current})
    return {"paragraphs": paragraphs}
