from roboflow import Roboflow
rf = Roboflow(api_key="1YfKPnmgH56zBY9QL8M5")
project = rf.workspace("car-test").project("car_bound_dection")
dataset = project.version(1).download("yolov8")
