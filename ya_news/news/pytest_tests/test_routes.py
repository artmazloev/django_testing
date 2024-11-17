from http import HTTPStatus

import pytest
from django.test.client import Client
from pytest_lazyfixture import lazy_fixture
from pytest_django.asserts import assertRedirects
# Комментарий ревьюера для редиректов (два урла)
# тоже лучше сразу тут расчитать

OK = HTTPStatus.OK
NOT_FONUD = HTTPStatus.NOT_FOUND

client = Client()
not_author_client = lazy_fixture('not_author_client')
author_client = lazy_fixture('author_client')
URL_DELETE = lazy_fixture('url_delete')
URL_DETAIL = lazy_fixture('url_detail')
URL_EDIT = lazy_fixture('url_edit')
URL_HOME = lazy_fixture('url_home')
URL_LOGIN = lazy_fixture('url_login')
URL_LOGOUT = lazy_fixture('url_logout')
URL_SIGNUP = lazy_fixture('url_signup')


@pytest.mark.parametrize('p_client, url, expected_status', (
                         (client, URL_HOME, OK),
                         (client, URL_LOGIN, OK),
                         (client, URL_LOGOUT, OK),
                         (client, URL_SIGNUP, OK),
                         (not_author_client, URL_DETAIL, OK),
                         (not_author_client, URL_HOME, OK),
                         (not_author_client, URL_EDIT, NOT_FONUD),
                         (not_author_client, URL_DELETE, NOT_FONUD),
                         (author_client, URL_EDIT, OK),
                         (author_client, URL_DELETE, OK)))
def test_home_availability_for_anonymous_user(p_client, url, expected_status):
    """Анонимному пользователю доступна главная страница."""
    response = p_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (URL_EDIT, URL_DELETE),
)
def test_redirects(client, url, url_login):
    """Тесты редиректов."""
    expected_url = f'{url_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
