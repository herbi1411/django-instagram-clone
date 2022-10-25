from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.forms import TextInput

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ( 'profile_image', 'about', 'username')

    profile_image = forms.ImageField(
        label = "프로필 사진",
        required= False,
    )
    about = forms.CharField(
        label = "About",
        widget= forms.Textarea(
            attrs= {
                'placeholder' : '본인을 소개해주세요.',
                'row' :  3,
                'col' : 30,
            }
        )
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

