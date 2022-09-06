# Publisher

[Complex_watcher Index](../README.md#complex_watcher-index) /
[Complex Watcher](./index.md#complex-watcher) /
Publisher

> Auto-generated documentation for [complex_watcher.publisher](../../complex_watcher/publisher.py) module.

- [Publisher](#publisher)
  - [PubMsg](#pubmsg)

## PubMsg

[Show source in publisher.py:30](../../complex_watcher/publisher.py#L30)

Publish a message to a queue with exchange and routing key

#### Signature

```python
class PubMsg:
    def __init__(
        self, queue, rabhost, user, passwd, msg, routing_key="complex_fxp", vhost="/"
    ):
        ...
```


