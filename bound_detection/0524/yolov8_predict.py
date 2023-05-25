from ultralytics import YOLO

model = YOLO("bound_model.pt")


results = model.predict(source="bound_photo", save=True)
