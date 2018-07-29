# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from .models import Premium
from django.http import HttpResponse

# Create your views here.
def request_course_creator(request):
    """
    User has requested course creation access.
    """
    user_requested_access(request.user)
    return render(request)


def add_user_with_status_unrequested(user):
    """
    Adds a user to the course creator table with status 'unrequested'.

    If the user is already in the table, this method is a no-op
    (state will not be changed).

    If the user is marked as is_staff, this method is a no-op (user
    will not be added to table).
    """
    _add_user(user, Premium.UNREQUESTED)


def user_requested_access(user):
    """
    User has requested course creator access.

    This changes the user state to CourseCreator.PENDING, unless the user
    state is already CourseCreator.GRANTED, in which case this method is a no-op.
    """
    user = Premium.objects.get(user=user)
    if user.state != Premium.GRANTED:
        user.state = Premium.PENDING
        user.save()


def _add_user(user, state):
    """
    Adds a user to the course creator table with the specified state.

    Returns True if user was added to table, else False.

    If the user is already in the table, this method is a no-op
    (state will not be changed, method will return False).

    If the user is marked as is_staff, this method is a no-op (False will be returned).
    """
    if Premium.objects.filter(user=user).count() == 0:
        entry = Premium(user=user, state=state)
        entry.save()
        return True

    return False


########################################################################

def premium_list(request):
	premiums = Premium.objects.all()
	choices = Premium.STATES
	states = []
	for choice in choices:
		states.append(str(choice[0]))
	return render(request, 'CoursePremium/premium_list.html', {'premiums':premiums, 'states':states})



def update_state(request):
    
    t_state = str(request.GET['id_state'])

    t_id = request.user.id
    obj = Premium.objects.get(id=t_id)
    obj.state = t_state
    obj.save()
    return HttpResponse(t_state) # Sending an success response


# @receiver(post_init, sender=Premium)
# def post_init_callback(sender, **kwargs):
#     """
#     Extend to store previous state.
#     """
#     instance = kwargs['instance']
#     instance.orig_state = instance.state


# @receiver(post_save, sender=Premium)
# def post_save_callback(sender, **kwargs):
#     """
#     Extend to update state_changed time and fire event to update course creator group, if appropriate.
#     """
#     instance = kwargs['instance']
#     # We only wish to modify the state_changed time if the state has been modified. We don't wish to
#     # modify it for changes to the notes field.
#     if instance.state != instance.orig_state:
#         granted_state_change = instance.state == Premium.GRANTED or instance.orig_state == Premium.GRANTED
        
#         # If user has been denied access, granted access, or previously granted access has been
#         # revoked, send a notification message to the user.
#         if instance.state == CourseCreator.DENIED or granted_state_change:
#             send_user_notification.send(
#                 sender=sender,
#                 user=instance.user,
#                 state=instance.state
#             )

#         # If the user has gone into the 'pending' state, send a notification to interested admin.
#         if instance.state == CourseCreator.PENDING:
#             send_admin_notification.send(
#                 sender=sender,
#                 user=instance.user
#             )

#         instance.state_changed = timezone.now()
#         instance.orig_state = instance.state
#         instance.save()
