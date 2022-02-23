from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from users import models

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

class RemoveTaskForm(forms.Form):
    task = forms.CharField(label="Remove Task")

def index(request):
    return render(request, "tasks/index.html", {
        "tasks": models.Profile.objects.get(user=request.user).tasks
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            models.Profile.objects.get(user=request.user).tasks += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
        })

def remove(request):
    if request.method == "POST":
        form = RemoveTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            models.Profile.objects.get(user=request.user).tasks.remove(task)
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/remove.html", {
                "form": form
            })
    return render(request, "tasks/remove.html", {
        "form": RemoveTaskForm()
        })