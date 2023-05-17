#!/usr/bin/env python3.8

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import face_recognition
import os

class FaceRecognitionNode:
    def __init__(self):
        self.bridge = CvBridge()
        self.known_faces = {}
        self.unknown_faces_dir = "../data/known_faces"
        self.image_sub = rospy.Subscriber("/usb_cam_node/image_raw", Image, self.image_callback)
        self.faces_image_service = rospy.Service('faces_image', String, self.faces_image_service_callback)
        self.faces_names_service = rospy.Service('faces_names', String, self.faces_names_service_callback)
        self.capture_unknown_face_service = rospy.Service('capture_unknown_face', String, self.capture_unknown_face_service_callback)

    def load_known_faces(self):
        for file_name in os.listdir(self.unknown_faces_dir):
            if file_name.endswith(".jpg"):
                name = os.path.splitext(file_name)[0]
                image_path = os.path.join(self.unknown_faces_dir, file_name)
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                self.known_faces[name] = face_encoding

    def _display_results(self, matchs, face_locations, frame):
        # Display the results

        face_names = [val if valid else 'unkown' for val, valid in zip(self.known_faces.keys(), matchs)]

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            return frame

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            face_locations = face_recognition.face_locations(cv_image)
            face_encodings = face_recognition.face_encodings(cv_image, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # TODO: Implement face recognition here


                matchs = face_recognition.compare_faces(self.known_faces.values, face_encoding)
            
            imgFinal = self._display_results(matchs, face_locations, cv_image)
                # for name, knownFace in self.known_faces.items():
                #     match = face_recognition.compare_faces([knownFace], face_encoding)

                #     if match[0]:
                #         name = "Leo"

                #     face_names.append(name)
                
            return imgFinal
        
        except Exception as e:
            rospy.logerr("Error processing image: {0}".format(e))

    def faces_image_service_callback(self, req):
        # TODO: Implement returning the frame with recognized faces
        pass

    def faces_names_service_callback(self, req):
        # TODO: Implement returning the names of recognized faces
        pass

    def capture_unknown_face_service_callback(self, req):
        # TODO: Implement capturing and saving the unknown face with a name
        pass

def main():
    rospy.init_node('face_recognition_node')
    face_recognition_node = FaceRecognitionNode()
    face_recognition_node.load_known_faces()
    rospy.spin()

if __name__ == '__main__':
    main()