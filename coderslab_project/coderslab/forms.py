from django import forms
from django.forms import modelformset_factory
from .models import Branch, PipeOrder, MATERIAL, SIZE, WALL_THK
import math
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PipeOrderForm(forms.ModelForm):
    class Meta:
        model = PipeOrder
        # fields = "__all__"
        exclude = ['customer']


class BranchForm(forms.BaseFormSet):

    class Meta:
        model = Branch
        fields = [
            "position",
            "size",
            "angle"
        ]


BranchFormSet = modelformset_factory(
    Branch, fields=['size', 'angle', 'position']
)
