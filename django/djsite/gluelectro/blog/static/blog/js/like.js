
function addMark(id) {
    var csrfToken = getCookie('csrftoken'); // Получение CSRF-токена из куки
    var alreadyNoted

    if (document.getElementById('mark-button-' + id).classList.value == 'like-button-pushed')
       alreadyNoted = true
    else
       alreadyNoted = false

    $.ajax({
        url: "/add-mark/", // URL для вызова функции-представления
        type: "POST",
        dataType: "json",
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'id': id,
            'post_id': id,
            'already_noted': alreadyNoted
        },
        success: function(response) {
            const btnMark = document.getElementById('mark-button-' + id)
            btnMark.classList.value = response.newClass
        }
    });
}

function addLike(id) {
    var csrfToken = getCookie('csrftoken'); // Получение CSRF-токена из куки
    var likedByUser

    if (document.getElementById('like-button-' + id).classList.value == 'like-button-pushed')
       likedByUser = true
    else
       likedByUser = false

    $.ajax({
        url: "/add-like/", // URL для вызова функции-представления
        type: "POST",
        dataType: "json",
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'id': id,
            'post_id': id,
            'liked_by_user': likedByUser
        },
        success: function(response) {
            const btnLike = document.getElementById('like-button-' + id)
            const btnDislike = document.getElementById('dislike-button-' + id)
            const countLike = document.getElementById('like-count-' + id)
            const countDislike = document.getElementById('dislike-count-' + id)

            btnLike.classList.value = response.newClass
            if (btnDislike.classList.value == 'like-button-pushed')
                btnDislike.classList.value = 'like-button-not-pushed'

            countLike.innerHTML = response.likes
            countDislike.innerHTML = response.dislikes
        }
    });
}

function addDislike(id) {
    var csrfToken = getCookie('csrftoken'); // Получение CSRF-токена из куки
    var dislikedByUser

    if (document.getElementById('dislike-button-' + id).classList.value == 'like-button-pushed')
       dislikedByUser = true
    else
       dislikedByUser = false

    $.ajax({
        url: "/add-dislike/", // URL для вызова функции-представления
        type: "POST",
        dataType: "json",
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'id': id,
            'post_id': id,
            'disliked_by_user': dislikedByUser
        },
        success: function(response) {
            const btnDislike = document.getElementById('dislike-button-' + id)
            const btnLike = document.getElementById('like-button-' + id)
            const countLike = document.getElementById('like-count-' + id)
            const countDislike = document.getElementById('dislike-count-' + id)

            btnDislike.classList.value = response.newClass

            if (btnLike.classList.value == 'like-button-pushed')
                btnLike.classList.value = 'like-button-not-pushed'

            countLike.innerHTML = response.likes
            countDislike.innerHTML = response.dislikes
        }
    });
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
