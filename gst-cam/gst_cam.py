import cv2

if __name__ == "__main__":

    
    
    # For capturing webcam
    gstreamer_pipeline = "autovideosrc ! videoconvert ! appsink"

    # # For resizing input frames 
    # # Note: The "! video/x-raw.... !" is not an element. These are Caps. Refer to Gstreamer documentation for more info)
    # gstreamer_pipeline = 'autovideosrc ! videoscale ! video/x-raw,width=800,height=400 ! videoconvert ! appsink'
    
    # # For capturing from file
    # gstreamer_pipeline = "uridecodebin uri=file://[Your file] ! videoconvert ! appsink"
    # gstreamer_pipeline = "uridecodebin uri=file:///home/amin/personal/KNTU_CV_2021/output.mp4 ! videoconvert ! appsink"
    
    # # For capturing from rtsp (e.g. Network Cameras)
    # gstreamer_pipeline = "uridecodebin uri=rtsp://[Password]:[Username]@[IP]:[Port]/[Path] ! videoconvert ! appsink

    # # For a quick test
    # gstreamer_pipeline = 'videotestsrc ! videoconvert ! appsink'
    
    cap = cv2.VideoCapture(gstreamer_pipeline)
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        cv2.imshow("Gst Cam", frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key ==  ord('q'):
            break

    cv2.destroyAllWindows()
