
SUCCESS_CLASS = 'btn-success solid_border'
FAIL_CLASS = 'btn-danger solid_border'
INFO_CLASS = 'btn-info solid_border'
WARN_CLASS = 'btn-warning solid_border'

function page_alert(message, style_class, fadeOutTime = -1) {
    $("#feedback_message").html(message);
    $("#feedback_message").removeClass();
    $("#feedback_message").addClass('btn');
    $("#feedback_message").addClass(style_class);
    $("#feedback_box").fadeIn('slow');

    if (fadeOutTime > 0) {
        $("#feedback_box").delay(fadeOutTime * 1000).fadeOut();
    }
}


function not_implemented() {
    page_alert('not implemented yet', INFO_CLASS, fadeOutTime = 2);
}


