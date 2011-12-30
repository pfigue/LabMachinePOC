# coding=utf-8

"""
celery_tasks.py
Celery wrapper for the fabric tasks
"""


from Crypto import Random
from celery.decorators import task as cTask
from labmachine.fabsteps.helpers import update_activity_log
from labmachine.fabsteps.helpers import RunCommandsException


@cTask(name='executor_for_celery')
def executor_for_celery(dev, branch, step_deque):
    if 0 == len(step_deque):
        return
    Random.atfork()

    step = step_deque.popleft()
    try:
        output = step(dev, branch)
    except RunCommandsException as fail:
        output = str(fail)
    # FIXME should we stop the execution of the next steps? empty the step_deque
    update_activity_log(dev, branch, step, output)

    if 0 != len(step_deque):
        executor_for_celery.delay(dev, branch, step_deque)


def executor_for_fabric(dev, branch, step_deque):
    if 0 == len(step_deque):
        return
    step = step_deque.popleft()
    step(dev, branch)
    executor_for_fabric(dev, branch, step_deque)

