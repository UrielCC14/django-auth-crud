from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import Create_Task_Form
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.
def Home(request):
    return render(request,'home.html')

def SignUp(request):
    #Analizamos si usa el metodo POST o GET.
    #Si usa GET le mostramos la pagina pagina con el formulario.
    if request.method == 'GET':
        return render(request,'signup.html',{
            'form':UserCreationForm
        })
    #Si usa POST significa que enviara datos, por lo que los extraemos
    else:
        #Validamos que las contraseñas sean iguales
        if request.POST['password1'] == request.POST['password2']:
            try:
                #register User
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                #Guardando Usuario
                user.save()
                #Creando la cockie para el usuario registrado
                login(request,user)
                #Redireccionamos a Task
                return redirect('task')
            #Manejamos un error especifico: Integriti error (Usuario repetido).
            except IntegrityError:
                #Redireccionamos a la misma pagina
                return render(request,'signup.html',{
                    'form':UserCreationForm,
                    'error':'Username already exist'
                })
        #Renderizamos la misma pagina si las contraseñas no coinciden        
        return render(request,'signup.html',{
            'form':UserCreationForm,
            'error':'Password dont Match'
        })

@login_required  
def Tasks(request):
    tittle = 'Task Pending'
    tasks = Task.objects.filter(user = request.user,datecompleted__isnull = True)
    return render(request,'Task.html',{
        'tasks' : tasks,
        'tittle':tittle
    })
    
@login_required
def Tasks_Completed(request):
    tittle = 'Task Completed'
    tasks = Task.objects.filter(user = request.user,datecompleted__isnull = False).order_by('-datecompleted')
    return render(request,'Task.html',{
        'tasks' : tasks,
        'tittle':tittle
    })

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def SignIn(request):
    if request.method == 'GET':
        return render(request,'Signin.html',{
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(request,username= request.POST['username'],password = request.POST['password'])
        if user is None:
            return render(request,'Signin.html',{
                'form': AuthenticationForm,
                'error':'username or password is incorrect'
            })
        else:
            login(request,user)
            return redirect('task')
@login_required
def Create_Task(request):
    
    if request.method == 'GET':
        return render(request,'Create_Task.html',{
            'form':Create_Task_Form
        })
    
    else:
        try: 
            form = Create_Task_Form(request.POST)
            new_Task = form.save(commit=False)
            new_Task.user = request.user
            new_Task.save()
            return redirect('task')
        except ValueError:
            return render(request,'Create_Task.html',{
                'form':Create_Task_Form,
                'error': 'Pleace provide valid data'
            })
@login_required
def Task_Detail(request,id):    
    if request.method == 'GET':
        task = get_object_or_404(Task,id= id,user =  request.user)
        form = Create_Task_Form(instance=task)
        return render(request, 'Task_Detail.html',{
            'task':task,
            'form':form
        })
    else:
        try:
            task = get_object_or_404(Task,id= id,user =  request.user)
            form = Create_Task_Form(request.POST,instance=task)
            form.save()
            return redirect('task')
        except ValueError:
            return render(request, 'Task_Detail.html',{
                'task':task,
                'form':form,
                'error': 'Error updating Task'
            })
            
@login_required
def Task_Complete(request,id):
    task = get_object_or_404(Task, id= id,user = request.user)
    if request.method == 'POST':
        task.datecompleted =  timezone.now()
        task.save()
        return redirect('task')

@login_required
def Task_Delete(request,id):
    task = get_object_or_404(Task, id= id,user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task')