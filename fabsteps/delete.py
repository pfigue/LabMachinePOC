# -*- coding: utf-8 -*-

"""
delete.py
Collection of functions related to deletion of branches.
"""


from labmachine.apps.branch.models import retrieve_branch
from labmachine.fabsteps.helpers import run_commands

def remove_directory(dev, branch):
    branch_object = retrieve_branch(dev=dev, branch=branch)
    return run_commands(['rm -rf %s' % branch_object.directory, ])


def remove_virtualenv(dev, branch):
    branch_object = retrieve_branch(dev=dev, branch=branch)
    return run_commands(['rm -rf %s' % branch_object.virtualenv_dir, ])


def remove_rabbit_vhost(dev, branch):
    branch_object = retrieve_branch(dev=dev, branch=branch)
    return run_commands([
            'sudo rabbitmqctl delete_vhost %s' % branch_object.broker_vhost,])


def remove_database(dev, branch):
    branch_object = retrieve_branch(dev=dev, branch=branch)
    return run_commands([
            'psql -U dowant_test -c "DROP DATABASE %s;"'  % branch_object.db_name,])


def remove_db_entry(dev, branch):
    branch_object = retrieve_branch(dev=dev, branch=branch)
    branch_object.delete()


# def delete_branch(dev, branch):
#     """
#     Runs all the steps to remove a branch
#     """
#     log = CmdLog(dev, branch, name='delete')
#     log.write('Beginning with delete for %s,%s' % (dev, branch))

#     change_branch_state(dev, branch, state.BEING_DELETED)
#     put_event(dev, branch, state.EV_DELETE_BEGIN)

#     branch_object = Branch.objects.get(dev=dev, branch=branch)
#     log.write('I\'m going with rm\'s and oher commands. Check the source')
#     sql_command = 'psql -U dowant_test -c "DROP DATABASE %s;"'
#     result = run_commands(
#         ['rm -rf %s' % branch_object.directory,
#          'rm -rf %s' % branch_object.virtualenv_dir,
#          'sudo rabbitmqctl delete_vhost %s' % branch_object.broker_vhost,
#          sql_command % branch_object.db_name, ],
#         ignore_errors=True)
#     log.write(result)

#     log.write('I\'m going with %s' % restart_services.__name__)
#     try:
#         step(restart_services, dev, branch, log)
#     except StepFailed:
#         change_branch_state(dev, branch, state.DELETE_FAILED)
#         put_event(dev, branch, state.EV_DELETE_END)
#     else:
#         put_event(dev, branch, state.EV_DELETE_END)
#         branch_object.delete()
#     finally:
#         log.close()


# def delete_branch_skipsteps(dev, branch, task_list):
#     """
#     Runs several steps (but not all) to remove a branch
#     """
#     log = CmdLog(dev, branch, name='delete')
#     log.write('Beginning with delete for %s,%s' % (dev, branch))

#     change_branch_state(dev, branch, state.BEING_DELETED)
#     put_event(dev, branch, state.EV_DELETE_BEGIN)

#     branch_object = Branch.objects.get(dev=dev, branch=branch)
#     log.write('I\'m going with rm\'s and oher commands. Check the source')
#     command_list = []
#     for task in task_list:
#         if str == type(task):
#             if 'remove_directory' == task:
#                 command_list.append('rm -rf %s' % branch_object.directory)
#             elif 'remove_virtualenv' == task:
#                 command_list.append('rm -rf %s' % branch_object.virtualenv_dir)
#             elif 'remove_rabbit_vhost' == task:
#                 shell_command = 'sudo rabbitmqctl delete_vhost %s'
#                 command_list.append(shell_command % branch_object.broker_vhost)
#             elif 'remove_database' == task:
#                 sql_command = 'psql -U dowant_test -c "DROP DATABASE %s;"'
#                 command_list.append(sql_command % branch_object.db_name)
#             else:
#                 pass
#     result = run_commands(command_list, ignore_errors=True)
#     log.write(result)

#     log.write('I\'m going with %s' % restart_services.__name__)
#     try:
#         step(restart_services, dev, branch, log)
#     except StepFailed:
#         change_branch_state(dev, branch, state.DELETE_FAILED)
#         put_event(dev, branch, state.EV_DELETE_END)
#     else:
#         put_event(dev, branch, state.EV_DELETE_END)
#         branch_object.delete()
#     finally:
#         log.close()
