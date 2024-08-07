import cv2


def extract_frames(video_path, output_folder, video_order):
    # 打开视频文件
    video_capture = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not video_capture.isOpened():
        print("Error: Failed to open video file.")
        return

    # 逐帧读取视频并导出图像
    frame_count = 0
    while True:
        # if frame_count % 5 != 0:
        #     continue
        # 读取一帧图像
        ret, frame = video_capture.read()

        # 检查是否成功读取到帧
        if not ret:
            break

        # 生成图像文件名
        frame_filename = f"{output_folder}/{video_order}_frame_{frame_count:04d}.jpg"

        # 保存帧图像
        if frame_count % 2 == 0:
            cv2.imwrite(frame_filename, frame)

        # 更新帧计数
        frame_count += 1

    # 关闭视频文件
    video_capture.release()
    print(f"Frames extracted: {frame_count}")

# 6
video_order = '47'
# 视频文件路径
# video_path = rf"../data/video/{video_order}.mp4"
video_path = (f'./videos/{video_order}.mp4')
# 输出文件夹路径
output_folder = "./images"

# 创建输出文件夹（如果不存在）
# import os
#
# os.makedirs(output_folder, exist_ok=True)

# 调用函数，将视频导出为一帧帧的图像
for video_order in range(1, 15):
    video_path = (f'./videos/47.mp4')
    print(video_path)
    extract_frames(video_path, output_folder, 47)
    break
