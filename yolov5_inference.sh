git clone https://github.com/ultralytics/yolov5.git
cd yolov5
curl -L https://github.com/ultralytics/yolov5/releases/download/v6.0/v61_yolov5s.pt --output v61_yolov5s.pt
pip install -r requirements.txt
python3 detect.py --weights v61_yolov5s.pt --source $1 --project /tmp/images --name result
