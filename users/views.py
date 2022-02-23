from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http.response import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse

from .forms import SignUpForm

def index(request):
    return render(request,"users/index.html")

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('User created successfully!')

        return HttpResponse(f"{form.errors}")
    if request.method == "GET":
        form = SignUpForm()
        return render(request, 'users/signUp.html', {'form': form})


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("tasks:index"))

            else:
                return HttpResponse("Invalid username or password.")

        else:
            return HttpResponse("Invalid username or password.")

    if request.method == "GET":
        form = AuthenticationForm()
        return render(request=request,
                      template_name="users/logIn.html",
                      context={"form": form})


def logout_request(request):
    logout(request)
    return HttpResponse("Logged out successfully!")
