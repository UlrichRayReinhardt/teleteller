import yt_dlp
import os
import openai
import re


def download_audio_ytdlp(video_url, output_path='./downloads'):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory: {output_path}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            audio_file = os.path.splitext(filename)[0] + ".mp3"
            print("Audio downloaded correctly")
            return audio_file
    except Exception as e:
        print(f"Error with audio donloading: {e}")
        return None


def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript['text']
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


def save_transcription_to_file(transcription, clean_title):
    transcription_path = "dist/transcriptions"
    if not os.path.exists(transcription_path):
        os.makedirs(transcription_path)
        print(f"Created output directory: {transcription_path}")
    filename = os.path.join(transcription_path, f"{clean_title}.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(transcription)
    print(f"Transcribed text saved to file: {filename}")
    return filename


def summarize_text(text, config, max_tokens=500):
    try:
        instruction = str(config.get("PROMPT"))
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"{instruction}"},
                {"role": "user", "content": f"Summarize this text: {text}"}
            ],
            max_tokens=max_tokens,
            temperature=0.7
        )
        summary = response['choices'][0]['message']['content']
        return summary
    except Exception as e:
        print(f"Error during summarization: {e}")
        return None


def clean_video_title(title):
    """removes hashtags and '/download' from title name"""
    title = re.sub(r"#\w+", "", title)
    title = title.replace("downloads/", "")
    title = os.path.basename(title)
    return title.strip()
