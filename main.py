import random
import threading

from config import *
from modules.screen import ScreenCapture
from modules.actions import Action
from modules.display import MessageDisplay


import time
import torch
import pyperclip
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
        self.continued = False      # 用于退出时检测是否按过继续，不能删除
        self.send_message = 0
        self.last_buff_select = time.time()
        self.no_monster_count = 0       # 多少次检测都没有怪物，连续特定次数后按下自动锁敌
        self.last_attack_status = None  # 用于记录上次是否是丢弃金币，防止金币为零卡住bug
        self.exit_count = 0
        # ------------------------------
        # init the screen capture
        self.screen_capture = ScreenCapture(None)
        # ------------------------------
        # init message displayer
        self.message_displayer = MessageDisplay()
        # ------------------------------
        # init model
        self.model = YOLO(MODEL_PATH, verbose=False)
        self.atk_model = YOLO(ATTACK_MODEL_PATH, verbose=False)
        self.model.to('cuda' if torch.cuda.is_available() else 'cpu')
        self.atk_model.to('cuda' if torch.cuda.is_available() else 'cpu')
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
                if LABELS[int(box.cls)] == 'Sta-CoExit' and float(box.conf) >= EXIT_CONFIDENCE:
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
            Sta-Loading: 进入游戏前
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
                self.exit_count = 0
                return '开始游戏'

        # 英雄选择状态下的流程 ---------------------------------------------
        elif self.status == 'Sta-HeroChoose':
            if 'Btn-HeroUse' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-HeroUse'])
                self.status = 'Sta-Loading'
                return '已选择英雄'

        # 加载状态下的流程 ---------------------------------------------
        elif self.status == 'Sta-Loading':
            if 'Sta-Loading' in labels_boxes.keys():
                self.status = 'Sta-InGame'
                return '加载游戏中'

        # 游戏状态下的流程 ---------------------------------------------
        elif self.status == 'Sta-InGame':
            if 'Btn-BuffSelect' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-BuffSelect'])
                self.last_buff_select = time.time()
                return '已选择一个灵诀'

            elif 'Sta-CoExit' in labels_boxes.keys() or time.time() - self.last_buff_select >= BUFF_TIME:
                if self.exit_count >= EXIT_COUNT:
                    time.sleep(5)
                    self.keyboard.press(Key.esc)
                    time.sleep(0.1)
                    self.keyboard.release(Key.esc)
                    self.status = 'Sta-Exit'
                    print('准备退出游戏')
                    self.exit_count = 0
                    return '准备退出游戏'

                else:
                    self.exit_count += 1
                    time.sleep(5)

                    return self.exit_count

            elif 'Sta-Esc' in labels_boxes.keys():
                # self.keyboard.press(Key.esc)
               	#  self.keyboard.release(Key.esc)
                return '跳过出厂动画'

            # 游戏正常结束
            elif 'Btn-Continue01' in labels_boxes.keys() or 'Btn-Continue02' in labels_boxes.keys():
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)
                self.status = 'Sta-Exit'
                self.continued = True
                time.sleep(1)  # 防止点击失效
                return '继续'

            else:
                if self.send_message == 40:
                    # 打招呼信息
                    time.sleep(1)
                    pyperclip.copy(MESSAGE)
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)

                    time.sleep(1)
                    self.keyboard.press(Key.ctrl_l)
                    self.keyboard.press('v')
                    self.keyboard.release(Key.ctrl_l)
                    self.keyboard.release('v')

                    time.sleep(1)
                    self.keyboard.press(Key.enter)
                    self.keyboard.release(Key.enter)

                self.send_message += 1
                return '攻击策略'

        # 退出状态下的流程 ---------------------------------------------
        elif self.status == 'Sta-Exit':
            if 'Btn-ReturnMain' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-ReturnMain'])
                time.sleep(2)
                self.keyboard.press(Key.space)
                self.keyboard.release(Key.space)
                return '返回大厅'

            elif 'Btn-BuffSelect' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-BuffSelect'])
                self.status = 'Sta-InGame'

                return '灵诀选择，重置状态'


            elif 'Btn-Continue01' in labels_boxes.keys():
                Action.box_click(labels_boxes['Btn-Continue01'])
                self.continued = True
                time.sleep(1)   # 防止点击失效
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

            elif 'Sta-Main' in labels_boxes.keys() and self.continued:
                self.status = 'Sta-Main'
                self.continued = False
                self.send_message = 0
                return '大厅'

    def atk_decision(self, results):
        result = results[0]

        labels_boxes = {}
        for box in result.boxes:
            if ATTACK_LABELS[int(box.cls)] == 'Cursor' and float(box.conf) >= ATTACK_CONFIDENCE:
                labels_boxes[ATTACK_LABELS[int(box.cls)]] = box

            elif ATTACK_LABELS[int(box.cls)] == 'SkillAvailable' and float(box.conf) >= CONFIDENCE:
                labels_boxes[ATTACK_LABELS[int(box.cls)]] = box

            elif ATTACK_LABELS[int(box.cls)] == 'SkillUsing' and float(box.conf) >= CONFIDENCE:
                labels_boxes[ATTACK_LABELS[int(box.cls)]] = box

            elif ATTACK_LABELS[int(box.cls)] == 'ExtremeSkill' and float(box.conf) >= CONFIDENCE:
                labels_boxes[ATTACK_LABELS[int(box.cls)]] = box

            elif ATTACK_LABELS[int(box.cls)] == 'NextLevel' and float(box.conf) >= CONFIDENCE:
                labels_boxes[ATTACK_LABELS[int(box.cls)]] = box

            elif ATTACK_LABELS[int(box.cls)] == 'DropMoney' and float(box.conf) >= CONFIDENCE:
                labels_boxes[ATTACK_LABELS[int(box.cls)]] = box

            elif ATTACK_LABELS[int(box.cls)] == 'Money' and float(box.conf) >= CONFIDENCE:
                labels_boxes[ATTACK_LABELS[int(box.cls)]] = box

        # 无目标策略
        if len(labels_boxes) <= 0:
            self.no_monster_count += 1

            # 特定次数后都未发现怪物，按下索敌键
            if self.no_monster_count >= NO_MONSTER_TIMES:
                Action.auto_seek()
                time.sleep(0.3)
                self.no_monster_count = 0
                return '按下锁敌键'

            if random.randint(0, 1) == 1:
                # threading.Thread(target=Action.run, args=(1, )).start()
                Action.run(1)

            Action.mouse_move(VISION_UNIT, 0)
            time.sleep(0.2)

            return f'第{self.no_monster_count}次无目标'

        if 'NextLevel' in labels_boxes.keys():
            # 睡眠等待
            time.sleep(3)
            # 打开背包
            self.keyboard.press(Key.tab)
            time.sleep(0.1)
            self.keyboard.release(Key.tab)

            return '进入下一关'

        elif 'Money' in labels_boxes.keys():
            Action.box_click(labels_boxes['Money'], flag='right', duration=0.1)
            Action.box_click(labels_boxes['Money'], flag='middle', duration=0.1)
            time.sleep(0.5)

            self.keyboard.press(Key.tab)
            time.sleep(0.1)
            self.keyboard.release(Key.tab)
            time.sleep(0.2)

            return '示意金币，关闭背包'

        elif 'DropMoney' in labels_boxes.keys():
            if self.last_attack_status != 'DropMoney':
                for i in range(10):
                    Action.box_click(labels_boxes['DropMoney'], flag='right')
                    time.sleep(0.2)

                self.last_attack_status = 'DropMoney'

                return '丢弃金币'

            else:
                self.keyboard.press(Key.tab)
                time.sleep(0.1)
                self.keyboard.release(Key.tab)
                time.sleep(0.2)

                self.last_attack_status = None

                return '关闭背包'

        elif 'SkillAvailable' in labels_boxes.keys():
            self.keyboard.press('f')
            time.sleep(0.1)
            self.keyboard.release('f')

            return '释放f'

        elif 'SkillUsing' in labels_boxes.keys():
            Action.mouse_move(VISION_UNIT, 0)
            threading.Thread(target=Action.run, args=(2,)).start()
            time.sleep(0.2)

            # 打药
            if random.randint(0, 1):
                self.keyboard.press('4' if random.randint(0, 1) else '5')
                time.sleep(0.1)
                self.keyboard.press('4' if random.randint(0, 1) else '5')
                time.sleep(2.4)

                return '技能正在释放（打药）'
            # 小跳
            else:
                for i in range(random.randint(1, 4)):
                    self.keyboard.press(Key.space)
                    time.sleep(0.1)
                    self.keyboard.release(Key.space)

                    return '技能正在释放'

        elif 'ExtremeSkill' in labels_boxes.keys():
            self.keyboard.press('v')
            time.sleep(0.1)
            self.keyboard.release('v')

            return '释放大招'

        elif 'Cursor' in labels_boxes.keys():
            for i in range(random.randint(1, 5)):
                Action.hold_attack(HERO)

            return '攻击'

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

            if self.status == 'Sta-InGame' and res in ['攻击策略', '跳过出厂动画']:
                results = self.atk_model.predict(img_np)
                res = self.atk_decision(results)
                if res:
                    self.message_displayer.print_message(f'Attack: {res}')
                else:
                    self.message_displayer.print_message(f'Status: {self.status}')


            time.sleep(SPACE_TIME)


if __name__ == '__main__':
    ca = CaNaraka()
