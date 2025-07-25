from typing import Callable, List

def run_interceptors(validators: List[Callable], data: dict = {}):
    for validator in validators:
        validator(data)