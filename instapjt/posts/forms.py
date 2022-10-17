from logging import PlaceHolder
from django import forms
from django import forms
from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ("content", "image")

class CommentForm(forms.ModelForm):
    class Meta():
        model = Comment
        exclude = ("post", "author")
    
    content = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                "class" : "d-inline",
                "placeholder" : "댓글을 입력해주세요.",
            },
        )
    )