from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

from .forms import RegisterForm


class RegisterView(View):
    template_name = 'users/signup.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('quotes_app:main')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Account {username} has been registered successfully')
            return redirect('users:login')
        return render(request, self.template_name, {'form': form})
