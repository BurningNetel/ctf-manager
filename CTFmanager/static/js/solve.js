$( document ).ready(function() {
    var last_chal_id;
    $('.btn-solve').click(function (e) {
        last_chal_id = $(this).closest('tr').attr('id');
    });

    $('#btn_solve').click(function (e) {
        e.preventDefault();
        var url = window.location.pathname + '/challenges/' + last_chal_id + '/users/';
        var flag = $('#id_flag').val();
        $.ajax({
            type: "POST",
            url: url,
            data: {'flag': flag},
            success: function (data) {
                if(data['status_code'] == 200) {
                    $('#' + last_chal_id).find('td').removeClass('bg-danger bg-warning').addClass('bg-success');
                }
                else {
                    alert('something went wrong!');
                }
            }
        });
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