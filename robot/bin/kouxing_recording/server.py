import xbase
from tool import *
import time
import pyaudio
import numpy as np
import dxl_server.server as dxl
import kouxing_recording



framerate = 16000
NUM_SAMPLES = int(framerate * kouxing_recording.sample_interval)  # 2000
channels = 1
sampwidth = 2
start_time_tick =time.time()

def start_record():
    print("start recording...")
    dxl_start = False
    play_handle = pyaudio.PyAudio()
    play_stream = play_handle.open(format=play_handle.get_format_from_width(sampwidth), channels=
    channels, rate=framerate, output=True)
    record_handle= pyaudio.PyAudio()
    record_stream = record_handle.open(format=pyaudio.paInt16, channels=1,
                     rate=framerate, input=True,
                     frames_per_buffer=NUM_SAMPLES)
    string_audio_data_list = [None, None]
    # for i in range(0, int(kouxing_recording.sample_interval/0.2)):
    #     string_audio_data_list.append(None)
    open_mouth = False
    while True:  # 控制录音时间
        if time.time() - start_time_tick > 30:  # 给系统自检留时间
            dxl_start =True
        string_audio_data_list.remove(string_audio_data_list[0])
        string_audio_data = record_stream.read_com(NUM_SAMPLES)
        string_audio_data_list.append(string_audio_data)
        wave_data = np.fromstring(string_audio_data, dtype=np.short)
        wav_energe = np.abs(wave_data)
        wav_energe = np.mean(wav_energe)
        if wav_energe > kouxing_recording.energy_threshold : # and speaking_true != True :
            if open_mouth == True:
                if dxl_start: dxl.client_send(kouxing_recording.close_mouth_script)
                open_mouth = False
            else:
                if dxl_start: dxl.client_send(kouxing_recording.open_mouth_script)
                open_mouth = True
        elif wav_energe <= kouxing_recording.energy_threshold :   # and speaking_true == True :
            if open_mouth == True:
                if dxl_start: dxl.client_send(kouxing_recording.close_mouth_script)
                open_mouth = False

        if string_audio_data_list[0]!= None:
            play_stream.write(string_audio_data_list[0])
            # pass
    # record_stream.close()


if __name__ == '__main__':
    print('%s starting ...' % kouxing_recording.MOD_NAME)
    pid = os.getpid()
    fname = "%s.%d" % (kouxing_recording.MOD_NAME, pid)
    write_file(xbase.get_server_pid_file_path(fname), " ")

    while True:
        try:
            start_record()
        except Exception as e:
            print("error happened in recording... start again in 10 seconds")
            print(e)
            time.sleep(10)


