from pyaudio import PyAudio, paInt16
import script_server.task_script
import wave
import time
import numpy as np
import matplotlib.pyplot as plt
# 生成口型的脚本
import xbase

ZCR_THREADHOLD = 100
ENERGY_THREADHOLD = 10000

framerate = 16000
sample_interval = 0.2  # 每隔0.25秒进行一次采样
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
    while True:  # 控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        wave_data = np.fromstring(string_audio_data, dtype=np.short)
        wav_energe = np.square(wave_data)
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
        if False:
            play_stream.write(string_audio_data)
            # dxl_server.server.client_send("pos mouth %d 100 0" % 100)
            # time.sleep(0.2)
        # else:
            # dxl_server.server.client_send("pos mouth %d 100 0" % 0)



        if wav_energe > 200 and speaking_true != True :
            script_server.task_script.run_os_script_file("kouxing")
            speaking_true = True
        elif wav_energe <= 200 and speaking_true == True :
            script_server.task_script.run_os_script_file("stop")
            speaking_true = False

    # save_wave_file('record.wav',my_buf)
    stream.close()


chunk = 2014


kouxing_interval_time = 0.5   #计算能量的间隔, 单位秒
kouxing_threshold = 0.05       #阈值, 区间内平均能量超过最大值的百分之多少算是张嘴

def Wav2Script(wav_file_path):
    # 打开WAV文档
    # 首先载入Python的标准处理WAV文件的模块，然后调用wave.open打开wav文件，注意需要使用"rb"(二进制模式)打开文件：
    f = wave.open(wav_file_path,  "rb")
    # open返回一个的是一个Wave_read类的实例，通过调用它的方法读取WAV文件的格式和数据：

    # 读取格式信息
    # (nchannels, sampwidth, framerate, nframes, comptype, compname)

    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]

    # getparams：一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采样频率,
    # 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息：
    # getnchannels, getsampwidth, getframerate, getnframes等方法可以单独返回WAV文件的特定的信息。

    # 读取波形数据
    str_data = f.readframes(nframes)
    # readframes：读取声音数据，传递一个参数指定需要读取的长度（以取样点为单位），readframes返回的是二进制数据（一大堆
    # bytes)，在Python中用字符串表示二进制数据：
    f.close()

    # 将波形数据转换为数组
    # 接下来需要根据声道数和量化单位，将读取的二进制数据转换为一个可以计算的数组：
    wave_data = np.fromstring(str_data, dtype=np.short)
    # 通过fromstring函数将字符串转换为数组，通过其参数dtype指定转换后的数据格式，由于我们的声音格式是以两个字节表示一个取
    # 样值，因此采用short数据类型转换。现在我们得到的wave_data是一个一维的short类型的数组，但是因为我们的声音文件是双声
    # 道的，因此它由左右两个声道的取样交替构成：LRLRLRLR....LR（L表示左声道的取样值，R表示右声道取样值）。修改wave_data
    # 的sharp之后：
    if nchannels == 1:
        wav_inuse = np.abs(wave_data)  # 只取一个轨道, 单声道
    elif nchannels == 2:
        wave_data.shape = -1, 2
        # # 将其转置得到：
        wave_data = wave_data.T
        wave_data = wave_data[0]
        # 最后通过取样点数和取样频率计算出每个取样的时间：
    else:
        return ""  #有没有好几个声道的?

    wave_data = wave_data[0:1000000]

    x = np.arange(0, len(wave_data))
    # 每一帧的时间线
    wav_long = nframes/framerate    # 音频多少秒
    print("总共多少秒")
    print(wav_long)
    seg_wav_data = np.zeros(len(wave_data))
    seg_open_mouth_wav_data= np.zeros(len(wave_data))
    # seg_close_mouth_wav_data = np.zeros(len(wave_data))
    seg_open_mouth_wav_data[:] = -10000
    seg_frames = int(framerate/5)
    for i in range(0, len(wave_data), seg_frames):
        seg_mean = np.mean(np.abs(wave_data[i: i + seg_frames-1]))
        if seg_mean > 1000:
            seg_open_mouth_wav_data[i:i + seg_frames-1] = seg_mean
        # else :
            # seg_close_mouth_wav_data[i:i + seg_frames - 1] = seg_mean

    print(seg_wav_data)
    plt.subplot(211)
    plt.plot(x, wave_data, color='green')
    plt.plot(x, seg_open_mouth_wav_data, color='yellow')
    # plt.plot(x, seg_close_mouth_wav_data, color='blue')
    plt.show()
    return


#
# if __name__ == '__main__':
#     # script = Wav2Script(r"C:\zztdell\myprojects\xrobot4\home\sound\Ring10-2chanel.wav")
#     # wav_file = xconfig.get_sound_file_path("1.wav")
#     wav_file = "song.wav"
#     # wav_path = xconfig.get_sound_file_path("ring.wav")
#     # script = Wav2Script(wav_path)
#     # print(script)
#
#     exit(0)



if __name__ == '__main__':
    # my_record()
    Wav2Script(xbase.get_sound_file_path("long.wav"))
    print('Over!')
    # play()
