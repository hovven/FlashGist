import logging
from pyrogram import Client, filters
import os
from youtube_transcript_api import YouTubeTranscriptApi
from services.summarizer import chunk_text, summarize_chunk
from services.video_processor import transcribe_video, extract_video_id

app = Client(
    "summariseItBot",
    api_id=os.getenv('TELEGRAM_API_ID'),
    api_hash=os.getenv('TELEGRAM_API_HASH'),
    bot_token=os.getenv('TELEGRAM_BOT_TOKEN')
)


@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "Hi there, welcome! You can upload your videos here and I'll summarize them for you. For "
        "YouTube videos, simply paste the URL."
    )


@app.on_message(filters.video)
async def handle_video(client, message):
    await message.reply_text("Processing your video...")
    logging.Logger.info("Processing the video...")
    video_path = await message.download()

    # Transcribe
    transcript = transcribe_video(video_path)
    transcript_chunks = chunk_text(transcript)

    logging.Logger.info("summarizing...")

    summaries = []

    for chunk in transcript_chunks:
        logging.info(f"printing the chunk:f{chunk}")

        summary = summarize_chunk(chunk)
        summaries.append(summary)

    combined_summary = ' '.join(summaries)
    logging.info(combined_summary)

    await message.reply_text(combined_summary[:4000])  # Telegram has a message limit


@app.on_message(filters.text)
async def summarize(client, message):
    url = message.text.split(maxsplit=1)[0]
    logging.info(f"url IS:f{url}")

    video_id = extract_video_id(url)

    logging.info(f"video id IS:f{video_id}")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_chunks = chunk_text(transcript)

    logging.info("summarizing...")

    summaries = []

    for chunk in transcript_chunks:
        logging.info(f"printing the chunk:f{chunk}")
        summary = summarize_chunk(chunk)
        summaries.append(summary)

    combined_summary = ' '.join(summaries)
    logging.info(combined_summary)

    await message.reply_text(combined_summary[:4000])  # Telegram has a message limit
