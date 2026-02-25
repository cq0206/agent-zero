import time


class RetryConfig:
    def __init__(self, max_retries=3, delay=1):
        self.max_retries = max_retries
        self.delay = delay


def retry_llm_call(func, config: RetryConfig):
    last_error = None

    for _ in range(config.max_retries):
        try:
            return func()
        except Exception as e:
            last_error = e
            time.sleep(config.delay)

    raise last_error


def retry_json_parse(parse_func, text, config: RetryConfig):
    last_error = None

    for _ in range(config.max_retries):
        try:
            return parse_func(text)
        except Exception as e:
            last_error = e
            time.sleep(config.delay)

    raise last_error
