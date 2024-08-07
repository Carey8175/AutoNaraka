import random
import threading

from config import *
from modules.screen import ScreenCapture
from modules.actions import Action
from modules.display import MessageDisplay

import time
import torch
from ultralytics import YOLO
from pynput.keyboard import Controller, Key
from pynput.mouse import Listener as MouseListener


class CaNaraka:
    def __init__(self):
        print('initializing')
        # ------------------------------
        # init the keyboard controller
        self.keyboard = Controller()
        mouse_listener = MouseListener(on_click=self.on_click)
        mouse_listener.start()
        # ------------------------------
        # init running parameters
        self.enable_ca_naraka = False
        self.status = 'Sta-Main'
        # ------------------------------
        # init the screen capture
        self.screen_capture = ScreenCapture(None)
        # ------------------------------
        # init message displayer
        self.message_displayer = MessageDisplay()
        # ------------------------------
        # init model
        self.model = YOLO(MODEL_PATH, verbose=False)
        self.model.to('cuda' if torch.cuda.is_available() else 'cpu')
        # -----------------------------
        # start
        self.start()

    def on_click(self, x, y, button, pressed):

        if button.name == 'x2' and pressed:
            self.enable_ca_naraka = not self.enable_ca_naraka
            self.message_displayer.print_message(f'状态更改：{self.enable_ca_naraka}')
        if button.name == 'x1' and pressed:
            self.keyboard.press('g')
            time.sleep(0.001)
            self.keyboard.release('g')

    def decision(self, result):
        result = result[0]
        # boxes_num = len(result.boxes)
        # if boxes_num <= 0:
        #     return '无目标'

        labels_boxes = {}
        for box in result.boxes:
            if float(box.conf) >= CONFIDENCE:
                # AcceptMission
                if LABELS[int(box.cls)] == 'Btn-AcceptMission':
                    labels_boxes[LABELS[int(box.cls)]] = box
                elif LABELS[int(box.cls)] != 'Sta-CoExit':
                    labels_boxes[LABELS[int(box.cls)]] = box

        # # 状态自更新
        if 'Btn-Continue01' in labels_boxes.keys():
            self.status = 'Sta-Exit'
        # elif 'Btn-HeroUse' in labels_boxes.keys():
        #     self.status = 'Sta-HeroChoose'

        # 决策流程 -------------------------------------------------------
        """
        Status:
            Sta-Main: 主菜单
            Sta-HeroChoose: 英雄选择
            Sta-InGame: 进入游戏后
            Sta-Exit: 退出游戏
        """
        # 大厅状态下决策流程 ----------------------------------------------
        if self.status == 'Sta-Main':
            # 开始游戏
            if 'Btn-Start' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-Start'])
                # 预期的下一个状态
                self.status = 'Sta-HeroChoose'
                return '开始游戏'

        # 英雄选择状态下的流程 ---------------------------------------------
        elif self.status == 'Sta-HeroChoose':
            if 'Btn-HeroUse' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-HeroUse'])
                self.status = 'Sta-Loading'
                return '已选择英雄'

            elif 'Sta-InGame' in labels_boxes.keys():
                self.status = 'Sta-InGame'
                return 'Game Start'

        # 游戏状态下的流程 ---------------------------------------------
        elif self.status == 'Sta-InGame':
            if 'Sta-Esc' in labels_boxes.keys():
                self.keyboard.press(Key.esc)
                self.keyboard.release(Key.esc)
                return '跳过出厂动画'

            # 游戏正常结束
            elif 'Btn-Continue01' in labels_boxes.keys() or 'Btn-Continue02' in labels_boxes.keys():
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)
                self.status = 'Sta-Exit'
                time.sleep(1)  # 防止点击失效
                return '继续'

            elif 'Sta-Success' in labels_boxes.keys():
                self.keyboard.press(Key.esc)
                self.keyboard.release(Key.esc)

                self.status = 'Sta-Exit'

                return 'Game Success'

            else:
                # pass

                return '攻击策略'

        # 退出状态下的流程 ---------------------------------------------
        elif self.status == 'Sta-Exit':
            if 'Btn-ReturnMain' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-ReturnMain'])
                time.sleep(2)
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)
                return '返回大厅'

            elif 'Btn-Continue01' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-Continue01'])
                self.continued = True
                time.sleep(1)  # 防止点击失效
                # 防止额外的东西弹出，阻塞进程
                for i in range(5):
                    self.keyboard.press(Key.space)
                    self.keyboard.release(Key.space)
                    Action.click(100, 100)
                    time.sleep(10)
                return '继续01'

            elif 'Btn-Continue02' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-Continue02'])
                self.continued = True
                time.sleep(1)  # 防止点击失效
                return '继续02'

            elif 'Btn-Start' in labels_boxes.keys() and self.continued:
                self.status = 'Sta-Main'

                return '大厅'

    def start(self):
        self.message_displayer.print_message('CaNaraka is ready!')
        while True:
            if not self.enable_ca_naraka:
                time.sleep(0.1)
                continue
            # 捕获屏幕
            time0 = time.time()
            img_np = self.screen_capture.capture()

            # 使用YOLOv8模型进行预测
            results = self.model.predict(img_np)

            res = self.decision(results)
            if res:
                self.message_displayer.print_message(f'Action: {res}')
            else:
                self.message_displayer.print_message(f'Status: {self.status}')


if __name__ == '__main__':
    ca = CaNaraka()
