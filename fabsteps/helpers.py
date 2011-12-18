# coding=utf-8

from fabric.api import run, cd
from fabric.api import settings as fabric_settings
from django.conf import settings as django_settings

# from os import fsync, walk
# from os import write as fd_write
# from os import close as fd_close
# from os.path import join
# from datetime import datetime
# from tempfile import mkstemp
# from time import strftime
# import re
# from fabric.colors import red, green
# from fabric.operations import put as fab_put
# from django.http import HttpResponse
# from django.shortcuts import render_to_response
# from cont_building import state
# from cont_building.models import Branch, State, UnitaryTestsState
# from cont_building.models import EventType, BranchEvent


class RunCommandsException(Exception):
    pass


def run_commands(list_of_commands, directory='',
                 ignore_errors=False, pty=False, shell=False):
    """
    Runs through fabric a list of shell commands given.

    Set ignore_errors to True, to don't stop when a command in the list
    fails.
    Set directory to the directory where you want to run the scripts
    """
    output = ''
    with fabric_settings(host_string=django_settings.FABRIC_HOST, warn_only=True):
        with cd(directory):
            for command in list_of_commands:
                result = run(command, pty=pty, shell=shell)
                output += str(result)
                if result.failed is True and ignore_errors is False:
                    raise RunCommandsException(output)
    return output


def supervisor_tasks_list(branch_object):
    """
    Returns a string with the names of the supevisor tasks which live
    in the same group
    """
    first = True
    for (ignore1, ignore2, suffix) in django_settings.SUPERVISOR_TEMPLATE_LIST:
        if suffix is not None:
            if first:
                list_of_supervisor_tasks = ''
                first = False
            else:
                list_of_supervisor_tasks += ', '
            fields = (branch_object.cleared_project_name, suffix)
            list_of_supervisor_tasks += '%s-%s' % fields
    return list_of_supervisor_tasks


def env_to_str_comma(branch_object):
    """
    Returns a string with comma-separated environment variables.
    NOTE: branch_object is used by eval()
    """
    output = ''
    # FIXME use a list comprenhension here
    for key in django_settings.ENVIRONMENT_VARS.keys():
        fields = (key, eval(django_settings.ENVIRONMENT_VARS[key]))
        output += '%s=\'%s\',' % fields
    j = len(output) - 1
    output = output[:j]
    return output


def fill_in_the_templates(branch_object):
    """
    Return the context to fulfill a template
    """
    task_list = supervisor_tasks_list(branch_object)
    return {
        'project_name': branch_object.cleared_project_name,
        'db_name': branch_object.db_name,
        'project_uri': branch_object.uri,
        'project_mobile_uri': 'm.%s' % branch_object.uri,
        'project_path': branch_object.directory,
        'code_dir': branch_object.code_dir,
        'virtualenv': branch_object.virtualenv_dir,
        'log_dir': branch_object.log_dir,
        'broker_vhost': branch_object.broker_vhost,
        'list_of_supervisor_tasks': task_list,
        'uwsgi_port': branch_object.uwsgi_port,
        'environment': env_to_str_comma(branch_object),
    }
