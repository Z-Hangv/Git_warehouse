import time
import wave
from pyaudio import PyAudio, paInt16
import numpy as np
import dxl_server.server
import script_server.task_script
import matplotlib.pyplot as plt

ZCR_THREADHOLD = 100
ENERGY_THREADHOLD = 10000

framerate = 16000
sample_interval = 0.2  # 每隔sample_interval秒进行一次采样
NUM_SAMPLES = int(framerate * sample_interval)  # 2000
channels = 1
sampwidth = 2

TIME = 2


def save_wave_file(filename, data):
    '''save the date to the wavfile'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


# 计算每一帧的能量 256个采样点为一帧
def calEnergy(wave_data):
    energy = []
    sum = 0
    for i in range(len(wave_data)):
        sum = sum + (int(wave_data[i]) * int(wave_data[i]))
        if (i + 1) % 256 == 0:
            energy.append(sum)
            sum = 0
        elif i == len(wave_data) - 1:
            energy.append(sum)
    return energy


def sgn(data):
    if data >= 0:
        return 1
    else:
        return 0


# 计算过零率
def calZeroCrossingRate(wave_data):
    sum = 0
    for i in range(len(wave_data)):
        if i == 0:
            continue
        sum = sum + np.abs(sgn(wave_data[i]) - sgn(wave_data[i - 1]))
    return sum / len(wave_data)



def play(wav_data):
    play_handle = PyAudio()
    play_stream = play_handle.open(format=play_handle.get_format_from_width(sampwidth), channels=
    channels, rate=framerate, output=True)
    while True:
        data = wav_data
        if data == "": break
        play_stream.write(data)
    play_stream.close()
    play_handle.terminate()

def my_record():
    play_handle = PyAudio()
    play_stream = play_handle.open(format=play_handle.get_format_from_width(sampwidth), channels=
    channels, rate=framerate, output=True)
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1,
                     rate=framerate, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    my_buf = []
    time_tick = time.time()
    speaking_true = False
    stop_couter = 0
    string_audio_data_list = [None, None]
    open_mouth = False
    while True:  # 控制录音时间
        string_audio_data_list.remove(string_audio_data_list[0])
        string_audio_data = stream.read(NUM_SAMPLES)
        string_audio_data_list.append(string_audio_data)
        wave_data = np.fromstring(string_audio_data, dtype=np.short)
        wav_energe = np.abs(wave_data)
        wav_energe = np.mean(wav_energe)
        print("平均能量 %f" % wav_energe)
        view_energy = ""
        for i in range(int(wav_energe)):
            view_energy = view_energy + "*"
        print(view_energy)
        mean_zcr = calZeroCrossingRate(wave_data)
        mean_zcr = mean_zcr
        mean_zcr = mean_zcr * mean_zcr * 10000

        print("过零率 %f" % mean_zcr)
        view_zcr = ""
        for j in range(int(mean_zcr)):
            view_zcr = view_zcr + "-"
        print(view_zcr)
        # my_buf.append(string_audio_data)
        # if time.time() -  time_tick > 0.5:
        #     time_tick = time.time()
        # if string_audio_data != "":
            # dxl_server.server.client_send("pos mouth %d 100 0" % 100)
            # time.sleep(0.2)
        # else:
            # dxl_server.server.client_send("pos mouth %d 100 0" % 0)

        if wav_energe > 1000 : # and speaking_true != True :
            if open_mouth == True:
                dxl_server.server.client_send("pos mouth %d 100 0" % 0)
                open_mouth = False
            else:
                dxl_server.server.client_send("pos mouth %d 100 0" % 100)
                open_mouth = True

            # script_server.task_script.run_os_script_file("kouxing", "", 1)
            # speaking_true = True
        elif wav_energe <= 1000 : # and speaking_true == True :
            if open_mouth == True:
                dxl_server.server.client_send("pos mouth %d 100 0" % 0)
                open_mouth = False

            # if (stop_couter > 1):
            #     script_server.task_script.run_os_script_file("stop", "", 1)
            #     speaking_true = False
            #     stop_couter = 0
            # else:
            #     stop_couter = stop_couter + 1

        if string_audio_data_list[0]!= None:
            play_stream.write(string_audio_data_list[0])
    # save_wave_file('record.wav',my_buf)
    stream.close()


chunk = 2014




if __name__ == '__main__':
    my_record()
    print('Over!')
    play()
