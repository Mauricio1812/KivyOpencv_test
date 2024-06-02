import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

class CameraApp(App):
    def build(self):
        self.img1 = Image()
        layout = self.img1
        self.capture = cv2.VideoCapture(0)
        self.capture1 = cv2.VideoCapture(2)
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        return layout

    def update(self, dt):
        ret, frame = self.capture.read()
        ret1, frame1 = self.capture1.read()

        if ret and ret1:
            # Resize frames to the same size
            reframe = cv2.resize(frame, (720, 720), interpolation=cv2.INTER_AREA)
            reframe1 = cv2.resize(frame1, (720, 720), interpolation=cv2.INTER_AREA)
            
            # Stack the frames side by side
            both = np.hstack((reframe, reframe1))
            
            # Convert it to texture
            buf1 = cv2.flip(both, 0)
            buf = buf1.tobytes()
            texture1 = Texture.create(size=(both.shape[1], both.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            
            # Display image from the texture
            self.img1.texture = texture1

    def on_stop(self):
        # Release the camera when the app stops
        self.capture.release()
        self.capture1.release()

if __name__ == '__main__':
    CameraApp().run()
