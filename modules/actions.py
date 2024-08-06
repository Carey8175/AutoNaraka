from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController
from pynput.mouse import Button
import time
import ctypes
import win32api


keyboard = Controller()
mouse = MouseController()


class Action:
    @staticmethod
    def zd(is_jump, is_c=False):
        if is_jump:
            with keyboard.pressed(Key.space):
                time.sleep(0.006)
                keyboard.press('g')
                time.sleep(0.001)
                keyboard.release('g')

        elif is_c:
            Action.c_zd()

        else:
            keyboard.press('g')
            time.sleep(0.001)
            keyboard.release('g')

    @staticmethod
    def c_zd():
        keyboard.press('c')
        keyboard.release('c')
        mouse.press(Button.left)
        mouse.press(Button.right)
        time.sleep(0.0001)
        mouse.release(Button.left)
        mouse.release(Button.right)

    @staticmethod
    def mouse_move(x, y, interval=10):
        MOUSEEVENTF_MOVE = 0x0001
        interval = - interval if x < 0 else interval

        for i in range(abs(x) // 10):
            # time.sleep(0.0005)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE, interval, y, 0, 0)  # 将 x 和 y 作为目标位置传递给 mouse_event 函数


    @staticmethod
    def move_mouse_to_absolute_position(dest_x, dest_y):
        MOUSEEVENTF_MOVE = 0x0001
        MOUSEEVENTF_ABSOLUTE = 0x8000
        # 获取屏幕分辨率
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)

        print(screen_width // 2)
        print(screen_height // 2)
        dest_x = screen_width // 2 + 93
        dest_y = screen_height // 2 + 54
        # 将目标位置的坐标转换为绝对坐标
        absolute_x = int(dest_x * 65535 / screen_width)
        absolute_y = int(dest_y * 65535 / screen_height)
        x0, y0 = win32api.GetCursorPos()
        print('x: ', x0, 'y: ', y0)

        # 移动鼠标到绝对坐标的位置
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_MOVE, absolute_x, absolute_y, 0, 0)
        x, y = win32api.GetCursorPos()
        print('x: ', x, 'y: ', y)

    @staticmethod
    def click(x, y):
        mouse.position = (x, y)
        mouse.click(Button.left)

    @staticmethod
    def box_click(box, flag='left', duration=0):
        xyxy = box.xyxy.tolist()[0]

        center_x = (xyxy[0] + xyxy[2]) / 2
        center_y = (xyxy[1] + xyxy[3]) / 2

        mouse.position = (center_x, center_y)
        time.sleep(duration)
        if flag == 'left':
            mouse.click(Button.left)
        elif flag == 'right':
            mouse.click(Button.right)
        elif flag == 'middle':
            mouse.click(Button.middle)
        else:
            raise KeyError('flag does not exist')

    @staticmethod
    def hold_attack(hero_name='jn'):
        record_time = {
            'sm': [0.75, 2],
            'hy': [0.75, 1],
            'jch': [0.75, 2],
            'th': [0.75, 2],
            'tme': [1, 2],
            'ht': [0.75, 1],
            'csn': [0.75, 2.5],
            'ys': [0.75, 2],
            'wc': [0.75, 1.5],
            'jn': [0.75, 0.3]
        }

        Action.run(0.5)
        if hero_name in ['sm', 'hy', 'tme', 'ht', 'csn', 'ys', 'jn']:
            mouse.press(Button.left)
            time.sleep(record_time[hero_name][0])
            mouse.release(Button.left)
            time.sleep(0.5)
            mouse.press(Button.right)
            time.sleep(0.1)
            mouse.release(Button.right)
            time.sleep(record_time[hero_name][1] / 2)
        elif hero_name in ['jch', 'th', 'wc']:
            mouse.press(Button.right)
            time.sleep(record_time[hero_name][0])
            mouse.release(Button.right)
            time.sleep(0.5)
            mouse.press(Button.left)
            time.sleep(0.1)
            mouse.release(Button.left)
            time.sleep(record_time[hero_name][1] / 2)

    @staticmethod
    def run(duration):
        keyboard.press('w')
        keyboard.press(Key.shift)
        time.sleep(duration)
        keyboard.release('w')
        keyboard.release(Key.shift)

    @staticmethod
    def auto_seek():
        """
        自动锁敌
        :return:
        """
        keyboard.press('`')
        time.sleep(0.01)
        keyboard.release('`')


if __name__ == '__main__':
    time.sleep(5)
    mouse.click(Button.middle)



