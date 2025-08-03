from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)  # Log the user out before deleting
        user.delete()
        return redirect('account_deleted')  # Create this template/view or redirect as needed
    return render(request, 'messaging/delete_account_confirm.html')  # Confirmation page
