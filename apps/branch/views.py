# coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from labmachine.apps.branch.models import Branch
from labmachine.apps.branch.models import retrieve_branch
from labmachine.apps.branch.constants import CREATE_STEPS
from labmachine.apps.branch.constants import REMOVE_STEPS
from labmachine.apps.branch.create_helpers import action_submit


def list(request):
    """
    Show all the branches installed ordered alphabetically
    by dev and branch name
    """
    list_of_branches = Branch.objects.all().order_by('dev', 'branch')
    return render_to_response('list.html',
                              {'list_of_branches': list_of_branches})


def create(request):
    return render_to_response('create.html',
                              {'step_list': CREATE_STEPS})


@csrf_exempt
def create_submit(request):
    return action_submit(request, action='install')


def update(request, dev, branch):
    branch_object = retrieve_branch(dev=dev, branch=branch)
    return render_to_response('update.html',
                              {'branch_object': branch_object})


@csrf_exempt
def update_submit(request):
    return action_submit(request, action='update')


def delete(request, dev, branch):
    branch_object = retrieve_branch(dev=dev, branch=branch)
    return render_to_response('delete.html',
                              {'branch_object': branch_object,
                               'step_list': REMOVE_STEPS})


@csrf_exempt
def delete_submit(request):
    return action_submit(request, action='remove')


# def view(request, branch_id):
    
#     ## branch = retrieve_object(branch_id)
    
#     return HttpResponse("branch %s" % branch_id)
