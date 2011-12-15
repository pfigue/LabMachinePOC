from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns
from django.shortcuts import render_to_response
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
from django.views.generic import list_detail
from labmachine.apps.branch.models import Branch

urlpatterns = patterns('labmachine.apps.branch.views',
                       url(r'^list/$', list_detail.object_list,
                           {'queryset': Branch.objects.all().order_by('dev', 'branch')},
                           name="branch-list"),

                       url(r'^create/$', 'create', name='branch-create'),
                       url(r'^create-submit/$', 'create_submit', name="branch-create-submit"),
    
    # url(r'^(\d)+$', 'view', name="branch-view"),
    
    # url(r'^create/$', 'create', name="branch-create"),

    # # url(r'^delete/(?P<id_branch>\w+)/$', 'delete', name="branch-delete"),
                       url(r'^delete/(?P<dev>\w+)/(?P<branch>[\w-]+)/$', 'delete', name="branch-delete"),
                       # FIXME waht about / in branch name?
                       url(r'^delete-submit/$', 'delete_submit', name="branch-delete-submit"),

    # # url(r'^update/(?P<id_branch>\w+)/$', 'update', name="branch-update"),
                       url(r'^update/(?P<dev>\w+)/(?P<branch>[\w-]+)/$', 'update', name="branch-update"),
                       # FIXME waht about / in branch name?
    # url(r'^update-submit/$', 'update_submit', name="branch-update-submit"),
                       )
