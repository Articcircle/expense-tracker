from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.db.models import Sum

def signup(request):
    if(request.method=="POST"):
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"Account Created Successfully.")
            return redirect('expense_list')
        #expense_list is a url pattern name 
    else:
        form=UserCreationForm()

    return render(request,"signup.html",{'form':form})
# {'form':form} -> This is a Python dictionary used to send data from a view to a template.

@login_required
def expense_list(request):
    category=request.GET.get('category')
    start_date=request.GET.get('start_date')
    end_date=request.GET.get('end_date')
    expenses = Expense.objects.filter(user= request.user)
    if category:
        expenses=expenses.filter(category=category)

    if start_date and end_date:
        expenses= expenses.filter(date__range=[start_date,end_date])
# In Django ORM, date range filtering uses __range lookup, not date_range.

    total_expense= expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    #aggregate returns dictionary
#amount__sum -> Extracts only the numeric value
    return render(request, 'expenses/list.html', {'expenses': expenses, 'selected_category':category,
                                                  'start_date':start_date,'end_date':end_date,
                                                  'total_expense' : total_expense,
                                                  })


@login_required
def add_expense(request):
    if request.method == "POST":
        form= ExpenseForm(request.POST)
        if form.is_valid():
            expense= form.save(commit=False)
# commit=False tells Django not to save the form data to the database immediately,
# so we can modify the object before saving it.
# 3️⃣Without commit=False (Problem)
# ❌ Django tries to save immediately
# ❌ Required fields like user may be missing
# ❌ Results in IntegrityError

# 4️⃣ With commit=False (Correct Way)
# ✔ Object created in memory
# ✔ Required fields added manually
# ✔ Saved safely to database
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form=ExpenseForm()
    
    return render(request,'expenses/add.html',{'form':form})

@login_required
def delete_expense(request,id):
    expense= get_object_or_404(Expense,id=id,user=request.user)
    if request.method=="POST":
        expense.delete()
        messages.success(request,"Expense deleted successfully.")
        return redirect('expense_list')

    return render(request,'expenses/delete.html',{'expense':expense})


@login_required
def edit_expense(request,id):
    expense= get_object_or_404(Expense,id=id,user=request.user)
    if request.method =="POST":
        form= ExpenseForm(request.POST, instance=expense)
# “Apply this form’s data to this specific object, not a new one.”
        if form.is_valid:
            form.save()
            return redirect('expense_list')

    else:
        form= ExpenseForm(instance=expense)
    return render(request,'expenses/edit.html',{'form':form})


from django.db.models.functions import TruncMonth

@login_required
def monthly_summary(request):
    summary= (
        Expense.objects.filter(user=request.user).annotate(month= TruncMonth('date'))
        .values('month').annotate(total=Sum('amount')).order_by('month')
    )
    return render(request,'expenses/monthly.html',{'summary':summary})

