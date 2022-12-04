import  cv2
import numpy as np
import face_recognition

video_capture=cv2.VideoCapture(0)


# we store picture to database
K_image=face_recognition.load_image_file("Python Project/image/Kartik1.jpg")
s_image=face_recognition.load_image_file("Python Project/image/Shubham.jpg")
K_face_encoding=face_recognition.face_encodings(K_image)[0]
S_face_encoding=face_recognition.face_encodings(s_image)[0]

known_face_encoding=[K_face_encoding,S_face_encoding]
face_name=["Kartik","Shubham"]

# known_face_encoding=[S_face_encoding]
# face_name=["Shubham"]

# print(K_face_encoding)


#From video we doing
while(True):
    ret, frame=video_capture.read()
    
    # Convert the image from BGR color  to RGB color
    rgb_frame=frame[:,:,::-1]
    face_location=face_recognition.face_locations(rgb_frame)
    face_encoding=face_recognition.face_encodings(rgb_frame,face_location)

    for(top,right,bottom,left),face_encoding in zip(face_location,face_encoding):
        matches=face_recognition.compare_faces(known_face_encoding,face_encoding)
        name="Unknown"

        face_distance=face_recognition.face_distance(known_face_encoding,face_encoding)

        best_match_index=np.argmin(face_distance)
        if matches[best_match_index]:
            name=face_name[best_match_index]

        #Making rectangle around face
        cv2.rectangle(frame,(left,top),(right,bottom),(0,0,0),2)

        cv2.rectangle(frame,(left,bottom-35),(right,bottom),(0,0,0),cv2.FILLED)
        font=cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,name,(left+6,bottom-6),font,1.0,(255,255,255),1)
    cv2.imshow("Face Recognition",frame)

    # This statement just runs once per frame.if we press key "q" it will exit the while loop with a break,
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()



