$(window).on('resize', function () {
    let windowheight = $(window).height() - 150;
    let contentInnerWidth = $('.content').innerWidth();

    if (windowheight < 400) {
        windowheight = 400;
    }

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
