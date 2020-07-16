import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators import kubernetes_pod_operator

dag = DAG(dag_id="hello_airflow", start_date=airflow.utils.dates.days_ago(3), schedule_interval="@daily")


def do_magic(**context):
    print(context)


hello = BashOperator(task_id="hello", bash_command="echo 'hello'", dag=dag)
airflow = PythonOperator(task_id="airflow", python_callable=do_magic, provide_context=True, dag=dag)

k8s_task = kubernetes_pod_operator.KubernetesPodOperator(
	task_id="demo",
	name="minimal_example",
	cmds=["echo hello"],
	namespace="default",
	image="alpine:3.12.0",
)

hello >> airflow >> k8s_task
