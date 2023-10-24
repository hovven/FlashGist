from services.summarizer import chunk_text


def test_chunk_text():
    text = "This is a test. " * 300  # Replicating a big text
    chunks = chunk_text(text)
    assert chunks is not None
    assert len(chunks[0].split('. ')) <= 2048
