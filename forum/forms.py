from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import Theme, Answer


class RegisterForm(UserCreationForm):
    avatar = forms.ImageField(required=True, label='Аватар')

    class Meta:
        model = User
        fields = ('username', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'avatar':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ваш ответ...'
            }),
        }
        labels = {'content': ''}