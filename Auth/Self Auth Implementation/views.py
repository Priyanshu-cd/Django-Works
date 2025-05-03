from django.shortcuts import render, HttpResponse,HttpResponseRedirect
from accounts import forms , models
from django.urls import reverse

def login_view(request):
    form=forms.LoginForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            email=form.cleaned_data.get('user_email')
            password=form.cleaned_data.get('user_password')

            try: 
                user_exist=models.UserModel.objects.filter(user_email=email).exists()
            except:
                user_exist=False

            if user_exist:
                # data=models.UserModel.objects.get(user_email=email,user_password=password)
                request.session['email']=email
                request.session['password']=password
                path=request.COOKIES.get("redirect")
                if path:
                    return HttpResponseRedirect(path)
                else:
                    return HttpResponseRedirect(reverse("more"))
                
            else:
                form.add_error('user_email', 'User not Exists!')
                response = HttpResponseRedirect(reverse("signup"))
                return response
            
    response = render(request,"accounts/login.html",{"form":form,"head":"LOGIN","reverse":"signup"})
    return response

def signup_view(request):
    form = forms.LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form_data=form.cleaned_data
            user_email = form_data.get("user_email")
            user_password = form_data.get("user_password")
            redirect = request.COOKIES.get('redirect')
            try:
                user_exist = models.UserModel.objects.filter(user_email=user_email,user_password=user_password).exists()
            except:
                user_exist = False

            if user_exist == False:
                models.UserModel.objects.create(user_email=user_email,user_password=user_password)

            request.session['email']=user_email
            request.session['password']=user_password
            if redirect:
                response = HttpResponseRedirect(redirect)
            else:
                response = HttpResponseRedirect(reverse("posts"))
            return response
        else:
            form = forms.LoginForm()
    return render(request,"accounts/login.html",{"form":form,"head":"SIGNUP","reverse":"login"})
