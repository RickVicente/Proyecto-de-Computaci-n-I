from ultralytics import YOLO

# Carga el modelo base YOLOv9 (puedes usar -n, -s, -m, -l según tu GPU)
model = YOLO("yolov9c.pt")  # o "yolov9e.pt" si tienes buena GPU

# Entrena con tu dataset
model.train(
    data="vehicles.yaml",  # ruta a tu archivo YAML
    epochs=100,            # número de épocas (puedes subir a 200)
    imgsz=1280,            # resolución de entrada (aumenta si tienes VRAM)
    batch=16,              # reduce si tienes poca memoria
    name="yolov9-vehicles", # nombre del experimento
    workers=4,             # núm. de hilos
)