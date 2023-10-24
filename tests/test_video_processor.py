from services.video_processor import transcribe_video, extract_video_id


def test_transcribe_video():
    assert transcribe_video("./downloads/2014_Three_Minute_Thesis_winning_presentation_by_Emily.mp4") is not None


def test_extract_video_id():
    sample_url = "https://www.youtube.com/watch?v=dh0pJdgY6Lc"
    assert extract_video_id(sample_url) == "dh0pJdgY6Lc"
