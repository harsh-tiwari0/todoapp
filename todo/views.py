from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required 
from . import models


@login_required(login_url='/login')
def home(request):
    return render(request, 'signup.html')



def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        confirm_pwd = request.POST.get('confirm_pwd')

        if pwd != confirm_pwd:
            messages.error(request, "Passwords do not match")
            return render(request, 'signup.html')

        if User.objects.filter(email=emailid).exists():
            messages.error(request, "Email already registered")
            return render(request, 'signup.html')

        my_user = User.objects.create_user(username=fnm, email=emailid, password=pwd)
        my_user.save()
        messages.success(request, "User registered successfully")
        return redirect('/login')
    
    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        emailid = request.POST.get('emailid')
        pwd = request.POST.get('pwd')
        

        try:
            user = User.objects.get(email=emailid)
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return render(request, 'login.html')

       
        user = authenticate(request, username=user.username, password=pwd)

        if user is not None:
            
            auth_login(request, user)
            messages.success(request, "Login successful")
            return redirect('todo_page')  
        else:
            messages.error(request, "Invalid credentials")
            return render(request, 'login.html')

    return render(request, 'login.html')

def user_logout(request):
    logout(request) 
    return redirect('user_login') 

@login_required(login_url='/login')
def todo_page(request):
    
    if request.method == 'POST':
        
        title = request.POST.get('title')
        if title:  
            obj = models.TODOO(title=title, user=request.user)
            obj.save()
            return redirect('/todo_page') 

    # Get the tasks to display in the page
    res = models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo_page.html', {'res': res})

@login_required(login_url='/login')
def delete_todo(request, srno):
    if request.method == 'POST':
        try:
            obj = models.TODOO.objects.get(srno=srno, user=request.user)
            obj.delete()
        except models.TODOO.DoesNotExist:
            pass  

    return redirect('/todo_page')  

@login_required(login_url='/login')
def edit_todo(request, srno):
    
    obj = models.TODOO.objects.get(srno=srno, user=request.user)
    
    if request.method == 'POST':
        
        title = request.POST.get('title')
        if title:
            obj.title = title
            obj.save()
        return redirect('/todo_page') 

    
    return render(request, 'edit_todo.html', {'obj': obj})

@login_required(login_url='/login')
def delete_all_todos(request):
    
    if request.method == 'POST':
        models.TODOO.objects.filter(user=request.user).delete()
    
    return redirect('/todo_page')  
