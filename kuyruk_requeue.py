import os
import sys
import json
import socket
import traceback
from datetime import datetime

import amqp
import redis

from kuyruk import signals


CONFIG = {
    "REDIS_HOST": "localhost",
    "REDIS_PORT": 6379,
    "REDIS_DB": 0,
    "REDIS_PASSWORD": None,
}

REDIS_KEY = "failed_tasks"


class Requeue(object):

    def __init__(self, kuyruk):
        self.kuyruk = kuyruk
        self.kuyruk.extensions["requeue"] = self
        self.redis = redis.StrictRedis(
            host=kuyruk.config.REDIS_HOST,
            port=kuyruk.config.REDIS_PORT,
            db=kuyruk.config.REDIS_DB,
            password=kuyruk.config.REDIS_PASSWORD)

        if "sentry" in kuyruk.extensions:
            sig = kuyruk.extensions["sentry"].on_exception
        else:
            sig = signals.worker_failure

        sig.connect(self._handle_failure, sender=kuyruk, weak=False)

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

    def requeue_failed_tasks(self):
        tasks = self.redis.hvals(REDIS_KEY)
        with self.kuyruk.channel() as channel:
            for task in tasks:
                task = json.loads(task)
                print "Requeueing task: %r" % task
                self.requeue_task(task, channel=channel)
        print "%i failed tasks have been requeued." % len(tasks)

    def requeue_task(self, failed, channel=None):
        if channel:
            _requeue_failed_task(failed, channel, self.redis)
        else:
            with self.kuyruk.channel() as channel:
                _requeue_failed_task(failed, channel, self.redis)


def _requeue_failed_task(failed, channel, redis):
        description = failed['description']
        queue_name = failed['worker_queue']
        count = description.get('requeue_count', 0)
        description['requeue_count'] = count + 1
        body = json.dumps(description)
        msg = amqp.Message(body=body)
        channel.queue_declare(queue_name, durable=True, auto_delete=False)
        channel.basic_publish(msg, exchange="", routing_key=queue_name)
        redis.hdel(REDIS_KEY, description['id'])


def requeue(kuyruk, args):
    r = Requeue(kuyruk)
    r.requeue_failed_tasks()

help_text = "requeue failed tasks"

command = (requeue, help_text, None)
