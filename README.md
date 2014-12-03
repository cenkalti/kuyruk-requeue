# Kuyruk-Requeue

Save failed tasks to Redis and requeue them.

## Install

    $ pip install kuyruk-requeue

## Usage

```python
from kuyruk import Kuyruk, Config
from kuyruk_requeue import Requeue

config = Config()
config.KUYRUK_REDIS_HOST = "localhost"
config.KUYRUK_REDIS_PORT = 6379
config.KUYRUK_REDIS_DB = 0
config.KUYRUK_REDIS_PASSWORD = None

kuyruk = kuyruk.Kuyruk(config)

s = Requeue(k)

@kuyruk.task
def oops():
    1/0  # failed task will be saved to Redis
```

Run the command to requeue saved tasks:

    $ kuyruk --app ... requeue
