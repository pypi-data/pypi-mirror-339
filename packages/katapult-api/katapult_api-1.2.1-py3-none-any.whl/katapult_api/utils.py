import asyncio
from collections.abc import Sequence
from typing import Callable, Optional


async def task_handler(
    func: Callable,
    param_list: Optional[Sequence[dict[str, str] | tuple[str, str]]] = None,
):
    tasks = []

    if not param_list:
        tasks.append(asyncio.create_task(func()))
    else:
        for i, params in enumerate(param_list):
            tasks.append(asyncio.create_task(func(**params), name=f"task-{i}"))

    return await asyncio.gather(*tasks)
