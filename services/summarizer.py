import logging
from collections import deque
import openai
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')


# Since there's a token limit (e.g., 2048 tokens for GPT-3) for each API call,
# for longer transcripts, we need to break them down into chunks or sections.
# then summarize each chunk separately and lastly combine the summaries.

def chunk_text(text, max_tokens=2048):
    sentences = deque(text.split('. '))
    chunks = []
    current_chunk = []
    current_length = 0

    while sentences:
        sentence = sentences.popleft() + '.'
        # If adding the next sentence doesn't exceed the max_token limit, add it to the current chunk.
        if current_length + len(sentence.split()) <= max_tokens:
            current_chunk.append(sentence)
            current_length += len(sentence.split())
        else:
            # Otherwise, start a new chunk.
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_length = len(sentence.split())

    # Add the last chunk if any sentences are left
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def summarize_chunk(chunk):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are tasked with summarizing the provided transcript clearly and concisely, "
                           "with a focus on research methods, key findings, and their broader implications. Make it "
                           "detailed yet to the point"
            },
            {
                "role": "user",
                "content": f"{chunk}"
            }
        ],
        temperature=0,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    logging.info("printing the response")
    logging.info(response)
    return response.choices[0].message.content
