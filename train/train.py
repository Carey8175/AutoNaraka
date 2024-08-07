import torch
from ultralytics import YOLO

def main():
    # 检查CUDA是否可用
    if not torch.cuda.is_available():
        raise SystemError("CUDA not available. Please check your PyTorch installation and GPU configuration.")

    # 加载YOLOv8模型
    model = YOLO('yolov8n.yaml')  # 加载预训练模型 yolov8n.pt

    # 确定设备/
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # 将模型移动到指定设备
    model.to(device)

    # 配置训练参数
    data = 'SnowMonster.yaml'
    epochs = 400

    # 开始训练并指定设备
    model.train(data=data, epochs=epochs, device=device, imgsz=640, batch=5)


if __name__ == '__main__':

    main()

