$( document ).ready(function() {
    var last_chal_id;

    var formAjaxSubmit = function(form, modal) {
        $(form).submit(function (e) {
            e.preventDefault();
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function (xhr, ajaxOptions, thrownError) {
                    if ( $(xhr).find('.has-error').length > 0 ) {
                        $(modal).find('.modal-body').html(xhr);
                        formAjaxSubmit(form, modal);
                    } else {
                        var btn = $('#' + last_chal_id);
                        if(btn.parent().parent().hasClass('panel')) {
                            btn.parent().parent().removeClass('panel-danger panel-warning').addClass('panel-success');
                        } else {
                            btn.closest('td').removeClass('bg-danger bg-warning').addClass('bg-success');
                        }
                    }
                },
                error: function (xhr, ajaxOptions, thrownError) {
                }
            });
        });
    };

    $('.btn-solve').click(function (e) {
        last_chal_id = $(this).attr('id');
        var url = '/events/solve-form/' + last_chal_id
        $('#form-modal-body').load(url, function (){
            $('#form-modal').modal('toggle');
            formAjaxSubmit('#form-modal-body form', '#form-modal');
        });
    });

    $('#btn_modal_submit').click(function (e) {
        $('#form-modal-body').find('form').submit();
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