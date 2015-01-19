# Kuyruk-Requeue

Save failed tasks to Redis and requeue them.

## Install

    $ pip install kuyruk-requeue

## Usage

```python
from kuyruk import Kuyruk, Config
from kuyruk_requeue import Requeue

config = Config()
config.REDIS_HOST = "localhost"
config.REDIS_PORT = 6379
config.REDIS_DB = 0
config.REDIS_PASSWORD = None

kuyruk = kuyruk.Kuyruk(config)

Requeue(kuyruk)

@kuyruk.task
def oops():
    1/0  # failed task will be saved to Redis
```

Run the command to requeue saved tasks:

    $ kuyruk --app ... requeue
