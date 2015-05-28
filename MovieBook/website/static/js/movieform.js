$(document).ready(function(){
    function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        var csrftoken = getCookie('csrftoken');


        function getmovie (movieID){

            $.ajax({
                type:"POST",
                url:"/movies".format(movieID),
                data: {"movie":movieID},
                success: function(result) {
                    $("#movie-" + movieID).hide();
                    console.log("Suausuasasajajsassak")
                },headers: {
                    'X-CSRFToken': csrftoken
                }
            })
            return false;
        }
    $(function() {
        $("#movie").click(function(){
            alert("Успешно добавен в любими!")
        })
    });
});

