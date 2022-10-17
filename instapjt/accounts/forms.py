from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    profile_image = forms.ImageField(
        label = "프로필 사진",
        required= False,
    )

class CustomUserChangeForm(UserChangeForm):

    profile_image = forms.ImageField(
        label = "프로필 사진",
        required= False,
    )

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('username', 'profile_image', 'about',)
        # fields = ('email', 'first_name', 'last_name', 'profile_image')

