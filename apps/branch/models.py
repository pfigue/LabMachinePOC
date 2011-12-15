# coding=utf-8

"""
models.py
Data model for cont_building app.
"""

import re
import datetime
from os.path import join
from django.db import models
from django.conf import settings as django_settings


def sanitize_branch_name(branch_str):
    """
    Table names in Postgres aren't allowed to
    have /- characters. Uppercase should be converted to lower.
    There is a similar problem with paths in filesystem.

    Returns the name in lowercase with those chars. replaced by _
    """
    good_name = re.sub('[/-]', '_', branch_str.lower())
    return good_name


def sanitize_branch_for_uri(branch_str):
    """
    For the URI we shouldn't have _ in the subdomain
    NOTE: Internet Explorer doesn't work properly with cookies
    if the subdomain includes '_'
    """
    good_name = re.sub('[/_]', '-', branch_str.lower())
    return good_name


def retrieve_branch(id_branch=None, dev=None, branch=None):
    if dev is None and branch is None:
        my_branch = Branch.objects.get(id_branch=id_branch)
    elif id_branch is None:
        my_branch = Branch.objects.get(dev=dev, branch=branch)
    else:
        print('jander more jiar!') # FIXME
    return my_branch


class Branch(models.Model):
    """
    Every installed branch stores its info. here: directories, URI, names, etc.
    """
    id_branch = models.CharField(max_length=64, primary_key=True)

    dev = models.CharField(max_length=30)
    branch = models.CharField(max_length=200)
    # cleared_branch = models.CharField(max_length=200)

    # dev_email = models.EmailField()
    # notes = models.TextField()
    # git_repo = models.CharField(max_length=200)
    # project_name = models.CharField(max_length=200)
    # cleared_project_name = models.CharField(max_length=200)
    directory = models.CharField(max_length=200)
    # code_dir = models.CharField(max_length=200)
    log_dir = models.CharField(max_length=200)
    # config_dir = models.CharField(max_length=200)
    virtualenv_dir = models.CharField(max_length=200)
    # db_name = models.CharField(max_length=200)
    # uri = models.CharField(max_length=200)
    # broker_vhost = models.CharField(max_length=200)
    # settings_file_path = models.CharField(max_length=200)
    uwsgi_port = models.IntegerField()

    # lettuce_mode = models.BooleanField()

    # state = models.ForeignKey('State')
    # state_last_mod = models.DateTimeField()
    # unittests_state = models.ForeignKey('UnitaryTestsState')
    # unittests_state_last_mod = models.DateTimeField()

    class Meta:
        unique_together = (('dev', 'branch'), )


    @property
    def git_repo(self):
        return 'git@github.com:%s/www_de.git' % self.dev


    @property
    def code_dir(self):
        return join(self.directory, 'code/')


    @property
    def settings_file_path(self):
        config_file = 'dowant/settings/lieferheld_lab.py'
        return join(self.code_dir, config_file)


    @property
    def db_name(self):
        branch = sanitize_branch_name(self.branch)
        db_name = 'dowant_test_%s_%s' % (self.dev, branch)
        db_name = db_name[:63]
        return db_name


    @property
    def broker_vhost(self):
        branch = sanitize_branch_name(self.branch)
        vhost = '%s_%s' % (self.dev, branch)
        return vhost

    @property                   # FIXME review what to do with property and get_XXX()
    def uri(self):
        foo_bar = '%s.%s.%s' % (self.dev,
                             sanitize_branch_for_uri(self.branch),
                             django_settings.SUBDOMAIN)
        return foo_bar

    
    @property
    def config_dir(self):
        return join(self.directory, 'config/')


    @property
    def cleared_project_name(self): # FIXME do we need this really?
        branch = sanitize_branch_name(self.branch)
        cleared_project_name = '%s_%s' % (self.dev, branch)
        return cleared_project_name


    def __str__(self):
        return '%s / %s' % (self.dev, self.branch)


class State(models.Model):
    """
    State for every branch: installing, updating, queued
    for deletion, etc.
    """
    id = models.IntegerField(primary_key=True)
    caption = models.CharField(max_length=30)


class UnitaryTestsState(models.Model):
    """
    State of the unitary tests for every branch: doing tests,
    failed, succeeded, not yet run.
    """
    id = models.IntegerField(primary_key=True)
    caption = models.CharField(max_length=30)


class BranchEvent(models.Model):
    """
    List of events done on the branches
    Which event, when and what branch
    """
    # NOTE: don't make FK to Branch() cause we want to save
    # the events, even if we remove the branches
    id_branch = models.CharField(max_length=200)
    dev = models.CharField(max_length=30)
    branch = models.CharField(max_length=200)
    event = models.ForeignKey('EventType')
    tstamp = models.DateTimeField(default=datetime.datetime.now)


class EventType(models.Model):
    """
    Event types: update, install, etc.
    """
    id = models.IntegerField(primary_key=True)
    caption = models.CharField(max_length=30)
