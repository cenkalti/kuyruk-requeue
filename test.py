import unittest
from collections import namedtuple

import mock

import kuyruk
import kuyruk_requeue

c = kuyruk.Config()
c.REDIS_HOST = "localhost"
c.REDIS_PORT = 6379
c.REDIS_DB = 0
c.REDIS_PASSWORD = None

k = kuyruk.Kuyruk(c)


@k.task
def error():
    1/0


Args = namedtuple("Args", ["queue", "local"])


class RequeueTestCase(unittest.TestCase):

    @mock.patch("kuyruk_requeue.redis")
    def test_save_exception(self, mock_redis):
        r = kuyruk_requeue.Requeue(k)

        queue = "kuyruk"
        args, kwargs = (), {}
        desc = error._get_description(args, kwargs, queue)

        message = mock.Mock()
        w = kuyruk.Worker(k, Args(queue, False))
        w._process_task(message, desc, error, args, kwargs)

        assert r.redis.hset.called
        assert message.channel.basic_reject.called
