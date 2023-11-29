from django import template
from blog.models import *

register = template.Library()


@register.simple_tag
def show_menu(is_auth=True):
    if is_auth:
        common_actions = [
            {'title': 'Подписки', 'url_name': 'subscriptions'},
            {'title': 'Интересное', 'url_name': 'home'},
            {'title': 'Категории', 'url_name': 'cats'},
            {'title': 'Поиск', 'url_name': 'search'},
        ]
        user_actions = [
            {'title': 'Выйти', 'url_name': 'logout'},
            {'title': 'Мой профиль', 'url_name': 'profile'},
            {'title': 'Написать', 'url_name': 'add_post'}
        ]
    else:
        common_actions = [
            {'title': 'Интересное', 'url_name': 'home'},
            {'title': 'Категории', 'url_name': 'cats'},
            {'title': 'Поиск', 'url_name': 'search'},
        ]
        user_actions = [
            {'title': 'Войти', 'url_name': 'login'},
            {'title': 'Регистрация', 'url_name': 'register'},
        ]
    return {'common_actions': common_actions, 'user_actions': user_actions}
