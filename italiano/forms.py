#-*- coding: utf-8 -*-
from django import forms
from italiano.models import Mot, Expression

class TestMotForm(forms.ModelForm):
    class Meta:
        model = Mot
        fields = '__all__'
