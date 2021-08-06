WORKER_NAME_SAMPLE_WORKER = "sample_worker"


def execute_worker(event):
    name = event['name']
    return "Hello world," + name
