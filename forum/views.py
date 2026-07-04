from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')