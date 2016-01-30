$( document ).ready(function() {
    btn_post_handler();

    /** prevent page from going to next page if clicked on an element inside 'a' tag. **/
    $(".sp").click(function (e){
        e.preventDefault();
        e.stopPropagation();
    });

    /** Initialize Bootstrop popover **/
    $(function () {
        $('[data-toggle="popover"]').popover()
    });

    csrf_setup();

});

function csrf_setup() {
    /** Django required setup for csrf validation  **/
    function getCookie(name) {
        var cookieValue = null;
        var i = 0;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function btn_post_handler() {
    /** Handles click event on Join/Leave event button in upcoming events list. **/
    $(".btn-post").click(function (e) {
        /** Updates the 'participating' count. **/
        e.preventDefault();
        e.stopPropagation();

        var event_name = $(this).closest('a').attr('id');
        var url = "/events/" + event_name + "/users/";
        var p_join_count = $('#' + event_name + '-join-count');
        var username = $('#username').text();

        if ($(this).text() == "Join") {
            $.ajax({
                type: "POST",
                url: url,
                success: function (data) {
                    var members = data['members'];
                    if (data['status_code'] == 200) {
                        $('#' + event_name + '-join-count').text(members + " Participating!");
                        p_join_count.attr('data-content', p_join_count.attr('data-content') + '\n' + username)
                        $(e.target).removeClass('btn-primary').addClass('btn-warning').text('Leave');
                    } else {
                        alert('something went wrong!');
                    }

                }
            });
        }
        else {
            $.ajax({
                type: "DELETE",
                url: url,
                success: function (data) {
                    var members = data['members'];
                    if (data['status_code'] == 200) {
                        p_join_count.text(members + " Participating!");
                        if (members > 0) {
                            p_join_count.attr('data-content', p_join_count.attr('data-content').replace(username, ''));
                        }
                        else {
                            p_join_count.attr('data-content', 'Nobody has joined yet!')
                        }
                        $(e.target).removeClass('btn-warning').addClass('btn-primary').text('Join');
                    }
                }
            });
        }
    });
}

