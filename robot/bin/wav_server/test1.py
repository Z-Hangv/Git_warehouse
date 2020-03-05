"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import sys
import xbase


wf = wave.open(xbase.get_sound_file_path("bye.wav"), 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()


framerate = wf.getframerate()
# print(framerate)

sample_interval = 0.2  # 每隔sample_interval秒进行一次采样
NUM_SAMPLES = int(framerate * sample_interval)  # 2000
print(NUM_SAMPLES)

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)
while stream.is_active():
    time.sleep(0.1)

# stop stream (6)
stream.stop_stream()
stream.close()
wf.close()

# close PyAudio (7)
p.terminate()
print("finished")