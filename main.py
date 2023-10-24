from pyrogram import Client, filters
import whisper
import re
from collections import deque
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv

load_dotenv()

app = Client(
    "summariseItBot",
    api_id=os.getenv('TELEGRAM_API_ID'),
    api_hash=os.getenv('TELEGRAM_API_HASH'),
    bot_token=os.getenv('TELEGRAM_BOT_TOKEN')
)

openai.api_key = os.getenv('OPENAI_API_KEY')


def transcribe_video(video_path):
    print("transcribing the video...")

    model = whisper.load_model("base.en")
    result = model.transcribe(video_path, fp16=False)

    transcript_text = result['text']
    # Remove speaker labels like "Speaker Name:"
    cleaned_transcript = re.sub(r'\w+?:', '', transcript_text)
    cleaned_transcript = ' '.join(cleaned_transcript.split())

    return cleaned_transcript


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
    print("printing the response")
    print(response)
    return response.choices[0].message.content


@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hi there, welcome! You can upload your videos here and I'll summarize them for you. For "
        "YouTube videos, simply paste the URL."
    )


@app.on_message(filters.video)
async def handle_video(client, message):
    await message.reply_text("Processing your video...")
    print("Processing the video...")
    video_path = await message.download()

    # Transcribe
    transcript = transcribe_video(video_path)
    transcript_chunks = chunk_text(transcript)

    print("summarizing...")

    summaries = []

    for chunk in transcript_chunks:
        print(f"printing the chunk:f{chunk}")
        summary = summarize_chunk(chunk)
        summaries.append(summary)

    combined_summary = ' '.join(summaries)
    print(combined_summary)

    await message.reply_text(combined_summary[:4000])  # Telegram has a message limit


@app.on_message(filters.text)
async def summarize(client, message):
    url = message.text.split(maxsplit=1)[0]
    print(f"url IS:f{url}")

    video_id = extract_video_id(url)

    print(f"video id IS:f{video_id}")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_chunks = chunk_text(transcript)

    print("summarizing...")

    summaries = []

    for chunk in transcript_chunks:
        print(f"printing the chunk:f{chunk}")
        summary = summarize_chunk(chunk)
        summaries.append(summary)

    combined_summary = ' '.join(summaries)
    print(combined_summary)

    await message.reply_text(combined_summary[:4000])  # Telegram has a message limit


def extract_video_id(url):
    # Regular expression to match the video id in YouTube URLs
    youtube_id_pattern = re.compile(r'(?<=v=)[a-zA-Z0-9_-]+|(?<=be/)[a-zA-Z0-9_-]+')
    match = youtube_id_pattern.search(url)
    return match.group(0) if match else None


if __name__ == "__main__":
    app.run()
