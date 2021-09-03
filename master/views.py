from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Documents

# Create your views here.
def index(request):
    return render(request, "master/index.html", {"documents":Documents.objects.filter(expiry__lte=datetime.now()+timedelta(days=60)).order_by('expiry')})

def documents(request):

    return render(request, "master/documents.html", {"documents":Documents.objects.order_by('expiry')})