import serial
import time
import script_server.task_script as task_script
# import protocol

com_port = "com4"

if __name__ == '__main__':

    serial_handle = serial.Serial(com_port, 115200, timeout=1)

    print("connect %s..." % com_port)
    while True:
        try:
            time.sleep(0.1)
            count = serial_handle.inWaiting()
            if count == 0:
                continue
            if count != 3:
                print("收到数据不完整, count = %d" % count)
                continue
            if count == 3:
                print("count: %d"% count)
                rec_byte = serial_handle.read(count)
                print("收到串口数据:");
                a  = str(rec_byte[1:3].hex())
                b = int(a, 16)
                c = str(rec_byte.hex())
                c = c[0:2]
                param = c + str(b)
                print(param)
                task_script.run_os_script_file("voice_respond",  5, param)
                # protocol.run_module("voice_respond", rec_str, 1)
                #

        except Exception as e:
            print("exception happened: ")
            print(e)
            pass

