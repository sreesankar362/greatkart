import contextlib
from django.contrib.auth import authenticate,login as loginfn,logout
from django.contrib import messages,auth
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from accounts.forms import RegistrationForm
from accounts.models import Account
from django.contrib.auth.decorators import login_required
from cart.models import CartModel,CartItem
from cart.views import _cart_id
import requests

#verificationEmail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



def register(request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number = phone_number
            user.save()

             #ACCOIUNT ACTIVATION not added gmail not sending

            messages.success(request,"Regsitration Successfull")
            return redirect("login")
    else:
        form = RegistrationForm()

    context = {
        "form":form,
    }
    return render (request,"accounts/register.html",context)



# ACCOIUNT ACTIVATION code
# current_site = get_current_site(request)
# mail_subject = "Please Activate Your Account"
# message = render_to_string('accounts/account_verification_email.html',{
#     'user':user,
#     'domain':current_site,
#     'uid' :urlsafe_base64_encode(force_bytes(user.pk)), 
#     'token': default_token_generator.make_token(user),
# })
# to_mail = email
# send_mail = EmailMessage(mail_subject, message, to=[to_mail])
# send_mail.send()

# class SignInView(View):

#     def get(self, request, *args, **kwargs):
#         return render (request,"accounts/login.html")

#     def post(self,request,*args,**kwargs):

#             email =  request.POST["email"]
#             password =request.POST["password"]
#             print(email,password)
#             user = authenticate(request, email=email, password=password)
#             print(user)
#             if user:
#                 login(request,user)
#                 return redirect("home")
#             else:
                
#                 messages.error(request,"Invalid Credentials")
#                 return redirect ("login")

def login(request):

    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        print(user,email,password)

        if user is not None:
            try:
                cart = CartModel.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(dict(variation))


                    #get cart item with user
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    #to getcommon pdt variation
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id(index)
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            loginfn(request, user)
            messages.success(request,"Login Successfull")
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect ('dashboard')
            
        else:
            messages.error(request,"Invalid Login Credentials!")
            return redirect ('login')

    return render (request,'accounts/login.html')


@login_required(login_url="login")
def user_logout(request):
    logout(request)
    messages.success(request,"Succesfully Logged Out")
    return redirect("login")



# def activate(request,uidb64,token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user =None
#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, "congratulations your account is activated")
#         return redirect ("login")
#     else:
#         messages.error(request,"Invalid Activation Link !")
#         return redirect("register")


@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')



def forgotPassword(request):
    if request.method =='POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid' :urlsafe_base64_encode(force_bytes(user.pk)), 
                'token': default_token_generator.make_token(user),
            })
            to_mail = email
            send_mail = EmailMessage(mail_subject, message, to=[to_mail])
            send_mail.send()
            messages.success(request,"Password reset email has been sent to your mail address")
            return redirect('login')

        else:
            messages.error(request,"Account Doesnt Exist")
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')