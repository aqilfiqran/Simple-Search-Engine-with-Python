$(document).ready(() => {
    $("#search").on('click', () => {
        let query = $(".text").val()
        let top = $(".number").val()

        let search = "http://localhost/simple-search-engine-with-python/core/php/query.php?t=" + top + "&s=" + query;
        $.ajax({
            url: search,
            success: function (result) {
                JSON.parse(result).forEach(el => {
                    $("#result").append(makeResult(el));
                });

            },
            error: function (err) {
                console.log('err :', err);
            }
        });
    });

    makeResult = data => {
        card = '<div class="content">';
        card += '<div>';
        card += '<h3>' + data.title + '</h3>';
        card += '<p>' + data.content + '</p>';
        card += '<a href="' + data.url + '">Read More</a>';
        card += '</div></div>';
        return card;
    }

})