import email
from gc import get_objects

from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from myapp.forms import RegisterForm, ApplicationCreateForm
from myapp.models import Users, Roles, Event, Application, Revie


def uikit(request):
    return render(request, 'uikit.html')
# Create your views here.



def main_page(request):
    events = Event.objects.all()
    for event in events:
        event.reviews_list = Revie.objects.filter(
            id_aplic__id_con_event__id_event=event
        ).select_related('id_aplic__id_user')
        context = {'events': events}
    return render(request, 'main_page.html', context)




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
            custom_user = Users.objects.filter(login=request.user.username).first()
            if custom_user:
                application.id_user = custom_user  # Передаем найденный объект Users
                application.save()  # Сохраняем в базу данных
                return redirect('personal_account')  # Перенаправляем в личный кабинет
            else:
                return render(request, '404.html' )
    else:
        form = ApplicationCreateForm()
        context = {'form': form}
    return render(request, 'create_application.html', context)

def personal_account(request):
    custom_user = Users.objects.filter(login=request.user.username).first()
    applications = Application.objects.filter(id_user=custom_user).select_related('id_con_event')[:5]
    for item in applications:
        item.total_price = item.id_con_event.id_event.price * item.quantity_sit
    context = {"applications": applications}
    return render(request, "base_personal_account.html", context)

def base_admin(request):
    applications = Application.objects.all().select_related('id_con_event__id_event', 'id_ststus')[:10]
    context = {"applications": applications}
    return render(request, "base_admin.html", context)

def chang_status(request,id_aplic,id_ststus):
    application = get_object_or_404(Application, pk=id_aplic)
    application.id_ststus_id = id_ststus
    application .save()
    return redirect("base_admin")

def send_review(request,app_id):
    if request.method == "POST":
        application = get_object_or_404(Application, pk=app_id)
        comment = request.POST.get('review_text', '').strip()
    if comment:
        Revie.objects.create(
            id_aplic=application,
            review=comment
        )
    return redirect('personal_account')


def custom_404(request, exception):
    return render(request, '404.html', {'request_path': request.path}, status=404)