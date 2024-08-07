MODEL_PATH = './models/l.pt'

# 其他置信度
CONFIDENCE = 0.75

# 选择使用的英雄
HERO = 'hy'

# 历史遗留问题，标签有冗余
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
    11: 'Sta-Dead',
    12: 'Sta-InGame',
    13: 'Sta-Success',
    14: 'Btn-AcceptMission',
    15: 'Btn-Transport'
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
