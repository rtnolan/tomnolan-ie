$(function () {
    $.post('/get-category').done(function (category) {
        $("#category").autocomplete({
            source: category['category']
        });
    })
});