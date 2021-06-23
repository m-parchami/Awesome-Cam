# Gstreamer Capture

Here we want to capture frames from a Gstreamer pipeline. The element that does the main job is `appsink`. To put it simple: it **copies** the frames in the buffer and passes them to the code. Note that copying entire frames adds overhead to the pipeline. To avoid this, we must work with pointers. This can be achieved by turning your code into a gstreamer element, which can take time if you are new to Gstreamer, especially if you want to write your plugin in Python. Afterall, using `appsink` for small projects is much easier and sufficient.

## Installation

Your OpenCV binary must be able to work with Gstreamer pipelines. You can check this with the following code:

```Python
import cv2
print (cv2.getBuildInformation())
```
Check the field next to Gstreamer. If it says `Yes`, skip the rest of the installation part.

### Step 1: Install Gstreamer

Installing Gstreamer is relatively easy. 
For linux, [this page](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html?gi-language=c) may get the job done. 
For MacOS, you can use the following command:
```bash
brew install gstreamer gst-plugins-base gst-plugins-good gst-plugins-bad gst-plugins-ugly gst-libav
```

Test the installation with a simple pipeline:
```bash
gst-launch-1.0 autovideotestsrc ! autovideosink
```

### Step 2: Build OpenCV.

There are dozens of tutorials on this. I refrain from repeating them. There is just one thing you must add and keep an eye for:
When you are running the CMake command, make sure to use `-D WITH_GSTREAMER=ON` in your options. The CMake must be able to locate your Gstreamer's installation path by itself. In other cases, add `-D GSTREAMER_DIR=/path/to/gstreamer` to the options. The path can, for example be: "C:/gstreamer/1.0/x86_64"

If all goes right, in the summary that CMake generates, you must see `Yes` in front of the Gstreamer's field.

Follow the rest of build procedure as usual.

## Examples

For using Gstreamer together with OpenCV (via appsink), all you need to do is to pass a pipeline to the `cv2.videoCapture()`.

+ For reading from file you would write:
```Python 
cap = cv2.VideoCapture('uridecodebin uri=file:///home/amin/.../output.mp4 ! videoconvert ! appsink')
```
In these examples I use `uridecodebin` to take care of arranging decoding pipeline. You can of course use other elements instead.

+ For reading from camera devices such as webcam you would write:
```Python 
cap = cv2.VideoCapture('autovideosrc ! videoconvert ! appsink')
```
+ For having a quick test with an input stream you would write:
```Python
cap = cv2.VideoCapture('videotestsrc ! videoconvert ! appsink')
```

## Tips

1. Gstremaer is highly efficient for video processing. For one thing, all elements are run in separate threads! Therefore, it is recommended to implement your basic processes via the pipeline. For instance, if you always want to resize the input frames you can write this:
```Python
cap = cv2.VideoCapture('autovideosrc ! videoscale ! video/x-raw,width=800,height=400 ! videoconvert ! appsink')
```
2. Another benefit of writing implementing your logic as a Gstreamer element instead of using appsink is that you can insert this element in the middle of the pipeline. This way, on top of the performance boost (using pointers instead of duplicating frames), you can take advantage of other Gstreamer elements. For instance, you can send metadata via udpsink to a back-end API.
