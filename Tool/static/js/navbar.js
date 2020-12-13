$(".toggleNav").click(() => {
    $(".toggleNav").toggleClass("close");
    $(".navbar-responsive").toggleClass("open");
    $(".navbar-responsive__link").toggleClass("open__link");
})