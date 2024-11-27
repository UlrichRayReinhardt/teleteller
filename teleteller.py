import openai
from mainflow import download_audio_ytdlp, transcribe_audio, summarize_text, save_transcription_to_file, \
    clean_video_title
import telegram_bot
import os
import json


def load_config(config_file="config.json"):
    """Loading configuration"""
    if not os.path.exists(config_file):
        print(f"Configuration file '{config_file}' not found.")
        exit(1)
    with open(config_file, "r", encoding="utf-8") as file:
        return json.load(file)


def main(video_url, config):
    openai.api_key = config.get("OPENAI_API_KEY")
    audio_path = download_audio_ytdlp(video_url)
    video_title = audio_path.split("/")[-1].split(".")[0]
    clean_title = clean_video_title(video_title)
    if audio_path:
        print(f"FIle saved in: {audio_path}")
    audio_file_path = audio_path

    print("Transcribing audio...")
    transcribed_text = transcribe_audio(audio_file_path)
    if transcribed_text:
        save_transcription_to_file(transcribed_text, clean_title)

        print("\nSummarizing text...")
        summary = summarize_text(transcribed_text, config)
        if summary:
            print(f"Summary: {summary}")

    try:

        hyperlink = f"[{clean_title}]({video_url})"

        hashtags_from_title = [word for word in video_title.split() if word.startswith("#")]
        if hashtags_from_title:
            print(f"Found hashtags in title: {hashtags_from_title}")
            hashtags = hashtags_from_title
        else:
            print("No hashtags in title, using hashtags from config.")
            hashtags = config.get("HASHTAGS", [])
        if hashtags:
            hashtags_str = "\n".join(tag.replace("_", "\\_") for tag in hashtags)
        else:
            print("Neither hashtags in config and title")
            hashtags_str = ""

        if hashtags_str:
            message = f"{hyperlink}\n\n{summary}\n\n{hashtags_str}"
        elif not hashtags_str:
            message = f"{hyperlink}\n\n{summary}"
        else:
            print("No post description. Transcription error")

        print("\nPosting to telegram...")
        telegram_bot.push_to_telegram(
            message,
            str(config.get("TELEGRAM_BOT_TOKEN")),
            str(config.get("TELEGRAM_CHANNEL")),
        )
        print("Done! Please check your channel")
    except:
        print("Oops! Something went wrong. Please recheck config.json")


if __name__ == "__main__":
    config_file = "config.json"
    config = load_config(config_file)

    video_url = input("Please enter the YouTube video URL: ").strip()
    if not video_url.startswith("http"):
        print("Invalid URL. Please enter a valid YouTube video URL.")
        exit(1)

    main(video_url, config)
