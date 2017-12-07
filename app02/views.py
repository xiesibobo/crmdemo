from django.shortcuts import render,HttpResponse

# Create your views here.
def subscrib(request):
    return render(request,'subscribemeeting.html')