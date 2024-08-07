import os
import random
import shutil


# id2label = {
#     0: 'Btn-BuffSelect',
#     1: 'Btn-HeroUse',
#     2: 'Btn-ReturnMain',
#     3: 'Btn-Start',
#     4: 'Sta-CoExit',
#     5: 'Btn-Continue01',
#     6: 'Btn-Continue02',
#     7: 'Sta-Loading',
#     8: 'Sta-main',
#     9: 'Sta-Esc',
#     10: 'Sta-BuffSelect'
# }


"""
How to use
change the folder name 
"""

def select_and_move_images(source_folder, new_source_folder, percentage=10):
    """
    从每个图片文件夹中随机选择一定百分比的图片及对应的.txt标签文件到val文件夹中。

    :param source_folder: 原始数据文件夹路径
    :param val_folder: 验证集目标文件夹路径
    :param percentage: 要移动的图片的百分比 (默认10%)
    """
    if not os.path.exists(new_source_folder):
        os.makedirs(new_source_folder)
    new_path = os.path.join(new_source_folder, 'images')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_path = os.path.join(new_source_folder, 'labels')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_path = os.path.join(new_source_folder, 'images', 'train')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_path = os.path.join(new_source_folder, 'images', 'val')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_path = os.path.join(new_source_folder, 'labels', 'val')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_path = os.path.join(new_source_folder, 'labels', 'train')
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    for folder_name in os.listdir(source_folder):
        folder_path = os.path.join(source_folder, folder_name)
        if os.path.isdir(folder_path):
            # 获取该文件夹下所有的图片文件名
            images = [f for f in os.listdir(folder_path) if
                      os.path.isfile(os.path.join(folder_path, f)) and f.endswith(('.jpg', '.png', '.jpeg'))]
            num_val = max(1, len(images) * percentage // 100)  # 至少选择1张图片

            # 随机选择图片
            selected_images = random.sample(images, num_val)

            # 移动图片和对应的txt文件到val子目录
            for img_name in images:
                img_src = os.path.join(folder_path, img_name)
                txt_src = os.path.join(folder_path, 'labels', os.path.splitext(img_name)[0] + '.txt')

                shutil.copy(img_src, os.path.join(new_source_folder, 'images', 'train' if img_name not in selected_images else 'val'))
                if os.path.exists(txt_src):  # 确保txt文件存在才移动
                    shutil.copy(txt_src, os.path.join(new_source_folder, 'labels',
                                                      'train' if img_name not in selected_images else 'val'))

                else:
                    os.remove(img_src)
                    print(f'由于标签文件不存在，删除：{img_src}')

# 使用示例
source_data_folder = '../Cursor'
new_data_folder = '../data'
select_and_move_images(source_data_folder, new_data_folder)
