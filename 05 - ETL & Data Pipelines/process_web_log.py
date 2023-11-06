from airflow import DAG
from airflow.operators.bash_operator import BashOperator
import datetime as dt



default_args = {
  'owner': 'me',
  'start_date': dt.datetime(2023,10,26),
  'email': ['brandon@ibmcapstone.org'],
}


dag=DAG(
  'process_web_log',
  description='ETL pipeline for SoftCart access log',
  default_args=default_args,
  schedule_interval=dt.timedelta(days=1),
)


extract_data = BashOperator(
  task_id='extract_data',
  bash_command='cut -f1 -d" " $AIRFLOW_HOME/dags/capstone/accesslog.txt > $AIRFLOW_HOME/dags/capstone/extracted_data.txt',
  dag=dag,
)



transform_data = BashOperator(
  task_id='transform_data',
  bash_command='grep -vw "198.46.149.143" $AIRFLOW_HOME/dags/capstone/extracted_data.txt > $AIRFLOW_HOME/dags/capstone/transformed_data.txt',
  dag=dag,
)




load_data = BashOperator(
  task_id='load_data',
  bash_command='tar -zcvf $AIRFLOW_HOME/dags/capstone/weblog.tar $AIRFLOW_HOME/dags/capstone/transformed_data.txt',
  dag=dag,
)



extract_data >> transform_data >> load_data






