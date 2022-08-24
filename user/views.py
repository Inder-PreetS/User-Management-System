from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User as DjangoUser
from django.core.exceptions import ValidationError
from django.http import request
from django.shortcuts import HttpResponse, redirect, render, resolve_url
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

# from .forms import CompanyForm
from user.models import *

from .models import *
from .models import User

# Create your views here.

class login(View):
    def post(self, request):
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        # print(user_name, password)
        
        try:
            user = User.objects.get(email=user_name)
            # print(user)
            user = authenticate(username=user.email, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                # messages.info(request, "Login success")
                    return redirect('index')
                else:
                    return redirect('login')
            else:
                messages.warning(request, 'Invalid Password')
                return render(request, 'login.html')
        except:
            messages.warning(request, 'Invalid Username')
            return render(request, 'login.html')
            
    def get(self, request):
        return render(request, 'login.html')


class logout(View):
    def get(self, request):
        auth_logout(request)
        return render(request, 'login.html')

class registration(View):
    def get(self, request):
        return render(request, 'registration.html')	
    
    def post(self,request):
        user_name = request.POST['user_name']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['pass']
        password2 = request.POST['confpass']
        phoneNumber = request.POST['phoneNumber']
        dateOfBirth = request.POST['dateOfBirth']
        address = request.POST['address']
        images = request.FILES.getlist('images', None)

		

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email Exists')
            return redirect('registration')
            
		
        if password1 == password2:
            formdata = User.objects.create_user(user_name=user_name,first_name=first_name,last_name=last_name,email=email,password=password1,phoneNumber=phoneNumber,dateOfBirth=dateOfBirth,address=address)
            for image in images:
                image = Images(user=formdata, images=image)
                image.save()
            
            return redirect('login')
        else:
            messages.info(request,"Password doesn't match")
            return render(request, 'registration.html')






class index(LoginRequiredMixin, View):
    def get(self,request):
        data = User.objects.all()
        data2 = Images.objects.all()
        
        return render(request,'index.html',{"data":data,"data2":data2})
    

class profile(View):
    def get(self,request,id):
        info = []
        data = User.objects.all()
        data2 = Images.objects.all()
        for ids in data:
            info.append(ids.id)
            data = User.objects.get(id=ids.id)
        return render(request,'profile.html',{"data":info,"data2":data2})

    def post(self,request,id):
        
        data = User.objects.get(pk=id)
        data2 =Images.objects.filter(user=data).delete()
        
        user_name = request.POST.get('user_name', None)
        email = request.POST.get('email', None)
        
        
        # if User.objects.filter(email=email).exists():
        #     messages.warning(request, 'Email Exists')
        #     return redirect('profile',data.id)
    

        first_name = request.POST.get('first_name', None)
        address = request.POST.get('address', None)
        dateOfBirth = request.POST.get('dateOfBirth', None)
        phoneNumber = request.POST.get('phoneNumber', None)
        images = request.FILES.getlist('images', None)


        for image in images:
            image = Images(user=data, images=image)
            image.save()
        
        

        data.user_name = user_name
        data.email = email
        data.first_name = first_name
       
        data.address = address
        data.dateOfBirth = dateOfBirth
        data.phoneNumber = phoneNumber
        
        data.save()
        
        
        return render(request, 'profile.html',{"data":data,"data2":data2})


class details(View):
    def get(self,request,id):
        data = User.objects.get(pk=id)
        data3 = Images.objects.all()
        data2 = ''
        checkData = Comment.objects.filter(user=data)
        if len(checkData) != 0:
            data2= Comment.objects.filter(user=data).first()
		
        return render(request, 'details.html',{"data":data,"data2":data2,"data3":data3})

    def post(self,request,id):
        userId = request.user.id
        data = User.objects.get(pk=id)
        review = request.POST['review']
		
		

        checkComment = Comment.objects.filter(user=data, userId=userId)
        if len(checkComment) == 0:
            formdata = Comment(user=data,review=review, userId=userId)
            if request.user != data:
                formdata.save()
        else:
        	return HttpResponse("You have already given review to this Company User's profile")

        return redirect('details', data.id)



class dummy(View):
    def get(self,request):
        data3 = User.objects.all()
        data2 = Comment.objects.all()
        data = Images.objects.all()
        # return HttpResponse(data2)
        return render(request,'dummy.html',{"data2":data2,"data3":data3,"data":data})


class dummyDetails(View):
    def get(self,request,id):
        data = User.objects.get(pk=id)
        data3 = Images.objects.all()
        
        data2 = ''
        checkData = Comment.objects.filter(user=data)
        if len(checkData) != 0:
            data2= Comment.objects.filter(user=data)
            
        return render(request,'dummyDetails.html',{"data":data,"data2":data2,"data3":data3})


class editProfile(View):
    def get(self,request,id):
        data = User.objects.get(pk=id)
        return redirect('index',{"data":data})

    def post(self, request, id):
        data = User.objects.get(pk=id)
       
        user_name = request.POST.get('user_name',None)
        email = request.POST.get('email',None)
        address = request.POST.get('address',None)
        dateOfBirth = request.POST.get('dateOfBirth',None)
        phoneNumber = request.POST.get('phoneNumber',None)
        images = request.FILES.get('images', None)
        # print(images)
        # if images:
        #     data.images = images
            
        data.user_name = user_name
        data.email = email
        data.address = address
        data.dateOfBirth = dateOfBirth
        data.phoneNumber = phoneNumber
        data.images = images

        
        
        data.save()
        
        return redirect(request.META.get('HTTP_REFERER'))



class company(View):
    def get(self,request):
        data = Comment.objects.all()
        data2 = User.objects.all()
        return render(request,'company.html',{"data":data,"data2":data2})



class ali(View):
    def get(self,request):
        return render(request,'ali.html')
