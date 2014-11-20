import os
import sys
import json
import socket
import traceback
from datetime import datetime

import redis

from kuyruk import signals


CONFIG_KEYS = ["REDIS_HOST", "REDIS_PORT", "REDIS_DB", "REDIS_PASSWORD"]

REDIS_KEY = "failed_tasks"


class Requeue(object):

    def __init__(self, kuyruk):
        self.redis = redis.StrictRedis(
            host=kuyruk.config.REDIS_HOST,
            port=kuyruk.config.REDIS_PORT,
            db=kuyruk.config.REDIS_DB,
            password=kuyruk.config.REDIS_PASSWORD)
        signals.worker_failure.connect(self._handle_failure,
                                       sender=kuyruk, weak=False)

    def _handle_failure(self, sender, description, task, args, kwargs,
                        exc_info, worker):
        failure = {
            "description": description,
            "worker_queue": worker.queue,
            "worker_hostname": socket.gethostname(),
            "worker_pid": os.getpid(),
            "worker_cmd": ' '.join(sys.argv),
            "worker_timestamp": datetime.utcnow().isoformat()[:19],
            "exception_traceback": traceback.format_exception(*exc_info),
            "exception_type": "%s.%s" % (
                exc_info[0].__module__, exc_info[0].__name__),
        }

        self.redis.hset(REDIS_KEY, description['id'], json.dumps(failure))
