from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from .fixtures import BaseTestNote

User = get_user_model()


class TestRoutes(BaseTestNote):
    """Тесты путей."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.URL_LOGIN = reverse('users:login')
        cls.URL_LOGOUT = reverse('users:logout')
        cls.URL_SIGNUP = reverse('users:signup')
        cls.URL_HOME = reverse('notes:home')
        cls.URL_LIST = reverse('notes:list')
        cls.URL_ADD = reverse('notes:add')
        cls.URL_SUCCESS = reverse('notes:success')
        cls.URL_DETAIL = reverse('notes:detail', args=(cls.note.slug,))
        cls.URL_EDIT = reverse('notes:edit', args=(cls.note.slug,))
        cls.URL_DELETE = reverse('notes:delete', args=(cls.note.slug,))
        

    def test_pages_availability_for_anonymous_user(self):
        params = (
            (self.URL_HOME, self.client, HTTPStatus.OK),
            (self.URL_LOGIN, self.client, HTTPStatus.OK),
            (self.URL_LOGOUT, self.client, HTTPStatus.OK),
            (self.URL_SIGNUP, self.client, HTTPStatus.OK),
            (self.URL_LIST, self.reader_client, HTTPStatus.OK),
            (self.URL_ADD, self.reader_client, HTTPStatus.OK),
            (self.URL_SUCCESS, self.reader_client, HTTPStatus.OK),
            (self.URL_DETAIL, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.URL_EDIT, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.URL_DELETE, self.reader_client, HTTPStatus.NOT_FOUND),
            (self.URL_DETAIL, self.author_client, HTTPStatus.OK),
            (self.URL_EDIT, self.author_client, HTTPStatus.OK),
            (self.URL_DELETE, self.author_client, HTTPStatus.OK))
        for param in params:
            with self.subTest(name=param):
                response = param[1].get(param[0])
                self.assertEqual(response.status_code, param[2])

    def test_redirects(self):
        """Тесты редиректов"""
        urls = (
            self.URL_LIST,
            self.URL_ADD,
            self.URL_SUCCESS,
            self.URL_EDIT,
            self.URL_DELETE
        )
        for url in urls:
            with self.subTest(name=url):
                redirect_url = f'{self.URL_LOGIN}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
