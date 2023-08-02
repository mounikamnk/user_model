from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def registration(request):
    usfo=UserForm()#create object
    pfo=ProfileForm()#create object
    d={'usfo':usfo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        usfd=UserForm(request.POST) #collect the data
        pfd=ProfileForm(request.POST,request.FILES) # collect the data
        if usfd.is_valid() and pfd.is_valid():  #check validation
            NSUFO=usfd.save(commit=False)  # don't save
            submittedpw=usfd.cleaned_data['password'] # collect the data
            NSUFO.set_password(submittedpw) # add the data
            NSUFO.save()                     # save the object
            NSPO=pfd.save(commit=False)  #don't save the data
            NSPO.username=NSUFO       # add the username
            NSPO.save()
            send_mail('registration','registration is successfully','mounika03n@gmail.com',
            [NSUFO.email],fail_silently=False)
        else:
            return HttpResponse('not valid')

        return HttpResponse('Registration is succesfully')


    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_details(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_details.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session['username']
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('password changed succesfully')
    return render(request,'change_password.html')

def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('reset password is done')
        else:
            return HttpResponse('enter valid username')



    return render(request,'reset_password.html')

    
