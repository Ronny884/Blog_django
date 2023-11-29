from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *


urlpatterns = [
    path('', Posts.as_view(), name='home'),
    path('add-post/', AddPage.as_view(), name='add_post'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('verification_code/', EnterVerificationCode.as_view(), name='verification_code'),
    path('detail/<slug:post_slug>/', ShowDetail.as_view(), name='detail'),
    path('<int:post_id>/comments/', ShowComments.as_view(), name='comments'),
    path('<int:pk>/<int:post_id>/del-comment/', CommentDeleteView.as_view(), name='del_comment'),
    path('<int:pk>/<int:post_id>/edit-comment/', CommentEditView.as_view(), name='edit_comment'),

    path('del-post/<slug:slug>/', PostDeleteView.as_view(), name='del_post'),
    path('edit-post/<slug:slug>/', PostEditView.as_view(), name='edit_post'),

    path('tag/<slug:tag_slug>/', Posts.as_view(), name='posts_by_tag'),

    path('add-like/', add_like, name='add_like'),
    path('add-dislike/', add_dislike, name='add_dislike'),
    path('add-mark/', add_mark, name='add_mark'),

    path('cats/', cats, name='cats'),
    path('search/', search, name='search'),
    path('profile/', profile, name='profile'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]