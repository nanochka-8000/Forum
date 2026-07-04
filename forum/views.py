from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import RegisterForm, LoginForm, ThemeForm, AnswerForm
from .models import User, Theme, Answer



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
    authentication_form = LoginForm
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('home')

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ThemeListView(ListView):
    model = Theme
    template_name = 'forum/home.html'
    context_object_name = 'themes'
    paginate_by = 5


class ThemeDetailView(DetailView):
    model = Theme
    template_name = 'forum/theme_detail.html'
    context_object_name = 'theme'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        from django.core.paginator import Paginator
        context = super().get_context_data(**kwargs)
        answers_qs = self.object.answers.all()
        paginator = Paginator(answers_qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        context['answers'] = context['page_obj'].object_list
        context['is_paginated'] = context['page_obj'].has_other_pages()
        context['form'] = AnswerForm()
        return context


class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'forum/theme_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('theme_detail', kwargs={'pk': self.object.pk})


class ThemeUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'forum/theme_form.html'

    def get_success_url(self):
        return reverse('theme_detail', kwargs={'pk': self.object.pk})


class ThemeDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Theme
    template_name = 'forum/theme_confirm_delete.html'
    success_url = reverse_lazy('home')


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.theme = get_object_or_404(Theme, pk=self.kwargs['theme_pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('theme_detail', kwargs={'pk': self.kwargs['theme_pk']})

    def get(self, request, *args, **kwargs):
        return redirect('theme_detail', pk=self.kwargs['theme_pk'])

class AnswerUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'forum/answer_form.html'

    def get_success_url(self):
        return reverse('theme_detail', kwargs={'pk': self.object.theme.pk})


class AnswerDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Answer
    template_name = 'forum/answer_confirm_delete.html'

    def get_success_url(self):
        return reverse('theme_detail', kwargs={'pk': self.object.theme.pk})

class ProfileView(DetailView):
    model = User
    template_name = 'forum/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        from django.core.paginator import Paginator
        context = super().get_context_data(**kwargs)
        themes_qs = self.object.themes.all()
        paginator = Paginator(themes_qs, 5)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginator.get_page(page_number)
        context['themes'] = context['page_obj'].object_list
        context['is_paginated'] = context['page_obj'].has_other_pages()
        return context


class CabinetRedirectView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('profile', username=request.user.username)