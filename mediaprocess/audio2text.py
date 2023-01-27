# -*- coding: UTF-8 -*-

import os
import wave
import contextlib
import datetime
from pydub.silence import split_on_silence
from moviepy.editor import AudioFileClip
import speech_recognition as sr
from pydub import AudioSegment


def get_audio_duration(file):
    with contextlib.closing(wave.open(file,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration

def get_large_audio_transcription(recognizer,path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = []
    time_lines = []
    # process each chunk 
    start_time = datetime.datetime.fromisoformat('2022-01-01T00:00:00')

    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = recognizer.record(source)
            # try converting it to text
            try:
                # 中文识别
                text = recognizer.recognize_google(audio_listened,language="zh-CN")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
                pass
            else:
                text = f"{text.capitalize()}. "
                print(start_time.time(), ":", text)
                whole_text.append(text)
                time_lines.append(start_time)
        duration = get_audio_duration(chunk_filename)
        start_time += datetime.timedelta(seconds=duration)
    return whole_text,time_lines

def video2text():
    audio_file = "./test.wav"
    r = sr.Recognizer()
    whole_text,time_lines = get_large_audio_transcription(r,audio_file)
    for t,txt in zip(time_lines,whole_text):
        print(f'{t.time()}: {txt}')

if __name__ == "__main__":
    video2text()
