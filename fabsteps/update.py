# -*- coding: utf-8 -*-

"""
update.py
Collection of functions related to the update of installed branches
"""

from labmachine.apps.branch.models import retrieve_branch
from labmachine.fabsteps.helpers import run_commands

# from cont_building import state
# from cont_building.models import Branch
# from cont_building.homeworks.install import install_config_files
# from cont_building.homeworks.install import install_pip_requirements
# from cont_building.homeworks.install import install_django_stuff
# from cont_building.homeworks.auxiliar import do_step, run_commands
# from cont_building.homeworks.auxiliar import restart_services
# from cont_building.homeworks.auxiliar import CmdLog, put_event
# from cont_building.homeworks.auxiliar import change_branch_state
# from cont_building.homeworks.auxiliar import change_branch_test_state




# def update_branch_skipsteps(dev, branch, task_list):
#     """
#     Run several (but not all) steps to update a branch
#     """
#     log = CmdLog(dev, branch, name='update_skipsteps')
#     log.write('Beginning with update_skipsteps for %s,%s' % (dev, branch))

#     change_branch_test_state(dev, branch, state.NOT_TESTED_YET)
#     change_branch_state(dev, branch, state.BEING_UPDATED)
#     put_event(dev, branch, state.EV_UPDATE_BEGIN)

#     for task in task_list:
#         log.write('Beginning step: %s' % task.__name__)
#         try:
#             step(task, dev, branch, log)
#         except:
#             change_branch_state(dev, branch, state.UPDATE_FAILED)
#             put_event(dev, branch, state.EV_UPDATE_END)
#             log.close()
#             raise

#     log.write('Done with update_skipsteps for %s,%s' % (dev, branch))
#     # NOTE reread the object. Functions like install_config_files
#     # modify the entry in the DB
#     # NOTE if we don't read it again, changes will be discharged
#     change_branch_state(dev, branch, state.READY)
#     put_event(dev, branch, state.EV_UPDATE_END)
#     log.close()
#     return True


def update_repo(dev, branch):
    """
    Update the branch's repository
    """
    branch_object = retrieve_branch(dev=dev, branch=branch)
    return run_commands(['git fetch origin',
                          'git pull origin %s' % branch_object.branch, ],
                          directory=branch_object.code_dir)


def remove_pyc_files(dev, branch):
    """
    Clean *.pyc
    """
    branch_object = retrieve_branch(dev=dev, branch=branch)
    return run_commands(['find . -name "*.pyc" -exec rm -f {} \;', ],
                          directory=branch_object.code_dir)
