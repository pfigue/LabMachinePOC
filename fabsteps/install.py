# coding=utf-8

"""
install.py
Collection of functions related to the install of new branches.

Some functions are used also in branch update
"""


from os.path import join
from django.conf import settings as django_settings
from fabric.api import settings as fabric_settings
from fabric.contrib.files import upload_template
from labmachine.apps.branch.models import Branch
from labmachine.fabsteps.helpers import run_commands
from labmachine.fabsteps.helpers import fill_in_the_templates
from labmachine.fabsteps.helpers import RunCommandsException

# from cont_building import state
# from cont_building.homeworks.auxiliar import do_step, env_to_str, run_commands
# from cont_building.homeworks.auxiliar import restart_services
# from cont_building.homeworks.auxiliar import fill_in_the_templates
# from cont_building.homeworks.auxiliar import CmdLog, RunCommandsException
# from cont_building.homeworks.auxiliar import change_branch_state, put_event
# from cont_building.homeworks.auxiliar import use_prefab_database


# def init_branch(dev, branch):
#     """
#     Run all the steps to install a new branch
#     """
#     log = CmdLog(dev, branch, name='install')
#     log.write('Beginning with install for %s,%s' % (dev, branch))

#     change_branch_state(dev, branch, state.BEING_INSTALLED)
#     put_event(dev, branch, state.EV_INSTALL_BEGIN)

#     for task in (install_dir_structure_pre_repo,
#                  install_repo,
#                  install_branch,
#                  install_dir_structure_post_repo,
#                  install_virtualenv,
#                  install_config_files,
#                  install_rabbit_vhost,
#                  install_pip_requirements,
#                  install_database,
#                  install_django_stuff,
#                  restart_services, ):
#         log.write('I\'m going with %s' % task.__name__)
#         try:
#             step(task, dev, branch, log)
#         except RunCommandsException:
#             change_branch_state(dev, branch, state.INSTALL_FAILED)
#             put_event(dev, branch, state.EV_INSTALL_END)
#             log.close()
#             raise

#     log.write('Done with install for %s,%s' % (dev, branch))
#     # NOTE reread the object. Functions like install_config_files
#     # modify the entry in the DB
#     # NOTE if we don't read it again, changes will be discharged
#     change_branch_state(dev, branch, state.READY)
#     put_event(dev, branch, state.EV_INSTALL_END)
#     log.close()
#     return True


# def init_branch_skipsteps(dev, branch, task_list):
#     """
#     Install a new branch. This gives the possibility of skip several steps
#     """
#     log = CmdLog(dev, branch, name='install')
#     log.write('Beginning with install for %s,%s' % (dev, branch))

#     change_branch_state(dev, branch, state.BEING_INSTALLED)
#     put_event(dev, branch, state.EV_INSTALL_BEGIN)

#     for task in task_list:
#         log.write('I\'m going with %s' % task.__name__)
#         try:
#             step(task, dev, branch, log)
#         except RunCommandsException:
#             change_branch_state(dev, branch, state.INSTALL_FAILED)
#             put_event(dev, branch, state.EV_INSTALL_END)
#             log.close()
#             raise

#     log.write('Done with install for %s,%s' % (dev, branch))
#     # NOTE reread the object. Functions like install_config_files
#     # modify the entry in the DB
#     # NOTE if we don't read it again, changes will be discharged
#     change_branch_state(dev, branch, state.READY)
#     put_event(dev, branch, state.EV_INSTALL_END)
#     log.close()
#     return True


def install_virtualenv(dev, branch):
    """
    Prepare an empty virtualenv
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)
    # NOTE Var. in postactivate script
    activate_path = join(branch_object.virtualenv_dir, 'bin/postactivate')
    command_list = [
        'virtualenv --no-site-packages %s' % branch_object.virtualenv_dir, ]
    for key in django_settings.ENVIRONMENT_VARS.keys():
        fields = (key,
                  eval(django_settings.ENVIRONMENT_VARS[key]),
                  activate_path)
        command_list.append('echo \'export %s=%s\' >> %s' % fields)
    return run_commands(command_list)


def install_dir_struct_pre_repo(dev, branch):
    """
    Create _branch_/ _branch_/log/ and _branch_/data/ directory
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)

    command_list = ['mkdir -p %s' % branch_object.directory,
                    'mkdir -p %s' % branch_object.log_dir, ]

    data_dirs = ('data/', 'data/billing/', 'data/bloomsburys/',
                 'data/bloomsburys/imports/',
                 'data/bloomsburys/imports/products.2011-02-07_small/',
                 'data/bloomsburys/imports/products.B-MY.20110207-164827.xml/',
                 'data/faxes/', 'data/faxes/retarus/',
                 'data/compressed/', 'data/orders/', )
    for one_dir in data_dirs:
        command_list.append('mkdir %s' %
                            join(branch_object.directory, one_dir), )

    return run_commands(command_list)


def install_dir_struct_post_repo(dev, branch):
    """
    Create _/data/ directory.
    Replace symlinks to global dirs. with different direcories for each branch
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)
    fields = (branch_object.log_dir,
              join(branch_object.directory, 'log'))
    command_list = ['rm -rf code/dowant/media/compressed',
                    'mkdir code/dowant/media/compressed',
                    'rm -rf code/dowant/media/restaurant_logos',
                    'mkdir code/dowant/media/restaurant_logos',
                    'rm -rf code/dowant/media/uploads',
                    'mkdir code/dowant/media/uploads',
                    'rm -rf code/dowant/media/img/company_logos',
                    'mkdir code/dowant/media/img/company_logos',
                    'ln -s %s %s' % fields, ]
    return run_commands(command_list, directory=branch_object.directory)


def install_repo(dev, branch):
    """
    Create the directory and clone the repo. if it doesn't exist
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)
    command_list = ['mkdir -p %s' % branch_object.directory,
                    'git clone %s %s' % (branch_object.git_repo,
                                         branch_object.code_dir), ]
    # NOTE: git clone mkdir and rmdir by itself
    return run_commands(command_list)


def install_branch(dev, branch):
    """
    If we want a branch different of master, download it.
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)
    if 'master' == branch:
        return '{nothing_to_do, "branch == master"}'
    command_list = ['git fetch origin',
                    'git checkout -b %s origin/%s' % (branch, branch), ]
    return run_commands(command_list, directory=branch_object.code_dir)


def install_config_files(dev, branch):
    """
    Fulfill the templates for config files and push them to the server
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)

    # Prepare data for templates
    context = fill_in_the_templates(branch_object)

    # Create dirs and install templates
    supervisor_path = join(branch_object.config_dir, 'supervisor/')
    nginx_path = join(branch_object.config_dir, 'nginx/')
    command_list = ['mkdir -p %s' % branch_object.config_dir,
                    'mkdir -p %s' % supervisor_path,
                    'mkdir -p %s' % nginx_path, ]
    output = run_commands(command_list)
    with fabric_settings(host_string=django_settings.FABRIC_HOST, warn_only=True):
        template_list = django_settings.SUPERVISOR_TEMPLATE_LIST
        for (template_path, target, ignore) in template_list:
            source = join(django_settings.SUPERVISOR_TEMPLATE_PATH, template_path)
            dest = join(branch_object.directory, target)
            upload_template(source, dest, context=context, backup=False)
    return output


def install_rabbit_vhost(dev, branch):
    """
    Create a RabbitMQ vhost and set permissions for the lab user
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)
    rabbit_vhost = 'sudo rabbitmqctl add_vhost %s'
    rabbit_perm = "sudo rabbitmqctl set_permissions -p %s lab '.*' '.*' '.*'"
    # NOTE: remember to allow www-data to run rabbitmqctl in sudoers file
    return run_commands(
        [rabbit_vhost % branch_object.broker_vhost,
         rabbit_perm % branch_object.broker_vhost, ])


def install_pip_requirements(dev, branch):
    """
    Install all the packages cited in requirements.pip in the virtual
    environment
    NOTE: Sometimes this step crashes because pip can not download the pkgs
    NOTE: Sometimes the name of the pkg changes
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)
    requirements_file = join(branch_object.code_dir, 'dowant/requirements.pip')
    return run_commands(
        ['pip install -E %s -r %s' % (branch_object.virtualenv_dir,
                                      requirements_file), ])


def install_database(dev, branch):
    """
    Copy dowant_test database for this installation
    NOTE: this takes like 10min.
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)
    # if bool(branch_object.lettuce_mode):
    #     return ''
    # else:
    use_prefab_database(branch_object.db_name)


def look_for_prefab_database(db_name):
    prefab_db_name = None
    output = ''
    # Look for a existing prefab DB
    for no_copy in range(1, 5):
        test_name = 'dowant_prefab_%s' % str(no_copy)
        # NOTE: api_apikey is faster than django_session
        sql_command = 'SELECT * FROM api_apikey LIMIT 1;'
        # NOTE: '-o -' is necessary to avoid the pager that
        # psql launches and stucks the process
        # Another option would be 'psql -l'
        command = '/usr/bin/psql -U dowant_test -t -d %s -c \"%s\" -o -'
        try:
            output += run_commands(
                [command % (test_name, sql_command), ], pty=True, shell=False)
            prefab_db_name = test_name
            break
        except RunCommandsException:
            continue
    return (prefab_db_name, output)


def use_prefab_database(db_name):
    """
    Assigns a databse for the branch.
    If there is a prefab. one, it uses it, if not,
    it creates a new one, taking dowant_test as template
    """
    (prefab_db_name, output) = look_for_prefab_database(db_name)

    if prefab_db_name is None:
        # no prefab available, create one (sloooow)
        sql_command = 'CREATE DATABASE %s WITH TEMPLATE dowant_test;'
        sql = sql_command % db_name
    else:
        # prefab available, change name (fast!)
        sql_command = 'ALTER DATABASE %s RENAME TO %s;'
        sql = sql_command % (prefab_db_name, db_name)
    output += run_commands(['psql -U dowant_test -c \"%s\"' % sql, ])

    return output


def install_django_stuff(dev, branch):
    """
    3 steps: install db schema mods., compress the JS (FIX: sure?) and
    compile the *.po i18n files

    NOTE: DB migrations are interactive with the user. If there is,
    the step crashes
    """
    branch_object = Branch.objects.get(dev=dev, branch=branch)
    dowant_dir = join(branch_object.code_dir, 'dowant/')
    environment = env_to_str(branch_object)
    migrate = '%s python manage.py migrate --delete-ghost-migrations'
    # FIXME list comprenhension
    commands_list = [
        migrate % environment,
        '%s python manage.py lh_synccompress' % environment,
        '%s python manage.py compilemessages' % environment, ]
    # '%s python manage.py test -s'%environment, ]
    return run_commands(commands_list,
                        directory=dowant_dir)


def env_to_str(branch_object):
    """
    Returns a string with space-separated environment variables.
    NOTE: branch_object is used by eval()
    """
    # FIXME use a comprenhension
    output = ''
    for key in django_settings.ENVIRONMENT_VARS.keys():
        fields = (key, eval(django_settings.ENVIRONMENT_VARS[key]))
        output += '%s=\'%s\' ' % fields
    return output


def restart_services(dev, branch):
    """
    Reload nginx and the supervisor
    """
    command_list = ['sudo supervisorctl reload',
                    'sudo /etc/init.d/nginx reload', ]
    # NOTE: don't forget to allow www-data run this in sudoers file
    return run_commands(command_list)

# def install_django_stuff(dev, branch):
#     """
#     3 steps: install db schema mods., compress the JS (FIX: sure?) and
#     compile the *.po i18n files

#     NOTE: DB migrations are interactive with the user. If there is,
#     the step crashes
#     """
#     branch_object = Branch.objects.get(dev=dev, branch=branch)
#     dowant_dir = join(branch_object.code_dir, 'dowant/')
#     environment = env_to_str(branch_object)
#     if bool(branch_object.lettuce_mode) is True:
#         # NOTE: avoid db stuff for lettuces
#         commands_list = ['%s python manage.py lh_synccompress' % environment,
#                          '%s python manage.py compilemessages' % environment, ]
#     # '%s python manage.py test -s' % environment, ]
#     else:
#         migrate = '%s python manage.py migrate --delete-ghost-migrations'
#         commands_list = [
#             migrate % environment,
#             '%s python manage.py lh_synccompress' % environment,
#             '%s python manage.py compilemessages' % environment, ]
#     # '%s python manage.py test -s'%environment, ]
#     return run_commands(commands_list,
#                         directory=dowant_dir)


