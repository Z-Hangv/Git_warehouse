import xbase as xconfig
import cv2
import time
import tool.xsock as xsock
import numpy as np


class Face_detect:
    def init(self):
        self.classifier = cv2.CascadeClassifier(xconfig.get_cv2_file_path("haarcascade_frontalface_default.xml"))

    def get_faces_from_file(self, image_file_path_):
        img = cv2.imread(image_file_path_)  # 读取图片
        return self.get_faces_from_img(img)

    def get_faces_from_img(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换灰色

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 调用识别人脸
        faceRects = self.classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        return faceRects

    def draw_face(self, image_file_path_, faces_):
        img = cv2.imread(image_file_path_)  # 读取图片
        color = (0, 255, 0)  # 定义绘制颜色
        if len(faces_):  # 大于0则检测到人脸
            for faceRect in faces_:  # 单独框出每一张人脸
                x, y, w, h = faceRect
                # 框出人脸
                cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)
                # 左眼
                cv2.circle(img, (x + w // 4, y + h // 4 + 30), min(w // 8, h // 8), color)
                # 右眼
                cv2.circle(img, (x + 3 * w // 4, y + h // 4 + 30), min(w // 8, h // 8), color)
                # 嘴巴
                cv2.rectangle(img, (x + 3 * w // 8, y + 3 * h // 4), (x + 5 * w // 8, y + 7 * h // 8), color)
        cv2.imshow("image", img)  # 显示图像
        c = cv2.waitKey(10)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



class Video_cap:
    last_time_face_status = False  #上次发送的数据如果是没人, 则不用再发了

    def send_face_data(self, faces_):
        if len(faces_) <= 0:
            if self.last_time_face_status :  #上次有人脸
                m = {}
                m["action"] = "face_detection"
                m["find"] = 0  # 没有人脸
                m["x"] = 0
                m["y"] = 0
                m["w"] = 0
                m["h"] = 0
                xsock.send_sock(xconfig.script_server.ip, xconfig.script_server.sock_port, str(m))
                self.last_time_face_status =False
                return
            else: # 什么都没做
                return
        else:
            # 找到最大的脸
            biggest_face = np.zeros(4, dtype=int)
            # print(biggest_face)
            # print(type(biggest_face))
            for faceRect in faces_:  # 单独框出每一张人脸
                # biggest_face =
                # print(faceRect)
                # print(type(faceRect))
                if biggest_face[3] < faceRect[3]:  # 第四个数据, 应该是h
                    biggest_face = faceRect
            x, y, w, h = biggest_face
            m = {}
            m["action"] = "face_detection"
            m["find"] = 1  # 没有人脸
            m["x"] = x
            m["y"] = y
            m["w"] = w
            m["h"] = h
            print(m)
            xsock.send_sock(xconfig.script_server.ip, xconfig.script_server.sock_port, str(m))
            self.last_time_face_status = True


    def run(self):
        self.face_detect = Face_detect()
        print("init face CascadeClassifier")
        self.face_detect.init()
        print("open video capture")
        cap = cv2.VideoCapture(0)
        print("starting...")
        while (True):
            time.sleep(1)
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret == False:
                print("please check the video cap is working")
                break
            faces = self.face_detect.get_faces_from_img(frame)
            self.send_face_data(faces)

            # if len(faces) > 0:
            #     print("发现{0}个目标!".format(len(faces)))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + w), (0, 255, 0), 2)

            cv2.imshow("frame", frame)
            # Display the resulting frame
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        # cap.release()
        # cv2.destroyAllWindows()

if __name__ == '__main__':
    v =Video_cap()
    v.run()


    # face_image = xconfig.get_cv2_file_path("hy2.jpg")
    # f = Face_detect()
    # f.init()
    # faces = f.get_faces_from_file(face_image)
    # f.draw_face(face_image, faces)




#
# filepath = xconfig.get_cv2_file_path("cv.jpg")
# img = cv2.imread(filepath) # 读取图片
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 转换灰色
# # OpenCV人脸识别分类器
# classifier = cv2.CascadeClassifier( xconfig.get_cv2_file_path("haarcascade_frontalface_default.xml"))
# color = (0, 255, 0) # 定义绘制颜色
# # 调用识别人脸
# faceRects = classifier.detectMultiScale( gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
#
# if len(faceRects): # 大于0则检测到人脸
#     for faceRect in faceRects: # 单独框出每一张人脸
#         x, y, w, h = faceRect
#         # 框出人脸
#         cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)
#         # 左眼
#         cv2.circle(img, (x + w // 4, y + h // 4 + 30), min(w // 8, h // 8), color)
#         #右眼
#         cv2.circle(img, (x + 3 * w // 4, y + h // 4 + 30), min(w // 8, h // 8), color)
#         #嘴巴
#         cv2.rectangle(img, (x + 3 * w // 8, y + 3 * h // 4), (x + 5 * w // 8, y + 7 * h // 8), color)
# cv2.imshow("image", img) # 显示图像
# c = cv2.waitKey(10)
# cv2.waitKey(0)
# cv2.destroyAllWindows()