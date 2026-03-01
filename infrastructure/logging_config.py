import logging
import os
import json
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "agent.log")

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "task_id"):
            log_record["task_id"] = record.task_id
        if hasattr(record, "stage"):
            log_record["stage"] = record.stage
        if hasattr(record, "input_tokens"):
            log_record["input_tokens"] = record.input_tokens
        if hasattr(record, "output_tokens"):
            log_record["output_tokens"] = record.output_tokens
        if hasattr(record, "total_tokens"):
            log_record["total_tokens"] = record.total_tokens

        return json.dumps(log_record)


def setup_logging():
    
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(JsonFormatter())

    logger.addHandler(file_handler)

    return logger