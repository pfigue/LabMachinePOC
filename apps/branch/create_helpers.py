# coding=utf-8

from collections import deque
from os.path import join
from django.http import HttpResponse
from django.conf import settings
from django.db.transaction import commit_on_success
from django.utils.datastructures import MultiValueDictKeyError
from labmachine.apps.branch.models import Branch
from labmachine.apps.branch.models import sanitize_branch_name
from labmachine.apps.branch.models import retrieve_branch
from labmachine.apps.branch.constants import STEPS_ORDER

# from labmachine.apps.branch.create_helpers import BranchManipulatorFactory
# from labmachine.apps.branch.create_helpers import ManipulatorProblem
# from labmachine.apps.branch.create_helpers import InvalidInput
# from labmachine.apps.branch.create_helpers import request2dict


from labmachine.fabsteps import install_dir_struct_pre_repo
from labmachine.fabsteps import install_repo
from labmachine.fabsteps import install_branch
from labmachine.fabsteps import install_dir_struct_post_repo
from labmachine.fabsteps import install_virtualenv
from labmachine.fabsteps import install_pip_requirements
from labmachine.fabsteps import install_config_files
from labmachine.fabsteps import install_rabbit_vhost
from labmachine.fabsteps import install_database
from labmachine.fabsteps import install_django_stuff
from labmachine.fabsteps import restart_services

from labmachine.fabsteps import remove_directory
from labmachine.fabsteps import remove_virtualenv
from labmachine.fabsteps import remove_rabbit_vhost
from labmachine.fabsteps import remove_database
from labmachine.fabsteps import remove_db_entry

from labmachine.fabsteps import update_repo
from labmachine.fabsteps import remove_pyc_files

from labmachine.fabsteps.executor import executor_for_celery
from labmachine.fabsteps.executor import executor_for_fabric


def action_submit(request, action):
    try:
        data = request2dict(request) # FIXME return a deque of steps and a branch obj.
    except InvalidInput:
        return HttpResponse("invalid data for branch")
    try:
        manipulator = Launcher()
        branch = manipulator.run(data, action=action, celery=True) # FIXME go with branch info., deque tasks, extra info. (like the action)
    except ManipulatorProblem:
        return HttpResponse("error while %s branch" % action)
        
    return HttpResponse("%s branch %s, %s" % (action, branch.dev, branch.branch))


class InvalidInput(Exception):
    pass

    
class ManipulatorProblem(Exception):
    pass


def order_steps(green, red):
    return STEPS_ORDER.index(green.__name__) - STEPS_ORDER.index(red.__name__)
   

def request2dict(request):
    """
    Check for valid parameters for branch creation
    """
    data = {}
    try:
        data['dev']  = request.POST['dev'].strip()
        data['branch'] = request.POST['branch'].strip()
        if '/' == data['branch'][0]:
            raise Exception('/ as first char.')
    except MultiValueDictKeyError:
        data['id_branch'] = request.POST['id_branch'].strip()

    steps_list = []
    for key in request.POST.keys():
        if 'on' == request.POST[key]:
            steps_list.append(eval(key)) # FIXME move this to fabstep.__init__
    data['steps'] = deque(sorted(steps_list, cmp=order_steps))
    # raise Exception('test ended')
    # FIXME look for strange things
    return data


def install_db_entry(dev, branch):
    filesystem_id = '%s_%s' % (dev,
                               sanitize_branch_name(branch))
    parameters = dict()
    parameters['id_branch'] = filesystem_id
    parameters['dev'] = dev
    parameters['branch'] = branch
    parameters['uwsgi_port'] = get_a_free_uwsgi_port()
    parameters['directory'] = join(settings.BRANCH_STORE, filesystem_id)
    parameters['virtualenv_dir'] = join(settings.VIRTUALENV_STORE,
                                        filesystem_id)
    parameters['log_dir'] = join(settings.LOG_STORE, filesystem_id)
    branch = Branch.objects.create(**parameters)
    print('(create_branch) id_branch = %s' % str(branch.id_branch))
    return branch


def get_a_free_uwsgi_port():
    """
    Returns the next lowest free uwsgi port which is not in use
    No port will be lowe than FIRST_UWSGI_PORT
    """
    branch_list = Branch.objects.all()
    list_of_ports = [a_branch.uwsgi_port for a_branch in branch_list]
    the_port = settings.FIRST_UWSGI_PORT
    while the_port in list_of_ports:
        the_port += 1
    return the_port


def notify(branch, msg):
    print "{NOTIFY} branch: %s, msg: %s" % (branch.id_branch, msg)


class Launcher(object):
    def run(self, data, action, celery):
        # Insert the new branch into DB, if we have to.
        if install_db_entry in data['steps']:
            branch = install_db_entry(dev=data['dev'], branch=data['branch'])
            data['steps'].remove(install_db_entry)
        else:
            branch = retrieve_branch(dev=data['dev'], branch=data['branch'])

        notify(branch, 'queued %s' % action)
        self.launch_steps(branch, data, celery=celery)
        return branch

    
    def launch_steps(self, branch, data, celery):
        step_deque = data['steps']
	if celery:
            # print('id_branch = %s' % str(branch.id_branch))
            executor_for_celery.delay(branch.dev, branch.branch, step_deque)
	else:
            executor_for_fabric(branch.dev, branch.branch, step_deque)
        return

