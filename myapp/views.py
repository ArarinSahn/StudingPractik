import email

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from myapp.forms import RegisterForm, ApplicationCreateForm
from myapp.models import Users, Roles


def uikit(request):
    return render(request, 'uikit.html')
# Create your views here.
def main_page(request):
    return render(request, 'main_page.html')
def login(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('main_page')

def registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            default_role = Roles.objects.get(id_rol=2)
            profile = Users()
            profile.id_rol = default_role
            fio = request.POST['fio']
            phone= request.POST['phone']
            email = request.POST['email']
            profile.login = user.username
            profile.password = user.password
            profile.save()
            auth_login(request, user)
            return redirect('personal_account')
        else:
            context = {'form': form}
            return render(request, 'registration.html', context)
    else:
        form = RegisterForm()
        context = {'form': form}
        return render(request, 'registration.html', context)

def create_application(request):
    if request.method == "POST":
        form = ApplicationCreateForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            profile = Users()
            application.user = request.user
            application.save()
            return redirect('personal_account')
        else:
            context = {'form': form}
            return render(request, 'create_application.html', context)
    else:
        form = ApplicationCreateForm()
        context = {'form': form}
        return render(request, 'create_application.html', context)

def personal_account(request):
    return render(request, 'base_personal_account.html')
def custom_404(request, exception):
    """Кастомная страница 404"""
    return render(request, '404.html', {'request_path': request.path}, status=404)