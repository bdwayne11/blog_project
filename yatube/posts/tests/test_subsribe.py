from posts.models import Post, Group, Follow
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus


User = get_user_model()


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username="Author")
        cls.follower = User.objects.create_user(username="Follower")

        cls.group = Group.objects.create(
            title="Тестовый тайтл",
            slug="test-slug",
            description="Тестовое описание",
        )

        cls.post_followed = Post.objects.create(
            author=cls.author,
            text="Тестовый текст",
            pub_date=timezone.now(),
            group=cls.group,
        )

        cls.post_unfollowed = Post.objects.create(
            author=cls.follower,
            text="Тестовый текст для отписки",
            pub_date=timezone.now(),
            group=cls.group,
        )

        cls.follow = Follow.objects.create(
            user=cls.follower,
            author=cls.author
        )

        cls.guest_client = Client()
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.follower_client = Client()
        cls.follower_client.force_login(cls.follower)
  
    def test_authorized_user_can_subscribe(self):
        """Проверка авторизированного пользователя на подписку"""
        response = self.author_client.get(
            reverse(
                "posts:profile_follow",
                kwargs={"username": self.follower.get_username()},
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_new_post_in_followers_feed(self):
        """Подписчики видят посты авторов"""
        response = self.follower_client.get(reverse("posts:follow_index"))
        post = response.context.get("page_obj")[0]
        self.assertEqual(post.text, "Тестовый текст")

    def test_none_followers_dont_see_posts(self):
        """Не подписчики не видят посты других авторов"""
        response = self.author_client.get(reverse("posts:follow_index"))
        count = len(response.context.get("page_obj"))
        self.assertEqual(0, count)
    
    def test_authorized_user_can_follow(self):
        """Авторизированный может подписаться"""
        if Follow.objects.filter(
            user=self.author, author=self.follower
        ).exists():
            Follow.objects.filter(
                user=self.author, author=self.follower
            ).delete()
        self.author_client.get(
            reverse(
                "posts:profile_follow",
                kwargs={"username": self.follower.username},
            )
        )
        if Follow.objects.filter(
            user=self.author, author=self.follower
        ).exists():
            subscribe = True
        self.assertTrue(subscribe)

    def test_authorized_user_can_unfollow(self):
        """Авторизированный может отписаться"""
        if not Follow.objects.filter(
            user=self.author, author=self.follower
        ).exists():
            Follow.objects.create(user=self.author, author=self.follower)
        self.author_client.get(
            reverse(
                "posts:profile_unfollow",
                kwargs={"username": self.follower.username},
            )
        )
        if not Follow.objects.filter(
            user=self.author, author=self.follower
        ).exists():
            follow = True
        self.assertTrue(follow)
