from datetime import datetime
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# DAG 정의
dag = DAG(
        dag_id="yolov5_inference", # webserver에 표시될 dag 이름
        description="Download person picture and inference it using yolov5",
        start_date=datetime(2021, 1, 1), #해당 pipeline 실행 시작 시간
        tags=["yolov5"],
        schedule_interval=None, #해당 pipeline 실행 주기,
        catchup=False # 이전에 실행되지 않았던 dag를 backfill할지 말지 결정
        )

IMAGE_DIR = '/tmp/images' # image 저장 장소 지정 (원하는 곳으로 지정)
def _make_img_store():
    Path(IMAGE_DIR).mkdir(exist_ok=True, parents=True)  # image가 저장될 장소 만듬

# task 정의
make_image_store = PythonOperator(
        task_id="make_image_store",
        python_callable=_make_img_store,
        dag=dag
    )

# task 정의
download_person_picture = BashOperator(
    task_id="download_person_picture",
    bash_command=f"curl -L https://source.unsplash.com/random\?person --output {Path(IMAGE_DIR)/'image.png'}",  # download person pic
    dag=dag,
)

# task 정의
inference_using_yolov5 = BashOperator(
    task_id="inference_using_yolov5",
    bash_command=f"sudo sh ~/airflow/dags/yolov5_inference.sh {Path(IMAGE_DIR)/'image.png'}",  # inference person image using yolov5
    dag=dag,
)

make_image_store >> download_person_picture >> inference_using_yolov5

