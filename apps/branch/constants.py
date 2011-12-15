# coding=utf-8

REMOVE_STEPS = ('remove_directory',
                'remove_virtualenv',
                'remove_rabbit_vhost',
                'remove_database',
                'remove_db_entry',
                'restart_services',)

UPDATE_STEPS = ('update_repo',
                'remove_pyc_files',
                'install_config_files',
                'install_pip_requirements',
                'install_django_stuff',
                'restart_services',)

CREATE_STEPS = ('install_db_entry',
                'install_dir_struct_pre_repo',
                'install_repo',
                'install_branch',
                'install_dir_struct_post_repo',
                'install_virtualenv',
                'install_config_files',
                'install_rabbit_vhost',
                'install_pip_requirements',
                'install_database',
                'install_django_stuff',
                'restart_services',)


# 1. All tasks should be before restart_services
# 2. Tasks regarding update should be before install
# (because update proc. uses several install steps)
# 3. Delete tasks could be anywhere else.

    # FIXME generate create/upd/etc. dinamically with this dict:

STEPS_ORDER = []
for step_list in (REMOVE_STEPS, UPDATE_STEPS, CREATE_STEPS):
    for step in step_list:
        if step in STEPS_ORDER:
            STEPS_ORDER.remove(step)
        STEPS_ORDER.append(step)

