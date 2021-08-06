from api.util import get_stage
from scheduler.sample_worker import WORKER_NAME_SAMPLE_WORKER, execute_worker

WORKER = 'worker'

WORK_HANDLERS = {
    WORKER_NAME_SAMPLE_WORKER: execute_worker
}


def _validate_event_details(event):
    if get_stage() is None:
        raise Exception("Stage is not defined in worker event " + event)
    return None


def process_event(event):
    _validate_event_details(event)

    worker_name = event[WORKER]
    work_handler = WORK_HANDLERS.get(worker_name)
    if work_handler is None:
        raise Exception('unknown worker: ' + worker_name)

    print("Executing worker handler:", worker_name, ":", event)
    return work_handler(event)
