# -*- coding: utf-8 -*-
import time

import pyaudio
import wave



framerate = 16000
channels = 1
sampwidth = 2
NUM_SAMPLES=2000

if __name__ == '__main__':
    print("start recording...")
    record_handle= pyaudio.PyAudio()
    record_stream = record_handle.open(format=pyaudio.paInt16, channels=1,
                     rate=framerate, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    my_buf = []
    time_tick = time.time()
    while True:
        string_audio_data = record_stream.read_com(NUM_SAMPLES)
        my_buf.append(string_audio_data)
        if time.time() - time_tick > 5:
            break
    '''save the date to the wavfile'''
    wf=wave.open("test.wav",'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(my_buf))
    wf.close()
