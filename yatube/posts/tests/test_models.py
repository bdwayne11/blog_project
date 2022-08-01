from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост, '
                 'который необходимо растянуть до 15 символов!',
        )

    def test_models_have_correct_objects_names(self):
        """Проверяем, что у моделей корректно работает __str__"""
        str_names = {
            self.post: self.post.text[:15],
            self.group: self.group.title,
        }
        for type_model, str_el in str_names.items():
            with self.subTest(str_el=str_el):
                self.assertEqual(str(type_model), str_el)
