from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import Coordinator
from .models import *
import re



def RegisterView(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        errors = []  # Store error messages

        # ✅ Constraint to allow only @banasthali.in emails
        if not re.match(r'^[a-zA-Z0-9._%+-]+@banasthali\.in$', email):
            errors.append("Only @banasthali.in emails are allowed for registration.")

        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")

        if User.objects.filter(email=email).exists():
            errors.append("Email already exists.")

        if len(password) < 5:
            errors.append("Password must be at least 5 characters.")

        if errors:
            return render(request, 'signup_page.html', {
                'errors': errors, 
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email
            })  # Return form data back to page with errors

        else:
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email, 
                username=username,
                password=password
            )
            messages.success(request, "Account created successfully! You can now login.")
            return redirect('login')

    return render(request, 'signup_page.html')

def LoginView(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('profile') ### change 
        
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')

    return render(request, 'login_page.html')



def LogoutView(request):
    # Clear session data
    request.session.flush()
    
    # Logout the user
    logout(request)
    
    return redirect('login')



def ForgotPassword(request):

    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'reset_password.html')

@login_required #restrict user to suthentication only then can view profile page 
def profile(request):
    user = request.user
    
    # Check if the user is a coordinator and redirect accordingly
    if user.is_authenticated:
        if hasattr(user, 'Club Coordinator'):
            return redirect('coordinator_dashboard')  # Redirect to the club dashboard
        elif hasattr(user, 'Department Coordinator'):
            return redirect('coordinator_dashboard_dept')  # Redirect to the department dashboard

    # Default profile view for non-coordinators
    return render(request, "profile.html", {"user": user})






# def home(request):
#     coordinator_name = request.session.get('coordinator_name', None)  # Retrieve coordinator name from session
#     return render(request, "index.html", {"message": "Login successful!", "coordinator_name": coordinator_name})
def home(request):
    return render(request, "index.html", {
        "coordinator_name": request.session.get('coordinator_name', None)
    })




def coordinator_view(request):
    # Check if the request is a POST (form submission)
    if request.method == "POST":
        coordinator_name = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Fetch coordinator object matching the provided credentials
            coordinator = Coordinator.objects.get(coordinator_name=coordinator_name, password=password)
            
            # Store essential coordinator info in session for later use
            request.session['coordinator_name'] = coordinator.coordinator_name
            request.session['email'] = coordinator.email
            request.session['coordinator_type'] = coordinator.coordinator_type

            # Redirect based on coordinator type
            if coordinator.coordinator_type == 'department':
                # If it's a department coordinator, redirect to department dashboard
                return redirect('coordinator_dashboard')
            else:
                # Otherwise, assume it's a club coordinator and redirect to club dashboard
                return redirect('coordinator_dashboard')

        except Coordinator.DoesNotExist:
            # If no matching coordinator is found, show an error and reload login page
            messages.error(request, "Invalid login credentials")
            return redirect('coordinator_login')

    # Render the login page initially or if the request isn't a POST
    return render(request, 'coordinator_login.html')


# def coordinator_dash(request):
#     if 'coordinator_name' in request.session:
#         coordinator_name = request.session['coordinator_name']  # ✅ Corrected key
#         email = request.session.get('email', None)  # ✅ Fetch email if exists
#         return render(request, 'coordinator_dashboard.html', {'coordinator_name': coordinator_name, 'email': email })
    
#     return redirect('coordinator_login')  # Redirect to login if session does not exist


# def coordinator_dash_dept(request):
#     if 'coordinator_name' in request.session:
#         coordinator_name = request.session['coordinator_name']  # ✅ Corrected key
#         email = request.session.get('email', None)  # ✅ Fetch email if exists
#         return render(request, 'coordinator_dept_dashboard.html', {'coordinator_name': coordinator_name, 'email': email })
    
#     return redirect('coordinator_login')  # Redirect to login if session does not exist






def coordinator_dashboard(request):
    if 'coordinator_name' in request.session:
        coordinator_name = request.session['coordinator_name']
        email = request.session.get('email', None)

        try:
            coordinator = Coordinator.objects.get(coordinator_name=coordinator_name)
            if coordinator.coordinator_type == 'department':
                return render(request, 'coordinator_dept_dashboard.html', {'coordinator_name': coordinator_name, 'email': email})
            else:
                return render(request, 'coordinator_dashboard.html', {'coordinator_name': coordinator_name, 'email': email})
        except Coordinator.DoesNotExist:
            return redirect('coordinator_login')  # Redirect if the coordinator doesn't exist
    
    return redirect('coordinator_login')  # Redirect if session does not exist