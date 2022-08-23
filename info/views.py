# Importing redirect library from django
from django.shortcuts import render,redirect
# Importing Authentication luibrary of Django
from django.contrib.auth.models import User
# Importing messages library of django
from django.contrib import messages
# To authenticate for valid user on sign in
from django.contrib.auth import authenticate
# To check if the user is a valid user or not
from django.contrib.auth import login
# To check logout current user
from django.contrib.auth import logout

# Sending Email

from django.conf import settings
from django.core.mail import send_mail


# Custom Reset email

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.

def index(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
  
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request,"Your account has been successfully created")


        # Sending Email to the User

        subject = 'welcome to Machine_Era'
        message = f'Hi {myuser.username}, thank you for registering to Machine Era.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [myuser.email, ]
        send_mail( subject, message, email_from, recipient_list )

        return redirect(signin)

    return render(request, "signup.html")

def signin(request):
    if request.method=="POST":
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")

        user = authenticate(username=username, password=pass1)

        # If user is a valid user
        if user is not None:
            fname = user.first_name
            login(request,user)
            return render(request, 'index.html',{"fname":fname})
        # If user credentials are Incorrect
        else:
            messages.error(request,"Bad Credentials!")
            return redirect(index)

    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request,"logged out Sucessfuly")
    return redirect(index)

# def password_reset(request):
#     return render(request,'password_reset.html')


# def password_reset_confirm(request):
#     return render(request,'password_reset_confirm.html')


# Password Reset Request

# def password_reset_request(request):
#     if request.method=="POST":
#         password_form = PasswordResetForm(request.POST)
#         if password_form.is_valid():
#             data = password_form.cleaned_data['email']
#             user_email = User.objects.filter(Q(email=data))
#             if user_email.exists():
#                 for user in user_email :
#                     subjects = 'Password Request'
#                     email_template_name = 'password_reset_email.txt'
#                     parameters = {
#                         'email': user.email,
#                         'domain':'127.0.0.1:8000',
#                         'site_name':'MachineEra',
#                         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                         'token':default_token_generator.make_token(user),
#                         'protocol':'http',
#                     }
#                     email = render_to_string(email_template_name, parameters)
#                     try:
#                         send_mail(subject, email, '',[user.email], fail_silently=False)
#                     except:
#                         return HttpResponse('Invalid Header')
#                     return redirect('password_reset_done')
#     else:
#         password_form = PasswordResetForm()
#     context={
#         'password_form':password_form,
#     }
#     return render(request, 'password_reset.html',context)




def password_reset(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					parameters = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'MachinEra',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, parameters)
					try:
						send_mail(subject, email, '' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ('password_reset_done')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})




# def password_reset(request):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = User.objects.filter(Q(email=data))
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
# 					email_template_name = "main/password/password_reset_email.txt"
# 					c = {
# 					"email":user.email,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return redirect (password_reset_done)
# 	password_reset_form = PasswordResetForm()
# 	return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form})


