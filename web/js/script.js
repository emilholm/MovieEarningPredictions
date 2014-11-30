$(document).ready(function() {
    var navListItems = $('ul.setup-panel li a');
    var allWells = $('.setup-content');
    var movie_name = "";
    var step_1 = "";
    var step_2 = "";
    var step_3 = "";
    var opts = {
        lines: 17, // The number of lines to draw
        length: 0, // The length of each line
        width: 10, // The line thickness
        radius: 30, // The radius of the inner circle
        corners: 1, // Corner roundness (0..1)
        rotate: 20, // The rotation offset
        direction: 1, // 1: clockwise, -1: counterclockwise
        color: '#000', // #rgb or #rrggbb or array of colors
        speed: 1, // Rounds per second
        trail: 100, // Afterglow percentage
        shadow: false, // Whether to render a shadow
        className: 'spinner', // The CSS class to assign to the spinner
        zIndex: 2e9, // The z-index (defaults to 2000000000)
        top: '50%', // Top position relative to parent
        left: '50%' // Left position relative to parent
    };

    $("#loading").each(function() {
        $(this).append(new Spinner(opts).spin().el);
    });

    // activate item
    $('body').on('click', '.list-group .list-group-item', function () {
        var $listgroup = $(this).closest('.list-group');
        var id = $listgroup.attr('id');
        if(id == 1) {
            step_1 = $(this).attr('id');
        } else if(id == 2) {
            step_2 = $(this).attr('id');
        } else if(id == 3) {
            step_3 = $(this).attr('id');
        }
        $listgroup.find('li.active').removeClass('active');
        $(this).toggleClass('active');
    });

    // search movies
    $('#search-movie-form').submit(function(e) {
        e.preventDefault();
        movie_name = $('#movie-name').val();

        // reset values
        $('#activate-step-2').show();
        $('#activate-step-3').show();
        step_1 = "";
        step_2 = "";
        step_3 = "";
        $("#step-1").find('ul li').remove();
        $("#step-2").find('ul li').remove();
        $("#step-3").find('ul li').remove();
        $("#loading").show();

        // get data and make it look fancy
        $('h2').each(function () {
            $(this).append();
        });
        $('#steps').collapse('show');

        $.ajax({
            type: "POST",
            url: "/searchwiki",
            data: {"movie": movie_name},
            cache: false,
            success: function(data) {
                console.log(data);
                var $step1 = $("#step-1");
                $.each(data, function(key, val){
                    $step1.find(".list-group").append('<li class="list-group-item" id="' + decodeURIComponent(val["url"]) +
                        '"><h4 class="list-group-item-heading">' + key +
                        '</h4><p class="list-group-item-text">' + val["description"] +
                        '</p></li>');
                });
                $step1.find("#loading").hide();
            },
            error: function(data) {
                console.log(data);
            }
        });

        $.ajax({
            type: "POST",
            url: "/searchboxofficemojo",
            data: {"movie": movie_name},
            cache: false,
            success: function (data) {
                console.log(data);
                var $step2 = $("#step-2");
                $.each(data, function(key, val){
                    $step2.find(".list-group").append('<li class="list-group-item" id="' + val +
                        '"><h4 class="list-group-item-heading">' + key + '</h4></li>');
                });
                $step2.find("#loading").hide();
            },
            error: function(data) {
                console.log(data);
            }
        });

        $.ajax({
            type: "POST",
            url: "/searchwiki",
            data: {"movie": movie_name},
            cache: false,
            success: function(data) {
                console.log(data);
                var $step3 = $("#step-3");
                $.each(data, function(key, val){
                    $step3.find(".list-group").append('<li class="list-group-item" id="' + val["url"] +
                        '"><h4 class="list-group-item-heading">' + key +
                        '</h4><p class="list-group-item-text">' + val["description"] +
                        '</p></li>');
                });
                $step3.find("#loading").hide();
            },
            error: function(data) {
                console.log(data);
            }
        });
    });

    allWells.hide();

    navListItems.click(function(e)
    {
        e.preventDefault();
        var $target = $($(this).attr('href'));
        var $item = $(this).closest('li');

        if (!$item.hasClass('disabled')) {
            navListItems.closest('li').removeClass('active');
            $item.addClass('active');
            allWells.hide();
            $target.show();
        }
    });

    $('ul.setup-panel li.active a').trigger('click');

    // next steps
    $('#activate-step-2').on('click', function() {
        if (step_1 == "") {
            swal({
                title: "Did you choose?",
                text: "You have to choose a Wikipedia article, before you can go to the next step!!",
                type: "error",
                showCancelButton: false,
                confirmButtonClass: 'btn-success',
                confirmButtonText: 'Ok!'
            });
        } else {
            $('ul.setup-panel li:eq(1)').removeClass('disabled');
            $('ul.setup-panel li a[href="#step-2"]').trigger('click');
            $(this).hide();
        }
    });

    $('#activate-step-3').on('click', function() {
        if (step_2 == "") {
            swal({
                title: "Did you choose?",
                text: "You have to choose a BoxOfficeMojo page, before you can go to the next step!!",
                type: "error",
                showCancelButton: false,
                confirmButtonClass: 'btn-success',
                confirmButtonText: 'Ok!'
            });
        } else {
            $('ul.setup-panel li:eq(2)').removeClass('disabled');
            $('ul.setup-panel li a[href="#step-3"]').trigger('click');
            $(this).hide();
        }
    });

    $('#generate-data').on('click', function() {
        if (step_3 == "") {
            swal({
                title: "Did you choose?",
                text: "You have to choose a YouTube video, before you can generate data!!",
                type: "error",
                showCancelButton: false,
                confirmButtonClass: 'btn-success',
                confirmButtonText: 'Ok!'
            });
        } else {
           $.ajax({
            type: "POST",
            url: "/getwikipageviews",
            data: {"wikiname": step_1},
            cache: false,
            success: function(data) {
                $('.generation').remove();
                $('#steps').after('<button id="generate-data" class="generation btn btn-primary pull-right">Generate Data</button>').fadeIn();
                $('#steps').after('<button type="button" class="generation btn btn-primary pull-right" data-toggle="collapse" data-target="#steps"><span class="glyphicon glyphicon-cog"></span> Steps</button>').fadeIn();

                console.log(data);
            },
            error: function(data) {
                console.log(data);
            }
        });
        }
    });
});