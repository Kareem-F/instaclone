from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile, Photo



class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('about', 'photo')


class PhotoForm(ModelForm):

    class Meta:
        model = Photo
        fields = ['photo', 'tags']



