from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image',)
        labels = {
            'group': 'Выберите группу',
            'text': 'Введите текст'
        }
        help_texts = {
            'group': 'Группа поста',
            'text': 'Текст записи'
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Введите текст'
        }
        help_texts = {
            'text': 'Текст комментария'
        }
