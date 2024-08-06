import time
import tkinter as tk
import ctypes
import threading
import win32api
import win32gui
import win32con

class MessageDisplay:
    def __init__(self, initial_message="这是一个置顶显示的消息"):
        self.current_message = initial_message
        self.root = None
        self.label = None
        self.thread = None
        self.start()

    def make_window_transparent(self, window):
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x00080000)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, 255, 0x2)

    def display_message_topmost(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # 去掉窗口边框
        self.root.attributes('-topmost', True)  # 置顶窗口
        self.root.attributes('-transparentcolor', 'white')  # 设置透明色
        # self.root.attributes('-alpha', 0.5)  # 设置透明度，0为完全透明，1为完全不透明

        # 创建标签并设置字体和颜色
        font_style = ("Times New Roman", 38)
        self.label = tk.Label(self.root, text=self.current_message, font=font_style, fg="red", bg="white")


        # 获取屏幕宽高并将窗口放置在右上角
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.label.winfo_reqwidth()
        window_height = self.label.winfo_reqheight()
        position_right = screen_width - window_width - 50  # 距离屏幕右边缘50像素
        position_up = 50  # 距离屏幕上边缘50像素
        self.label.place(x=0, y=0, width=window_width, height=window_height)
        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_up}')

        self.make_window_transparent(self.root)

        self.root.mainloop()

    def print_message(self, message):
        if self.label:
            self.label.config(text=message)


    def start(self):
        self.thread = threading.Thread(target=self.display_message_topmost)
        self.thread.daemon = True
        self.thread.start()
        time.sleep(0.5)

    @staticmethod
    def draw_bounding_box_with_annotation(box, text, color=(0, 255, 0), recycle=20):
        """
        在屏幕上绘制带有文字批注的bounding box.

        参数:
        box -- bounding box的xyxy坐标 (x_min, y_min, x_max, y_max)
        text -- 要显示的批注文本
        color -- 绘制bounding box的颜色 (默认绿色)
        """
        hwnd = win32gui.GetDesktopWindow()
        hdc = win32gui.GetWindowDC(hwnd)

        x_min, y_min, x_max, y_max = box
        x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)
        pen_color = win32api.RGB(color[0], color[1], color[2])

        # 创建画笔
        pen = win32gui.CreatePen(win32con.PS_SOLID, 2, pen_color)
        old_pen = win32gui.SelectObject(hdc, pen)

        # 绘制批注文本
        win32gui.SetTextColor(hdc, pen_color)
        win32gui.SetBkMode(hdc, win32con.TRANSPARENT)
        text_rect = (x_min, y_min - 20, x_max, y_min)

        for i in range(recycle):
            win32gui.Rectangle(hdc, x_min, y_min, x_max, y_max)
            win32gui.DrawText(hdc, text, -1, text_rect, win32con.DT_CENTER | win32con.DT_NOCLIP)

        # 恢复旧的画笔并删除新创建的画笔
        win32gui.SelectObject(hdc, old_pen)
        win32gui.DeleteObject(pen)
        win32gui.ReleaseDC(hwnd, hdc)

# 示例调用
if __name__ == "__main__":
    MessageDisplay.draw_bounding_box_with_annotation(
        [100,100,200,200],
        'test'
    )
