from django.shortcuts import HttpResponseRedirect
from django.urls import reverse

class CustomAuthMid:
    def __init__(self,get_response):
        self.get_response=get_response
        print("Auth mid is installed!")

    def __call__(self, request):
        print("Before view")
        path=request.path
        
        email=request.session.get('email')
        password=request.session.get('password')

        if email != None and password != None and path != reverse("login"):
            response=self.get_response(request)
        elif email != None and password != None and path == reverse("login"):
            return HttpResponseRedirect(reverse("more"))
        
        elif email == None and password == None and path == reverse("login"):
            response=self.get_response(request)

        elif email == None and password == None and path == reverse("signup"):
            response=self.get_response(request)
        else:
            redirect=HttpResponseRedirect(reverse("login"))
            if path!=reverse("login") and path!='"/favicon.ico"':
                redirect.set_cookie('redirect',path)
            else :
                redirect.set_cookie('redirect',"/posts")
            return redirect

        return response
        
        