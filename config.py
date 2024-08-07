MODEL_PATH = './models/l.pt'
ATTACK_MODEL_PATH = './models/ht-n.pt'

# 其他置信度
CONFIDENCE = 0.75
# 主动退出置信度
EXIT_CONFIDENCE = 0.9
EXIT_COUNT = 5

# 基础参数 -------------------------------------------------------
MESSAGE = '闺蜜的号，我第一次玩永杰，我尽力打，大佬饶命QWQ'     # 打招呼消息
BUFF_TIME = 20 * 60     # 两次灵诀时间若超过10分钟则退出
NO_MONSTER_TIMES = 3    # 特定次都没发现怪物，则按下锁敌键

# 攻击系统参数 ----------------------------------------------------
VISION_UNIT = 350    # 视角单次移动范围
ATTACK_CONFIDENCE = 0.45  # 游标模型置信度
CENTER_RANGE = 0.4  # 中心范围
MIN_ATTACK_DISTANCE = 0.35   # 最小攻击距离
MIN_DOOR_DISTANCE = 0.2   # 最小按门距离
VISION_RANGE_DICT = {
    0: -400,
    0.1: -300,
    0.2: -200,
    0.3: -100,
    0.4: -50,
    0.5: 0,
    0.6: 50,
    0.7: 200,
    0.8: 300,
    0.9: 400,
    1: 400
}

# 选择使用的英雄
HERO = 'ht'

# 间隔时间 (多久检测一次)
SPACE_TIME = 0.1

LABELS = {
    0: 'Btn-BuffSelect',
    1: 'Btn-HeroUse',
    2: 'Btn-ReturnMain',
    3: 'Btn-Start',
    4: 'Sta-CoExit',
    5: 'Btn-Continue01',
    6: 'Btn-Continue02',
    7: 'Sta-Loading',
    8: 'Sta-Main',
    9: 'Sta-Esc',
    10: 'Sta-BuffSelect',
    11: 'Sta-Dead'
}

ATTACK_LABELS = {
    0: 'Cursor',
    1: 'Store',
    2: 'SkillAvailable',
    3: 'SkillUsing',
    4: 'ExtremeSkill',
    5: 'DropMoney',
    6: 'Money',
    7: 'NextLevel'
}
