import pyaudio
import wave
import sys
import xbase
import numpy as np
import movement.server

import xbase
from tool import *

MOD_NAME  = "kouxing_recording"

energy_threshold = 1000
sample_interval = 0.3  # 每隔sample_interval秒进行一次采样
open_mouth_script = "move mouth 100 100 0"
close_mouth_script = "move mouth 0 100 0"

try:
    energy_threshold = float (xbase.get_mod_config_content(MOD_NAME, "energy_threshold"))
except:
    pass

try:
    sample_interval = float (xbase.get_mod_config_content(MOD_NAME, "sample_interval"))
except:
    pass
#
#
# if __name__ == '__main__':
#     print("energy_threshold")
#     print(energy_threshold)
#     print("sample_interval")
#     print(sample_interval)


def play_with_kouxing(wav_file):
    wf = wave.open(xbase.get_sound_file_path(wav_file), 'rb')
    framerate = wf.getframerate()

    channels = wf.getnchannels()
    NUM_SAMPLES = int(framerate * sample_interval)  # 2000
    # print(NUM_SAMPLES)


    # instantiate PyAudio (1)
    p = pyaudio.PyAudio()

    # open stream (2)
    play_stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # # read data
    # data = wf.readframes(NUM_SAMPLES)
    #
    # # play stream (3)
    # while len(data) > 0:
    #     play_stream.write(data)
    #     data = wf.readframes(NUM_SAMPLES)

    open_mouth = False
    # string_audio_data = wf.readframes(NUM_SAMPLES)
    string_audio_data_list = [None, None]
    while True:  # 控制录音时间
        string_audio_data_list.remove(string_audio_data_list[0])
        string_audio_data = wf.readframes(NUM_SAMPLES)
        string_audio_data_list.append(string_audio_data)

        # string_audio_data = wf.readframes(NUM_SAMPLES)
        wave_data = np.fromstring(string_audio_data, dtype=np.short)
        if channels >= 2:
            wave_data.shape = -1, 2
            # # 将其转置得到：
            wave_data = wave_data.T
            # 最后通过取样点数和取样频率计算出每个取样的时间：
            wave_data = wave_data[0]  # 只取一个轨道, 单声道

        # string_audio_data = play_stream.read(NUM_SAMPLES)
        if len(string_audio_data) <= 0:
            break
        wav_energe = np.abs(wave_data)
        wav_energe = np.mean(wav_energe)
        if wav_energe > energy_threshold : # and speaking_true != True :
            if open_mouth == True:
                movement.server.client_send(close_mouth_script)
                open_mouth = False
            else:
                movement.server.client_send(open_mouth_script)
                open_mouth = True
        elif wav_energe <= energy_threshold :   # and speaking_true == True :
            if open_mouth == True:
                movement.server.client_send(close_mouth_script)
                open_mouth = False
        play_stream.write(string_audio_data)

    # stop stream (4)
    play_stream.stop_stream()
    play_stream.close()

    # close PyAudio (5)
    p.terminate()
    print("finished")




def play_wav(wave_file_):
    # open a wav format music
    chunk = 1024
    f = wave.open(xbase.get_sound_file_path(wave_file_), "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # paly stream
    while data != '':
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()