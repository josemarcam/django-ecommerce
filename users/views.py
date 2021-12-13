from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from users.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

app_name = "users"

login_view = LoginView.as_view(template_name="login.html")
logout_view = LogoutView.as_view(next_page="user:login")

def homepage(request):
	return render(request=request, template_name='home.html')

@login_required
@permission_required('users.add_user',"users:homepage")
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid() and request.user.has_perm('users.add_user'):
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("users:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form":form})