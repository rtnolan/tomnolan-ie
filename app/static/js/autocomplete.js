$(function() {
    $('button').click(function() {
        $.ajax({
            url: '/add-category',
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