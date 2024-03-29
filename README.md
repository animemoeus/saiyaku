# Saiyaku: Auto-Retry Decorator for Python

Saiyaku, inspired by the Japanese term meaning "disaster" or "calamity," is a Python decorator that allows you to automatically retry a function when a specified exception occurs. It can be useful in scenarios where you want to handle transient errors gracefully by retrying the operation.

---

## Installation

```bash
pip install saiyaku
```

## API

### retry decorator

```python
    def retry(exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1, jitter=0, logger=logging_logger):
        """Return a retry decorator.

        :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
        :param tries: the maximum number of attempts. default: -1 (infinite).
        :param delay: initial delay between attempts. default: 0.
        :param max_delay: the maximum value of delay. default: None (no limit).
        :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
        :param jitter: extra seconds added to delay between attempts. default: 0.
                       fixed if a number, random if a range tuple (min, max)
        :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                       default: retry.logging_logger. if None, logging is disabled.
        """
```

Various retrying logic can be achieved by combination of arguments.

#### Examples

```python
    from saiyaku import retry
```

```python
    @retry()
    def make_trouble():
        '''Retry until succeed'''
```

```python
    @retry(ZeroDivisionError, tries=3, delay=2)
    def make_trouble():
        '''Retry on ZeroDivisionError, raise error after 3 attempts, sleep 2 seconds between attempts.'''
```

```python
    @retry((ValueError, TypeError), delay=1, backoff=2)
    def make_trouble():
        '''Retry on ValueError or TypeError, sleep 1, 2, 4, 8, ... seconds between attempts.'''
```

```python
    @retry((ValueError, TypeError), delay=1, backoff=2, max_delay=4)
    def make_trouble():
        '''Retry on ValueError or TypeError, sleep 1, 2, 4, 4, ... seconds between attempts.'''
```

```python
    @retry(ValueError, delay=1, jitter=1)
    def make_trouble():
        '''Retry on ValueError, sleep 1, 2, 3, 4, ... seconds between attempts.'''
```

```python
    # If you enable logging, you can get warnings like 'ValueError, retrying in
    # 1 seconds'
    if __name__ == '__main__':
        import logging
        logging.basicConfig()
        make_trouble()
```

### retry_call

```python
    def retry_call(f, fargs=None, fkwargs=None, exceptions=Exception, tries=-1, delay=0, max_delay=None, backoff=1,
                   jitter=0,
                   logger=logging_logger):
        """
        Calls a function and re-executes it if it failed.

        :param f: the function to execute.
        :param fargs: the positional arguments of the function to execute.
        :param fkwargs: the named arguments of the function to execute.
        :param exceptions: an exception or a tuple of exceptions to catch. default: Exception.
        :param tries: the maximum number of attempts. default: -1 (infinite).
        :param delay: initial delay between attempts. default: 0.
        :param max_delay: the maximum value of delay. default: None (no limit).
        :param backoff: multiplier applied to delay between attempts. default: 1 (no backoff).
        :param jitter: extra seconds added to delay between attempts. default: 0.
                       fixed if a number, random if a range tuple (min, max)
        :param logger: logger.warning(fmt, error, delay) will be called on failed attempts.
                       default: retry.logging_logger. if None, logging is disabled.
        :returns: the result of the f function.
        """
```

This is very similar to the decorator, except that it takes a function and its arguments as parameters. The use case behind it is to be able to dynamically adjust the retry arguments.

```python
    import requests

    from saiyaku import retry_call


    def make_trouble(service, info=None):
        if not info:
            info = ''
        r = requests.get(service + info)
        return r.text


    def what_is_my_ip(approach=None):
        if approach == "optimistic":
            tries = 1
        elif approach == "conservative":
            tries = 3
        else:
            # skeptical
            tries = -1
        result = retry_call(make_trouble, fargs=["http://ipinfo.io/"], fkwargs={"info": "ip"}, tries=tries)
        print(result)

    what_is_my_ip("conservative")
```

---

- This package is created based on [invl/retry](https://github.com/invl/retry) 🔥🚀
