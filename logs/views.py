from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Topic
from .forms import TopicForm
from django.http import Http404

@login_required
def index(request):
    return render(request, 'logs/index.html')
@login_required
def topics(request):
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'logs/topics.html', context)
@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('logs:topics'))

    context = {'form': form}
    return render(request, 'logs/new_topic.html', context)
from django.shortcuts import render, redirect
from .models import Topic
from .forms import EntryForm
@login_required
def new_entry(request, topic_id):
    """Add a new entry for a topic."""
    
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('logs:topic', topic_id=topic_id)

    context = {'topic': topic, 'form': form}
    return render(request, 'logs/new_entry.html', context)
from django.shortcuts import render, redirect
from .models import Entry
from .forms import EntryForm
@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logs:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'logs/edit_entry.html', context)
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')

    context = {'topic': topic, 'entries': entries}
    return render(request, 'logs/topic.html', context)