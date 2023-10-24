import logging
import whisper
import re


def transcribe_video(video_path):
    logging.info("transcribing the video...")
    model = whisper.load_model("base.en")
    result = model.transcribe(video_path, fp16=False)

    transcript_text = result['text']
    # Remove speaker labels like "Speaker Name:"
    cleaned_transcript = re.sub(r'\w+?:', '', transcript_text)
    cleaned_transcript = ' '.join(cleaned_transcript.split())

    return cleaned_transcript


def extract_video_id(url):
    # Regular expression to match the video id in YouTube URLs
    youtube_id_pattern = re.compile(r'(?<=v=)[a-zA-Z0-9_-]+|(?<=be/)[a-zA-Z0-9_-]+')
    match = youtube_id_pattern.search(url)
    return match.group(0) if match else None
