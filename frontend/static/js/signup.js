var ip = "https://localhost:8000/"
$(function() {
    $('#btnSignUp').click(function() {
 
        $.ajax({
            url: 'D5/signUp',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});