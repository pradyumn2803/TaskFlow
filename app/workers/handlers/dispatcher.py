from app.workers.handlers.job_handlers import generate_report

HANDLERS={
    "GENERATE_REPORT":generate_report
}

def execute_job(job_type:str,payload:dict)->None:

    handler = HANDLERS.get(job_type)

    if handler is None:
        raise ValueError(f"unsupported job type:{job_type}")

    handler(payload=payload)