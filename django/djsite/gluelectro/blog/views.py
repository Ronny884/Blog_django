from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger
from taggit.models import Tag
import random
from .forms import *
from .models import *
from .utils import *


class Posts(ListView):
    """
    Класс для предоставления всех постов подряд
    либо по выбранному тегу
    """
    paginate_by = 10
    template_name = 'blog/posts.html'
    tag_slug = None

    def get_queryset(self):
        self.tag_slug = self.kwargs.get('tag_slug')

        if self.tag_slug is not None:
            tag = get_object_or_404(Tag, slug=self.tag_slug)
            queryset = Post.published.filter(tags__in=[tag])
        else:
            queryset = Post.published.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все посты'
        context['comments'] = create_dict_of_count('comments')
        context['likes'] = create_dict_of_count('likes')
        context['dislikes'] = create_dict_of_count('dislikes')
        context['posts_liked_by_user'] = create_list_of_liked_posts(user=self.request.user.id)
        context['posts_disliked_by_user'] = create_list_of_disliked_posts(user=self.request.user.id)
        context['posts_noted_by_user'] = create_list_of_noted_posts(user=self.request.user.id)
        return context


class LoginUser(LoginView):
    """
    Класс авторизации пользователя. Для того, чтобы пользователь мог писать посты,
    оставлять комментарии, ставить лайки и метки, он должен быть зарегистрирован и авторизован
    """
    form_class = LoginUserForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    """
    Класс регистрации пользователя. При вводе им уникального ника,
    email и надёжного пароля, ему на почту приходит сообщение с кодом верификации,
    который необходимо ввести в следующем окне. Сохранение пользователя в БД
    происходит уже на этом этапе, однако он будет не активен, пока не введёт
    код верификации
    """
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        right_code = str(random.randrange(10000, 99999, 1))
        cd = form.cleaned_data
        subject = f'Код подтверждения'
        send_mail(subject, f'Ваш код: {right_code}', 'nikita.sivko77@gmail.com', [cd['email']])
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.request.session['right_code'] = right_code
        self.request.session['user_id'] = user.pk
        return redirect('verification_code')


class EnterVerificationCode(CreateView):
    """
    Класс ввода кода верификации. Введённый пользователем код (просмотренный на его почте)
    сравнивается с переданным в сессию правильным кодом. В случае совпадения пользователь становится
    активным и авторизованным, после чего перенаправляется на главную страницу. В противном случае
    рендерится эта же страница, но уже с сообщением о неверном вводе
    """
    form_class = VerificationCodeForm
    model = User
    template_name = 'blog/verification_code.html'
    success_url = reverse_lazy('login')
    reg_cls = RegisterUser()

    def form_valid(self, form):
        input_code = self.request.POST.get('verification_code')
        right_code = self.request.session.get('right_code')
        user_id = self.request.session.get('user_id')

        if input_code == right_code:
            user = User.objects.get(pk=user_id)
            user.is_active = True
            user.save()
            login(self.request, user)
            return redirect('home')
        else:
            context = {'form': form,
                       'error': 'Неверный код'}
            return render(self.request, 'blog/verification_code.html', context=context)


class ShowDetail(DetailView):
    """
    Класс детальной информации о посте. Помимо основных вещей (полный текст, лайки,
    дизлайки, комментарии, метки, теги) внизу предоставляется список схожих постов,
    что имеют общие теги и потенциально могут заинтересовать читателя
    """
    model = Post
    template_name = 'blog/detail.html'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        likes_count = get_count_of_likes(post_id=post.id)
        dislikes_count = get_count_of_dislikes(post_id=post.id)
        comments_count = get_count_of_comments(post_id=post.id)

        context['post'] = post
        context['title'] = post.title
        context['liked'] = check_like_post_by_user(user_id=self.request.user.id, post_id=post.id)
        context['disliked'] = check_dislike_post_by_user(user_id=self.request.user.id, post_id=post.id)
        context['noted'] = check_mark_post_by_user(user_id=self.request.user.id, post_id=post.id)
        context['likes'] = '' if is_zero(likes_count) else likes_count
        context['dislikes'] = '' if is_zero(dislikes_count) else dislikes_count
        context['comments'] = '' if is_zero(comments_count) else comments_count
        context['similar_posts'] = get_list_of_similar_posts(post)
        return context


class AddPage(LoginRequiredMixin, CreateView):
    """
    Класс окна добавления нового поста авторизованным пользователем
    """
    form_class = AddPostForm
    template_name = 'blog/addpost.html'
    login_url = '/admin/'

    def form_valid(self, form):
        user = self.request.user
        form.instance.author = user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новая статья'
        return context

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    """ Выход пользователя из аккаунта """
    logout(request)
    return redirect('home')


class ShowComments(ListView):
    """
    Класс окна со списком всех комментариев к выбранному посту. Так же реализована
    форма написания собственного комментария, если пользователь авторизован
    """
    form_class = CommentForm
    template_name = 'blog\comments.html'

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Comment.objects.filter(post_id=post_id).order_by('-created')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все комментарии'
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = self.kwargs['post_id']
            comment.author_id = self.request.user.id
            comment.save()
            return redirect('comments', post_id=self.kwargs['post_id'])
        else:
            return self.get(request, *args, **kwargs)


class CommentDeleteView(DeleteView):
    """
    Класс окна удаления своего комментария
    авторизованным пользователем
    """
    model = Comment
    template_name = 'blog\comment_delete.html'

    def get_success_url(self):
        return reverse_lazy('comments', kwargs={'post_id': self.kwargs['post_id']})


class CommentEditView(UpdateView):
    """
    Класс окна редактирования своего комментария
    авторизованным пользователем
    """
    model = Comment
    template_name = 'blog\comment_edit.html'
    fields = ['body']

    def get_success_url(self):
        return reverse_lazy('comments', kwargs={'post_id': self.kwargs['post_id']})


class PostDeleteView(DeleteView):
    """
    Класс окна удаления своего поста
    авторизованным пользователем
    """
    model = Post
    template_name = 'blog/post_delete.html'

    def get_success_url(self):
        return reverse_lazy('home')


class PostEditView(UpdateView):
    """
    Класс окна редактирования своего поста
    авторизованным пользователем
    """
    model = Post
    template_name = 'blog/post_edit.html'
    fields = ['title', 'body', 'tags']

    def get_success_url(self):
        return reverse_lazy('home')


def add_like(request):
    """
    Функция-представление постановки (удаления) лайка авторизованным пользователем. Вызывается
    из JavaScript-кода посредством ajax, что убирает необходимость перезагрузки всей страницы
    после постановки (удаления) лайка. Функция-представление производит необходимые действия в БД,
    после чего отправляет JSON с обновлёнными данными в ajax-фунцию JavaScript
    """
    object_id = request.POST.get('post_id')
    liked_by_user = request.POST.get('liked_by_user')
    content_type = ContentType.objects.get_for_model(Post)

    if liked_by_user == 'true':
        Like.objects.filter(author=request.user.id, content_type=content_type, object_id=object_id).delete()
        new_class = 'like-button-not-pushed'

    else:
        like = Like(author=request.user, content_type=content_type, object_id=object_id)
        like.save()
        Dislike.objects.filter(author=request.user.id, content_type=content_type, object_id=object_id).delete()
        new_class = 'like-button-pushed'

    new_count_of_likes = get_count_of_likes(post_id=object_id)
    new_count_of_dislikes = get_count_of_dislikes(post_id=object_id)
    data = {
        'likes': '' if is_zero(new_count_of_likes) else new_count_of_likes,
        'dislikes': '' if is_zero(new_count_of_dislikes) else new_count_of_dislikes,
        'newClass': new_class
    }
    return JsonResponse(data)


def add_dislike(request):
    """
    Функция-представление постановки (удаления) дизлайка авторизованным пользователем
    """
    object_id = request.POST.get('post_id')
    disliked_by_user = request.POST.get('disliked_by_user')
    content_type = ContentType.objects.get_for_model(Post)

    if disliked_by_user == 'true':
        Dislike.objects.filter(author=request.user.id, content_type=content_type, object_id=object_id).delete()
        new_class = 'like-button-not-pushed'

    else:
        dislike = Dislike(author=request.user, content_type=content_type, object_id=object_id)
        dislike.save()
        Like.objects.filter(author=request.user.id, content_type=content_type, object_id=object_id).delete()
        new_class = 'like-button-pushed'

    new_count_of_likes = get_count_of_likes(post_id=object_id)
    new_count_of_dislikes = get_count_of_dislikes(post_id=object_id)
    data = {
        'likes': '' if is_zero(new_count_of_likes) else new_count_of_likes,
        'dislikes': '' if is_zero(new_count_of_dislikes) else new_count_of_dislikes,
        'newClass': new_class
    }
    return JsonResponse(data)


def add_mark(request):
    """
    Функция-представление постановки (удаления) заметки авторизованным пользователем
    """
    object_id = request.POST.get('post_id')
    already_noted = request.POST.get('already_noted')
    content_type = ContentType.objects.get_for_model(Post)

    if already_noted == 'true':
        Mark.objects.filter(author=request.user.id, content_type=content_type, object_id=object_id).delete()
        new_class = 'like-button-not-pushed'

    else:
        mark = Mark(author=request.user, content_type=content_type, object_id=object_id)
        mark.save()
        new_class = 'like-button-pushed'

    data = {
        'newClass': new_class
    }
    return JsonResponse(data)


def popular(request):
    pass


def cats(request):
    pass


def profile(request):
    pass


def subscriptions(request):
    pass


def search(request):
    pass






