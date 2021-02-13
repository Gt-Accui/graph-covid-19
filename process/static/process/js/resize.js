$(window).on('resize', function () {
    var windowheight = $(window).height() - 150;
    var contentInnerWidth = $('.content').innerWidth();

    $(".content").css({
        "height": windowheight + "px"
    });
    $(".js-plotly-plot").css({
        "width": contentInnerWidth + "px",
        "height": windowheight + "px"
    });
    $(".plotly").css({
        "width": contentInnerWidth + "px",
        "height": windowheight + "px"
    });

    var update = {
        width: contentInnerWidth,
        height: windowheight
    };
    Plotly.relayout(gd, update);
});

$(window).on('load', function () {
    window.dispatchEvent(new Event('resize'));
});
