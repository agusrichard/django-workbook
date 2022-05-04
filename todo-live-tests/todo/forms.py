from django.contrib.auth.models import User
from django.forms import ModelForm, PasswordInput

from .models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget = PasswordInput()
        self.fields["username"].widget.attrs.update({"class": "form-control"})
        self.fields["password"].widget.attrs.update({"class": "form-control"})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
