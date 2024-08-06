import ctypes
import numpy as np
import time
import torch
import cv2


class ScreenCapture:
    def __init__(self, box=None, _x=0, _y=0, _width=1, _height=1):
        self.hdc_screen = ctypes.windll.user32.GetDC(0)
        self.hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc_screen)
        self.bmi = BITMAPINFOHEADER()
        self.hbitmap = None
        if not box:
            self.width, self.height = self.get_screen_size()
        else:
            self.width, self.height = box
        self.x, self.y = int(0 + self.width * _x), int(0 + self.height * _y),
        self.width, self.height = int(self.width * _width), int(self.height * _height)
        self.setup_bitmap(self.width, self.height)

    def setup_bitmap(self, width, height):
        self.bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        self.bmi.biWidth = width
        self.bmi.biHeight = -height  # Negative to create a top-down DIB
        self.bmi.biPlanes = 1
        self.bmi.biBitCount = 32
        self.bmi.biCompression = BI_RGB
        self.hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(self.hdc_screen, width, height)
        ctypes.windll.gdi32.SelectObject(self.hdc_mem, self.hbitmap)

    def capture(self):
        ctypes.windll.gdi32.BitBlt(self.hdc_mem, 0, 0, self.width, self.height, self.hdc_screen, self.x, self.y,
                                   SRCCOPY)
        bitmap_bits = (ctypes.c_char * (self.width * self.height * 4))()
        ctypes.windll.gdi32.GetDIBits(self.hdc_mem, self.hbitmap, 0, self.height, bitmap_bits, ctypes.byref(self.bmi),
                                      DIB_RGB_COLORS)

        image = np.frombuffer(bitmap_bits, dtype=np.uint8).reshape((self.height, self.width, 4))
        # gray_image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
        # gray_to_3channel = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)

        # gray_to_3channel = cv2.cvtColor(cv2.cvtColor(np.frombuffer(bitmap_bits, dtype=np.uint8).reshape((self.height, self.width, 4)), cv2.COLOR_RGBA2GRAY), cv2.COLOR_GRAY2BGR)
        return image[:, :, :3]
        # return gray_to_3channel



    def release(self):
        ctypes.windll.gdi32.DeleteObject(self.hbitmap)
        ctypes.windll.gdi32.DeleteDC(self.hdc_mem)
        ctypes.windll.user32.ReleaseDC(0, self.hdc_screen)

    @staticmethod
    def get_screen_size():
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)
        height = user32.GetSystemMetrics(1)
        return width, height


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ("biSize", ctypes.c_uint32),
        ("biWidth", ctypes.c_int32),
        ("biHeight", ctypes.c_int32),
        ("biPlanes", ctypes.c_uint16),
        ("biBitCount", ctypes.c_uint16),
        ("biCompression", ctypes.c_uint32),
        ("biSizeImage", ctypes.c_uint32),
        ("biXPelsPerMeter", ctypes.c_int32),
        ("biYPelsPerMeter", ctypes.c_int32),
        ("biClrUsed", ctypes.c_uint32),
        ("biClrImportant", ctypes.c_uint32)
    ]


# Constants
SRCCOPY = 0x00CC0020
BI_RGB = 0
DIB_RGB_COLORS = 0

# Usage example
if __name__ == "__main__":
    capture = ScreenCapture()
    time.sleep(2)

    while True:
        start_time = time.time()
        screenshot = capture.capture()
        end_time = time.time()
        from PIL import Image

        img = Image.fromarray(screenshot)
        img.show()
        break

        print(f"Time taken: {end_time - start_time:.4f} seconds")


    # # If you need to save the screenshot for verification
    # from PIL import Image
    # img = Image.fromarray(screenshot)
    # img.save("screenshot.png")
