from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_student = True  # default role
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_student:
                login(request, user)
                return redirect('student_dashboard')
            elif user.is_staff:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Your account does not have the correct role.")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'account/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def custom_logout(request):
    logout(request)
    return redirect('login')  # or any page you want after logout

