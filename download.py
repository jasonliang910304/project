from roboflow import Roboflow
rf = Roboflow(api_key="tI0FEIFYZE4jlpI7wRXV")
project = rf.workspace("fyp-object-detection-tc8af").project("sya-car")
dataset = project.version(1).download("yolov8")
