import cv2
import queue
from threading import Thread
class Stream:

    def __init__(self, source = 0):

        self.cap = cv2.VideoCapture(source)
        self.current_size = 0
        if not self.cap.isOpened():

            print('something went wrong while openning source')
            exit(0)

        self.release = False


    def start(self, queue_size = 1):

        self.frame_queue = queue.Queue(queue_size)
        Thread(target = self.flow).start()
            
    def flow(self):
        
        while True:
            
            if self.release:
                break
            
            if self.frame_queue.full():
                print('missed a frame because queue is full!')
                continue
            
            ok, frame = self.cap.read()
        
            if not ok:
                print('no more frames from source!')
                self.stop()
                
            self.frame_queue.put(frame)
            self.current_size += 1
        exit(0)

    def read(self):
        self.current_size -= 1
        return self.frame_queue.get()
    
    
    def stop(self):
        self.release = True
        

if __name__ == '__main__':
    buffer_size = 10
    # For default camera source (usually the webcam)
    source = 0
    # Using Gstreamer pipeline
    # source = 'autovideosrc ! videoconvert ! appsink'
    stream = Stream(source)
    stream.start(buffer_size)

    while True:

        img = stream.read()
        
        img = cv2.putText(img, 'queue len: '+ str(stream.current_size), (50,50), cv2.FONT_HERSHEY_SIMPLEX,  1, (0,0,255), 2, cv2.LINE_AA)
        
        cv2.imshow('webcam',img)
        key = cv2.waitKey(1)

        if key & 0xFF == ord('q'):

            stream.stop()
            break

    cv2.destroyAllWindows()
        

    
