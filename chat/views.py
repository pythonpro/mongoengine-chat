from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mongoengine.django.auth import User
from mongoengine.queryset import Q
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned
from forms import MessageForm
from documents import Message


def index(request):
    """Main page."""
    if request.user.is_authenticated():
        all_users = User.objects.filter(pk__ne=request.user.pk).order_by(
            "username")
        udata = []
        for u in all_users:
            all_m_count = Message.objects.filter(
                Q(author=request.user, addressee=u) | Q(
                    author=u, addressee=request.user)).count()
            unread_count = Message.objects.filter(author=u,
                                                  addressee=request.user,
                                                  read=False).count()
            udata.append((u.username, all_m_count, unread_count))
        return render(request, 'index.html', {"udata": udata})
    else:
        return render(request, 'index.html')


@login_required
def chat(request, username):
    """Chat page."""
    try:
        # adressee. do not allow user to chat with himself.
        user = User.objects.get(pk__ne=request.user.pk, username=username)
    except (DoesNotExist, MultipleObjectsReturned):
        raise Http404
    all_messages = Message.objects.filter(
        Q(author=request.user, addressee=user) | Q(
            author=user, addressee=request.user)).order_by("created")
    # Mark unread messages as read.
    all_messages.filter(author=user, read=False).update(set__read=True)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.addressee = user
            message.save()
            return redirect("chat", user.username)
    else:
        form = MessageForm()
    return render(request, 'chat.html', {"addressee": user, "form": form,
                                         "all_messages": all_messages})
