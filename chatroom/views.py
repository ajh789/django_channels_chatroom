import haikunator
from django.db import transaction
from django.urls import reverse
from django.shortcuts import render, redirect
from chatroom.models import Room

# Create your views here.
def about(request):
    return render(request, 'chatroom/about.html')

def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.Haikunator().haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(reverse('chatroom:chat_room', args=(label,)))

def chat_room(request, label):
    room, created = Room.objects.get_or_create(label=label)

    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, 'chatroom/room.html', {'room': room, 'messages': messages})