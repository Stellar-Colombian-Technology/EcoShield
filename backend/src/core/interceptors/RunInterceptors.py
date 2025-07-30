from typing import Callable, List

async def run_interceptors(validators: List[Callable], data: dict = {}):
    for validator in validators:
        await validator(data)