from .models import *
from django.db.models import Count


def get_count_of_likes(post_id):
    """Общее кол-во лайков под данным постом"""
    count_of_likes = Like.objects.filter(object_id=post_id,
                                         content_type_id=ContentType.objects.get_for_model(Post)).count()
    return count_of_likes


def get_count_of_dislikes(post_id):
    """Общее кол-во дизлайков под данным постом"""
    count_of_dislikes = Dislike.objects.filter(object_id=post_id,
                                               content_type_id=ContentType.objects.get_for_model(Post)).count()
    return count_of_dislikes


def get_count_of_comments(post_id):
    """Общее кол-во комментариев под данным постом"""
    count_of_comments = Comment.objects.filter(post_id=post_id).count()
    return count_of_comments


def is_zero(count):
    """Проверяем, является ли количество нулевым"""
    if count == 0:
        return True
    else:
        return False


def create_posts_ids_list():
    """Общий список айдишников всех постов"""
    posts_ids_list = Post.objects.values_list('id', flat=True)
    return posts_ids_list


def create_dict_of_count(count_target):
    """
    Формируем словарь, где ключ - id поста, а значение -
    количество всех комментариев под данным постом
    либо общее количество лайков/дизлайков под ним
    """
    count_dict = {}
    post_id_list = create_posts_ids_list()

    for post_id in post_id_list:
        if count_target == 'comments':
            count_of_comments = get_count_of_comments(post_id=post_id)
            count_dict[post_id] = '' if is_zero(count_of_comments) else count_of_comments

        elif count_target == 'likes':
            count_of_likes = get_count_of_likes(post_id=post_id)
            count_dict[post_id] = '' if is_zero(count_of_likes) else count_of_likes

        elif count_target == 'dislikes':
            count_of_dislikes = get_count_of_dislikes(post_id=post_id)
            count_dict[post_id] = '' if is_zero(count_of_dislikes) else count_of_dislikes

    return count_dict


def create_list_of_liked_posts(user):
    """Список id постов, которые были лайкнуты данным пользователем"""
    posts_ids_liked_by_user = \
        Like.objects.filter(author=user,
                            content_type=ContentType.objects.get_for_model(Post)).values_list('object_id',
                                                                                              flat=True)
    return posts_ids_liked_by_user


def create_list_of_disliked_posts(user):
    """Список id постов, которые были дизлайкнуты данным пользователем"""
    posts_ids_disliked_by_user = \
        Dislike.objects.filter(author=user,
                               content_type=ContentType.objects.get_for_model(Post)).values_list('object_id',
                                                                                                 flat=True)
    return posts_ids_disliked_by_user


def create_list_of_noted_posts(user):
    """Список id постов, отмеченных данным пользователем"""
    posts_ids_noted_by_user = \
        Mark.objects.filter(author=user,
                            content_type=ContentType.objects.get_for_model(Post)).values_list('object_id',
                                                                                              flat=True)
    return posts_ids_noted_by_user


def check_like_post_by_user(user_id, post_id):
    """Был ли конкретный пост лайкнут конкретным пользователем"""
    result = Like.objects.filter(author_id=user_id,
                                 content_type_id=ContentType.objects.get_for_model(Post),
                                 object_id=post_id).exists()
    return result


def check_dislike_post_by_user(user_id, post_id):
    """Был ли конкретный пост дизлайкнут конкретным пользователем"""
    result = Dislike.objects.filter(author_id=user_id,
                                    content_type_id=ContentType.objects.get_for_model(Post),
                                    object_id=post_id).exists()
    return result


def check_mark_post_by_user(user_id, post_id):
    """Был ли конкретный пост помечен конкретным пользователем"""
    result = Mark.objects.filter(author_id=user_id,
                                 content_type_id=ContentType.objects.get_for_model(Post),
                                 object_id=post_id).exists()
    return result


def get_list_of_similar_posts(post):
    """Список схожих постов"""
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:5]
    return similar_posts
