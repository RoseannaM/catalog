
$(document).ready(function () {
    $('li.linkbold').on('click', function () {
        $('li.linkbold').removeClass('active'); 
        $(this).addClass('active'); 
    });
});