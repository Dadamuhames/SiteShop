$(document).scroll(function () {
    var scroll = $(window).scrollTop();
    $(".baner-img").css("top", "0" + (scroll / 1.5) + "px");
});  