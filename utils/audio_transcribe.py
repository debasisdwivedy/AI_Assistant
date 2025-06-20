import openai

import os,sys
sys.path.append(os.getcwd())

def get_transcript(filename:str):
    folder_path = f'{os.getcwd()}/tools/video_ops/temp'
    files = os.listdir(folder_path)

    # Required because the downloaded format could be mp3, webm etc.
    matching_files = [f for f in files if f.startswith(filename)]

    if len(matching_files) > 0:
        with open(f"tools/video_ops/temp/{matching_files[0]}", "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        
        #print(transcript.text)
        return transcript.text
    else:
        return "Unable to READ the file !!!!"


if __name__ == "__main__":
    get_transcript("5ba1a01c-b20b-4863-9274-2fc22475989a.webm")