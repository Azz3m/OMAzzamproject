from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Contactus

# Create your views here.
@login_required(login_url="/accounts/signup")
def contactus(request):
    if request.method == 'POST':
        if request.POST['firstname'] and request.POST['lastname'] and request.POST['areacode'] and request.POST['telnum'] and request.POST['emailid'] and request.POST['feedback']:
            contactus = Contactus()
            contactus.firstname = request.POST['firstname']
            contactus.lastname = request.POST['lastname']
            contactus.areacode = request.POST['areacode']
            contactus.telnum = request.POST['telnum']
            contactus.email = request.POST['emailid']
            contactus.body = request.POST['feedback']
            contactus.pub_date = timezone.datetime.now()
            contactus.contact = request.user
            contactus.save()
            return render(request, 'contactus/contactus.html',  {'state':'Feedback has been sent successfuly.'})
        else:
            return render(request, 'contactus/contactus.html', {'error':'all the fields are required.'})
    else:
        return render(request, 'contactus/contactus.html')

def aboutus(request):
    return render(request, 'aboutus/aboutus.html')
