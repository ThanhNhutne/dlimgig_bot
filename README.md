# Instagram Media Downloader Telegram Bot

This is a simple Telegram bot that downloads images and videos from Instagram posts and reels.

## Features

- Download media from public Instagram posts and reels.
- Handles both single and multiple media posts (carousels).
- Supports both images and videos.
- Cleans up downloaded files after sending.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/dlimgig_bot.git
    cd dlimgig_bot
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the bot:**
    - Rename the `config.py.example` file to `config.py`.
      ```bash
      mv config.py.example config.py
      ```
    - Open `config.py` and fill in your credentials:
      - `TOKEN`: Your Telegram Bot token from [BotFather](https://t.me/botfather).
      - `INSTAGRAM_USERNAME`: Your Instagram username.
      - `INSTAGRAM_PASSWORD`: Your Instagram password.

## Running the Bot

Once you have completed the setup, you can run the bot with the following command:

```bash
python main.py
```

The bot will start polling for new messages.

## Usage

Simply send an Instagram post or reel URL to the bot in a Telegram chat. The bot will download the media and send it back to you in the same chat.

**Example:**
```
https://www.instagram.com/p/Cxyz123abc/
```

The bot will respond with the image(s) or video(s) from that post.