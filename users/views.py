from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import UserRegistrationForm, EmailAuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            try:
                send_mail(
                    subject='Добро пожаловать!',
                    message='Спасибо за регистрацию на нашем сайте.',
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=True,
                )
            finally:
                pass
            return redirect('catalog:product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


class EmailLoginView(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'users/login.html'
    next_page = reverse_lazy('catalog:product_list')


def user_logout(request):
    logout(request)
    return redirect('catalog:product_list')
