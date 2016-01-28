$( document ).ready(function() {

    $(".btn-post").click(function (e) {
        /** Updates the 'participating' count. **/
        e.preventDefault();
        e.stopPropagation();

        var event_name = $(this).closest('a').attr('id');
        var url = "/events/" + event_name + "/users/";
        $.ajax({
            type: "POST",
            url: url,
            success: function(data) {
                var members = data['members'];
                if(data['status_code'] == 200){
                    $('#' + event_name + '-join-count').text(members + " Participating!");
                    $(e.target).removeClass('btn-primary').addClass('btn-warning').text('Leave');
                }
            }
        });
    });


    // CSRF code
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

});
