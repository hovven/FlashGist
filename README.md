# FlashGist

A powerful tool harnessing the potential of AI to generate concise summaries from video content. Integrated with Telegram, FlashGist enables users to get the essence of any video they desire swiftly.

## Features

- **Video to Text**: Converts user-uploaded videos into textual content.
- **AI-Powered Summarization**: Distills lengthy transcripts into easily digestible summaries.
- **Telegram Integration**: Seamlessly fetch summaries directly on your favorite messaging platform.
- **Multi-Source Support**: Get the gist of any video from multiple platforms, not just limited to YouTube.

## Getting Started

### Prerequisites

- Python 3.8+
- An active Telegram Bot Token
- [Whisper](https://link-to-whisper) for video transcription (or any other service you're using)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/hovven/FlashGist.git
   ```

2. Navigate into the project directory:


   ```bash
   cd FlashGist
   ```

3. Install the required packages:


   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your configurations (use 

`.env.sample` as a reference).

5. Run the bot:

   ```bash
   python main.py
   ```

## Usage

1. Start a conversation with your Telegram bot.
2. Upload or provide a link to the video you want summarized.
3. Wait for the magic to happen and get your summarized content in a FLASH!


## Contributing

Contributions are always welcome!

## License

This project is licensed under the MIT License.