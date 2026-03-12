from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    return render(request, 'logs/index.html')


def topics(request):
    topics = Topic.objects.order_by('date_added')
    return render(request, 'logs/topics.html', {'topics': topics})


def topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    entries = topic.entry_set.order_by('-date_added')

    return render(request, 'logs/topic.html',
                  {'topic': topic, 'entries': entries})


def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('logs:topics')

    return render(request, 'logs/new_topic.html', {'form': form})


def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('logs:topic', topic_id=topic.id)

    return render(request, 'logs/new_entry.html',
                  {'topic': topic, 'form': form})


def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic

    # owner check
    if entry.owner != request.user:
        messages.error(request, "You can't edit this entry.")
        return redirect('logs:topics')

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('logs:topic', topic_id=topic.id)

    return render(request, 'logs/edit_entry.html',
                  {'entry': entry, 'topic': topic, 'form': form})


def delete_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    if topic.owner != request.user:
        messages.error(request, "You can't delete this topic.")
        return redirect('logs:topics')

    topic.delete()
    messages.success(request, "Topic deleted successfully.")
    return redirect('logs:topics')


def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    if entry.owner != request.user:
        messages.error(request, "You can't delete this entry.")
        return redirect('logs:topics')

    topic_id = entry.topic.id
    entry.delete()
    messages.success(request, "Entry deleted successfully.")
    return redirect('logs:topic', topic_id=topic_id)