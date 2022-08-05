from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Group, Post
from http import HTTPStatus
from django.urls import reverse
from django.core.cache import cache

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user')
        cls.user2 = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title="test-group",
            slug='test-slug',
            description="test-descriptipon"
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text="test-group",
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_2 = Client()
        self.authorized_client_2.force_login(self.user2)
        cache.clear()

    def test_public_pages(self):
        """Проверка общедоступных страниц"""
        public_pages = [
            '/',
            f'/group/{self.group.slug}/',
            f'/profile/{self.user.username}/',
            f'/posts/{self.post.id}/'
        ]
        for adress in public_pages:
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_id(self):
        """Страница posts/post_id доступна любому пользователю"""
        response = self.guest_client.get(
            f"/posts/{self.post.id}/"
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            "Страница поста не найдена"
        )

    def test_unexisting_page(self):
        """Несуществующая страница"""
        response = self.guest_client.get('unexisting-page')
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND,
            "Страница не найдена"
        )

    def test_create(self):
        """Страница test_create доступна авторизированному пользователю """
        response = self.authorized_client.get('/create/')
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            "Страница создания поста не найдена"
        )

    def test_posts_post_id_edit(self):
        """Страница post_id_edit достпуна автору поста"""
        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            "Страница posts/post_id/edit не найдена"
        )

    def test_create_post_guest_redirect(self):
        """Редирект гостя при попытке создать пост."""
        response = self.guest_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_edit_post_guest_redirect(self):
        """Редирект гостя при попытке редактировать пост."""
        response = self.guest_client.get(f'/posts/{self.post.id}/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_edit_post_not_author(self):
        """Редактирование поста не автором."""
        edit_post_page = f'/posts/{self.post.id}/edit/'
        response = self.authorized_client_2.get(edit_post_page)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_uses_correct_template(self):
        """Ссылка использует соответствующий HTML-шаблон"""
        template_url_name = {
            '/': 'posts/index.html',
            f'/group/{TaskURLTests.group.slug}/': 'posts/group_list.html',
            f'/profile/{TaskURLTests.user.username}/': 'posts/profile.html',
            f'/posts/{TaskURLTests.post.id}/': 'posts/post_detail.html',
            f'/posts/{TaskURLTests.post.id}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }
        for url, template in template_url_name.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='author')
        cls.post = Post.objects.create(
            author=cls.user,
            text='тестовый текст'
        )

    def test_comment_only_authorized_user(self):
        response = self.guest_client.get('/create/', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_index_page_cache(self):
        """Проверка работы кеша главной страницы"""
        response_1 = self.guest_client.get(reverse('posts:index'))
        resp_1 = response_1.content
        post_to_delete = self.post
        post_to_delete.delete()
        response_2 = self.guest_client.get(reverse('posts:index'))
        resp_2 = response_2.content
        self.assertEqual(resp_1, resp_2)
        cache.clear()
        response_3 = self.guest_client.get(reverse('posts:index'))
        resp_3 = response_3.content
        self.assertNotEqual(resp_3, resp_1)
        self.assertNotEqual(resp_3, resp_2)
