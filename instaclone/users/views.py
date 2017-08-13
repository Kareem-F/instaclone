from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Profile, Photo
from .forms import UserForm, ProfileForm, PhotoForm


@login_required
def profile(request, username):
    editable = False
    user_info = Profile.objects.get(user__username=username)
    if request.user == user_info.user:
        editable = True
    try:
        user_photos = Photo.objects.filter(user=user_info.user)
    except Photo.DoesNotExist:
        user_photos = None

    context = {'user_info': user_info, 'user_photos': user_photos, 'editable': editable}
    return render(request, 'users/profile.html', context=context)


@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form_object = form.save(commit=False)
            form_object.user = request.user
            form.save()
            return redirect('users:profile', request.user.username)
    form = PhotoForm()
    context = {'form': form}
    return render(request, 'users/upload_photo.html', context=context)


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('users:profile', username= request.user.username)
        else:
            messages.error(request, 'Please correct the error below')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'users/update_profile.html', context=context)


@login_required
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query', None)
        if query is not None:
            query = query.strip().lower()
            query_user = get_object_or_404(User, username=query)
            return redirect('users:profile', username=query_user.username)
        else:
            return redirect('users:profile', username=request.user.username)
