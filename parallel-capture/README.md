Here, we simply use multi-threading for reading and displaying images from a VideoCapture stream.

While we use a heavy processing algorithms, we add delays to our workflow. If the input capture and processes are done in sequence,
the capture's delay can add delay to the rest of the code. Similarly, other processes can lead to frame loss (in case of live streams).

A great approach can be to separate input capture from the rest of the code. This way, not only can we benefit from multi-threaded programming, but also we can increase our input FPS and lower the frame loss.

Here is a pseudo code that demonstrates the issue:

```
while True:
  ...
  img = cap.read()
  
  my_process(img)

  cv2.imshow('whatever',img) # also a process
  cv2.waitKey(1)
  ...
```

The problem is that every `my_process()` call is waiting for its previous `read()` to complete, and also every `read()` invocation is waiting for the previous captured frame to be processed and displayed.

On this approach we try to make these tasks separate, therefore we use the main thread for other processes and create a separate thread for reading the frames from the input stream. However, in order to avoid dropping too many frames, we buffer them using the Python's built-in queue module. 

The length of queue can be adjusted based on the setup. Setting it too small(e.g. 1), may result in frame loss. On the other hand, long queues may result in constant delays.

Please keep in mind that if your process is always slower than the input FPS, then frame loss is almost inevitable.

Best.

