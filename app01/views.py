from django.shortcuts import render,redirect
from django.contrib import auth
# Create your views here.
from app01 import models


def login(request):
    if request.method=="POST":

        user = auth.authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            auth.login(request, user)

            return redirect('/questionnairemanage/')
    return render(request,'login.html')


def questionnairemanage(request):
    questionnaire_list=models.Questionnaire.objects.filter(creator=request.user)
    return render(request,'questionnairemanage.html',{'questionnaire_list':questionnaire_list})
