import prefect
from prefect import task, Flow
from prefect.run_configs import KubernetesRun
from prefect.storage import GitHub

@task
def say_hello():
    logger = prefect.context.get("logger")
    logger.info("Hello, Cloud!")

with Flow("hello-flow") as flow:
    say_hello()

#flow.run_config = KubernetesRun(image="prefecthq/prefect:0.14.15")
flow.run_config = KubernetesRun()
flow.executor = DaskExecutor("tcp://dask-scheduler:8786")
flow.storage = GitHub(
    repo="swyngaard/prefect-flows",              # name of repo
    path="hello.py",                             # location of flow file in repo
    #access_token_secret="GITHUB_ACCESS_TOKEN"   # name of personal access token secret
)

# Register the flow under the "tutorial" project
flow.register(project_name="tutorial")
