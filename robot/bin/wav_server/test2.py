import wav_server.robot_wav as robot_wav
import xbase

wav_object = robot_wav.PlayWav()
wav_object.play(xbase.get_sound_file_path("1.wav"), False)
print("finished")
