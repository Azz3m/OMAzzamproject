from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Profile
from django.http import JsonResponse
import urllib.parse,urllib.error,urllib.request
import json

# Create your views here.
def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'comments/home.html',{'signuperror':'username has already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'], email=request.POST['email'])
                user.profile.api_key = request.POST['key']
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request, 'comments/home.html',{'signuperror':'passwords do not mutch'})
    return render(request, 'comments/home.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['usernamelogin'],password=request.POST['passwordlogin'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'comments/home.html',{'loginerror':'username or password is innorect'})
    else:
        return render(request, 'comments/home.html')

def logout(request):
    auth.logout(request)
    return redirect('home')



def editeaccount(request):
    if request.method == 'POST':
            try:
                user = User.objects.get(username=request.POST['username'])
                user.profile.api_key = request.POST['api_key']
                user.email = request.POST['email']
                user.set_password(request.POST['password'])
                user.save()
                user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])

                auth.login(request, user)

                return JsonResponse({'state':"success"})
            except User.DoesNotExist:

                return JsonResponse({'state':"we fail to update the user information "})

    return JsonResponse({'state':"we fail to update the user information outside "})


def accountgetter(request):
    if request.method == 'POST':
        current_user = request.user
        user = get_object_or_404(User,username=current_user)
        username = user.username
        api_key = user.profile.api_key
        email = user.email
        password = user.password
        context = {
        "state":"success",
        "username":username,
        "api_key" :api_key,
        "email" :email,
        "password" :password
        }


        return JsonResponse(context)
    return JsonResponse({"state":"fail"})

def testapi(request):
    if request.method == 'POST':
        try:

            api_key = request.POST['api_key']
            base_url = 'https://www.googleapis.com/youtube/v3/videos?id=fS0g9edDIVE&key='
            complementary_url = '&part=snippet,contentDetails,statistics,status'
            validation_url = base_url + api_key + complementary_url
            api_validation_json_recieved = urllib.request.urlopen(validation_url).read()
            response_for_api_validation_details = api_validation_json_recieved.decode("utf-8")
            api_processing_recieved = json.loads(response_for_api_validation_details)
            return JsonResponse({"state":"success",'api_processing_recieved':api_processing_recieved})
        except:
            return JsonResponse({"state":"fail"})
    return JsonResponse({"state":"fail"})
