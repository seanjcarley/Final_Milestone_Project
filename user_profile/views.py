from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm


# Create your views here.
@login_required
def profile(request):
    """ display user profile """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(
                request, 'Update failed. Please enter all required details.'
            )
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    template = 'user_profile/profile.html'

    context = {
        'form': form,
        'orders': orders,
        'profile': profile,
    }

    return render(request, template, context)
