function content_reload() {
    $('#info').hide();
    $('#warn').show();
    setInterval(location.reload(), 150000);
}

$(document).ready(function() {
    $('#info').show();
    $('#warn').hide();
    setInterval('content_reload()', 300000);
});
