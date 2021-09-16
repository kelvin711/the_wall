from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt

def register_login(request):
    return render(request, "register_login.html")

def register(request):
    print(request.POST)
    print("%" *70)
    print(User.objects.reg_validator(request.POST))
    print("%" *70)
    
    #check if register object is valid
    errors = User.objects.reg_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags =key)
        return redirect("/")

    #check to see if email is in use
    user = User.objects.filter(email=request.POST['emailReg'])
    if user:
        messages.error(request, "Email is already in use.", extra_tags ="emailReg" )
        return redirect("/")

    #hash the password with bcrypt
    pw = bcrypt.hashpw(request.POST['passwordReg'].encode(),bcrypt.gensalt()).decode()

    #create user in database
    User.objects.create(
        firstname = request.POST['firstnameReg'],
        lastname = request.POST['lastnameReg'],
        email = request.POST['emailReg'],
        password = pw
    )

    # put user id into session and redirect
    request.session['user_id'] = User.objects.last().id
    return redirect("/dashboard")

    return redirect("/")

def dashboard(request):
    if "user_id" not in request.session: #make sure logged in
        return redirect("/")
    else:
        context = {
            "user" : User.objects.get(id=request.session['user_id']),
            "messages" : Message.objects.all(),
            "comments" : Comment.objects.all(),
        }
        return render(request, "dashboard.html", context)

def login(request):
    #check if POST request
    if request.method == "POST":
        #validate login
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect("/")
        #check if email is in database
        user = User.objects.filter(email=request.POST['loginEmail'])
        if len(user) == 0:
            messages.error(request, "Invalid Email\Password" , extra_tags="login")
            return redirect("/")
        #check if passwords match
        if not bcrypt.checkpw(request.POST['loginPassword'].encode(),user[0].password.encode()):
            messages.error(request, "Invalid Email\Password", extra_tags="login")
            return redirect("/")
        #put user id into session and redirect
        request.session['user_id'] = user[0].id
        return redirect("/dashboard")
    else:
        return redirect("/")

    return redirect("/dashboard")

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']

    return redirect("/")

def create_message(request):
    print(request.POST)
    newMessage = Message.objects.create(
        messageText = request.POST['message'],
        user = User.objects.get(id= request.session['user_id'])
    )

    return redirect("/dashboard")

def create_comment(request, message_id):
    print(request.POST)
    newComment = Comment.objects.create(
        comment_text = request.POST['comment'],
        user = User.objects.get(id= request.session['user_id']),
        message = Message.objects.get(id= message_id )
    )

    return redirect("/dashboard")