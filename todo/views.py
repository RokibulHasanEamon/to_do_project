from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import TodoItem

from django.contrib.auth.decorators import login_required


# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    else:

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            
            else:
                messages.info(request, 'username or password is incorrect! Try again.')

        return render(request,'login.html')



def logoutpage(request):
    logout(request)
    return redirect('login')

def registerpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

        form = UserCreationForm()
        
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account created succesfully! please login ' + user)
                return redirect('login')


        context = {'form' : form}
        return render(request,'register.html', context)

@login_required(login_url='login')
def todoView(request):
    all_todo_items = TodoItem.objects.all()
    return render(request,'todo.html',{'all_items':all_todo_items})


def addTodo(request):
    c = request.POST['content']
    new_item = TodoItem(content = c)
    new_item.save()
    return HttpResponseRedirect('/')

def delleteTodo(request, todo_id):
    item_to_dellete = TodoItem.objects.get(id = todo_id)
    item_to_dellete.delete()
    return HttpResponseRedirect('/')

