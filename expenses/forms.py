from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model=Expense
# model = Expense tells Django which database model this form is linked to, 
# so Django can automatically generate form fields and handle saving.
        fields=['amount','category','date','note']
        widgets={
        'date': forms.DateInput(attrs={'class':'form-control','type':'date','id':'datepicker'}),

        }

# fields = '__all__'
# Then:  User can select any user
# Serious security flaw
# Data ownership breaks
# 📌 Security rule:
# Users must never control ownership fields
