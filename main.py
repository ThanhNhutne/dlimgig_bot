import telegram
from telegram.ext import Updater, MessageHandler, Filters
import instaloader
import os
import shutil
from config import TOKEN, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

# Create an Instaloader instance
L = instaloader.Instaloader(dirname_pattern="downloads/{target}")

def download_instagram_media(url):
    try:
        if "/p/" in url:
            shortcode = url.split("/p/")[1].split("/")[0]
        elif "/reel/" in url:
            shortcode = url.split("/reel/")[1].split("/")[0]
        else:
            return []

        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Download the post
        L.download_post(post, target=shortcode)

        # Get the path of the downloaded files
        download_dir = os.path.join("downloads", shortcode)
        media_paths = []
        for filename in os.listdir(download_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png', '.mp4')):
                media_paths.append(os.path.join(download_dir, filename))

        return media_paths
    except Exception as e:
        print(f"Error downloading media: {e}")
        return []

def handle_message(update, context):
    message_text = update.message.text

    if "instagram.com/p/" in message_text or "instagram.com/reel/" in message_text:
        update.message.reply_text("Downloading, please wait...")
        media_paths = download_instagram_media(message_text)

        if media_paths:
            download_dir = os.path.dirname(media_paths[0])
            for media_path in media_paths:
                try:
                    if media_path.endswith('.mp4'):
                        context.bot.send_video(chat_id=update.effective_chat.id, video=open(media_path, 'rb'))
                    else:
                        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(media_path, 'rb'))
                except Exception as e:
                    print(f"Error sending file: {e}")
                    update.message.reply_text("Error sending one of the files.")
            # Clean up the download directory
            shutil.rmtree(download_dir)
        else:
            update.message.reply_text("Failed to download the media. Please check the URL and try again.")
    else:
        update.message.reply_text("Please send a valid Instagram post or reel URL.")

def main():
    # Create 'downloads' directory if it doesn't exist
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Instagram login
    try:
        L.load_session_from_file(INSTAGRAM_USERNAME)
    except FileNotFoundError:
        try:
            L.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            L.save_session_to_file(INSTAGRAM_USERNAME)
        except Exception as e:
            print(f"Failed to log in to Instagram: {e}")
            print("Warning: Running without being logged in to Instagram. Downloads may fail.")


    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()