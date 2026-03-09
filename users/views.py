from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('logs:index')
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm


def register(request):
    """Register a new user."""

    if request.method != 'POST':
        form = UserCreationForm()

    else:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save()

            authenticated_user = authenticate(
                username=new_user.username,
                password=request.POST['password1']
            )

            login(request, authenticated_user)

            return redirect('logs:index')

    context = {'form': form}
    return render(request, 'users/register.html', context)