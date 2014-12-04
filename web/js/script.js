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
    $('body').on('click', '.list-group .list-group-item', function() {
        var $listgroup = $(this).closest('.list-group');
        var id = $listgroup.attr('id');
        if (id == 1) {
            step_1 = $(this).attr('id');
        } else if (id == 2) {
            step_2 = $(this).attr('id');
            console.log(step_2);
        } else if (id == 3) {
            step_3 = $(this).attr('id');
            console.log(step_3);
        }
        $listgroup.find('li.active').removeClass('active');
        $(this).toggleClass('active');
    });

    //Wiki specific search
    $('#wikisearchsubmit').click(function() {
        step_1 = "";
        $("#step-1").find('ul li').remove();

        var internalWiki = $('#wikisearch').val();
        $('.step_1_loading').show();

        $.ajax({
            type: "POST",
            url: "/searchwiki",
            data: {"movie": internalWiki},
            cache: false,
            success: function(data) {
                var $step1 = $("#step-1");
                $.each(data, function(key, val) {
                    $step1.find(".list-group").append('<li class="list-group-item" id="' + decodeURIComponent(val["url"]) +
                            '"><h4 class="list-group-item-heading">' + key +
                            '</h4><p class="list-group-item-text">' + val["description"] +
                            '</p></li>');
                });
                $('.step_1_loading').hide();
            },
            error: function(data) {
                console.log(data);
                $('.step_1_loading').hide();
            }
        });
    });

    // search movies
    $('#search-movie-form').submit(function(e) {
        e.preventDefault();
        var $step1 = $("#step-1");
        var $step2 = $("#step-2");
        var $step3 = $("#step-3");

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
        $('h2').each(function() {
            $(this).append();
        });
        $('#steps').collapse('show');

        $('#wikisearch').val(movie_name);

        $.ajax({
            type: "POST",
            url: "/searchwiki",
            data: {"movie": movie_name},
            cache: false,
            success: function(data) {
                $.each(data, function(key, val) {
                    $step1.find(".list-group").append('<li class="list-group-item" id="' + decodeURIComponent(val["url"]) +
                            '"><h4 class="list-group-item-heading">' + key +
                            '</h4><p class="list-group-item-text">' + val["description"] +
                            '</p></li>');
                });
                $step1.find("#loading").hide();
            },
            error: function(data) {
                console.log(data);
                $step1.find("#loading").hide();
            }
        });

        $.ajax({
            type: "POST",
            url: "/searchboxofficemojo",
            data: {"movie": movie_name},
            cache: false,
            success: function(data) {
                $.each(data, function(key, val) {
                    $step2.find(".list-group").append('<li class="list-group-item" id="' + val +
                            '"><h4 class="list-group-item-heading">' + key + '</h4></li>');
                });
                $step2.find("#loading").hide();
            },
            error: function(data) {
                $step2.find("#loading").hide();
                console.log(data);
            }
        });

        $.ajax({
            type: "POST",
            url: "/searchyoutubetrailer",
            data: {"movie": movie_name + " trailer"},
            cache: false,
            success: function(data) {
                $.each(data, function(key, val) {
                    $step3.find(".list-group").append('<li class="list-group-item" id="' + val +
                            '"><h4 class="list-group-item-heading">' + key +'</h4></li>');
                });
                $step3.find("#loading").hide();
            },
            error: function(data) {
                $step3.find("#loading").hide();
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
            var $steps = $('#steps');
            $('.generation').remove();
            $steps.collapse('hide');
            $steps.after('<div style="padding: 0;" class="generation col-xs-12 hide_show_steps"><button type="button" class="generation btn btn-primary pull-right" data-toggle="collapse" data-target="#steps"><span class="glyphicon glyphicon-cog"></span> Steps</button></div>').fadeIn();
            $steps.css('display', '');
            $('.hide_show_steps').after('<div id="graph-earnings" class="generation col-xs-12"><h2>BoxOfficeMojo Earnings <small>First 7 days</small></h2></div>');
            $('#graph-earnings').append('<div class="generation" id="chart_earnings"><svg></svg></div>');
            var $earningsgraph = $("#chart_earnings").hide();
            $('#graph-earnings').append('<div id="loading" class="col-xs-12 page_earnings" style="margin-top:50px; margin-bottom: 50px"></div>');
            $('.hide_show_steps').after('<div id="graph-pageviews" class="generation col-xs-12"><h2>Wiki Page Views</h2></div>');
            $('#graph-pageviews').append('<div class="generation" id="chart_page_views"><svg></svg></div>');
            var $pageviewsgraph = $("#chart_page_views").hide();
            $('#graph-pageviews').append('<div id="loading" class="col-xs-12 page_views_loading" style="margin-top:50px; margin-bottom: 50px"></div>');
            $('.hide_show_steps').after('<div id="analysis" class="generation col-xs-12"><h2>YouTube Comments</h2></div>');
            $('#analysis').append('<div id="loading" class="col-xs-12 youtube_comments" style="margin-top:50px; margin-bottom: 50px"></div>');
            var $pageViewsLoading = $('.page_views_loading');
            var $earningsLoading = $('.page_earnings');
            var $analysis = $('.youtube_comments');
            $pageViewsLoading.append(new Spinner(opts).spin().el);
            $earningsLoading.append(new Spinner(opts).spin().el);
            $analysis.append(new Spinner(opts).spin().el);

            $.ajax({
                type: "POST",
                url: "/getwikipageviews",
                data: {"wikiname": step_1, "boxofficemojoname": step_2},
                cache: false,
                success: function(data) {
                    var sorted_data = [];
                    $.each(data, function(key, value) {
                        var date = Date.parse(key.substring(0, 10));
                        sorted_data.push([date, value]);
                    });

                    sorted_data.sort(function(x, y) {
                        return x[0] - y[0];
                    })

                    var data_set = [
                        {
                            "key": "Page views",
                            "values": sorted_data
                        }
                    ];

                    nv.addGraph(function() {
                        var chart = nv.models.lineWithFocusChart()
                                .x(function(d) {
                            return d[0]
                        })
                                .y(function(d) {
                            return d[1]
                        })
                                .color(d3.scale.category10().range());

                        //nv.models.lineWithFocusChart();

                        chart.xAxis
                                .tickFormat(function(d) {
                            return d3.time.format('%x')(new Date(d));
                        });

                        chart.x2Axis
                                .tickFormat(function(d) {
                            return d3.time.format('%x')(new Date(d));
                        });

                        chart.yAxis.tickFormat(d3.format('10'));

                        chart.y2Axis.tickFormat(d3.format('10'));

                        d3.select('#chart_page_views svg')
                                .datum(data_set)
                                .transition().duration(500)
                                .call(chart);

                        nv.utils.windowResize(chart.update);

                        return chart;
                    });
                    $pageviewsgraph.fadeIn();
                    $pageViewsLoading.remove();

                },
                error: function(data) {
                    console.log(data);
                    $pageViewsLoading.remove();
                }
            });

            $.ajax({
                type: "POST",
                url: "/getfirstsevendaysearnings",
                data: {"boxofficemojoname": step_2},
                cache: false,
                success: function(data) {
                    var final_data = [];
                    console.log(data);
                    if(!('error' in data)) {
                        $.each(data, function(index, value) {
                            final_data.push({"label": "Day "+ (index+1), "value": value});
                        });

                        var data_set = [
                            {
                                "key": "Earnings",
                                "values": final_data
                            }
                        ];

                        nv.addGraph(function() {
                            var chart = nv.models.discreteBarChart()
                                .x(function(d) {return d.label})
                                .y(function(d) {return d.value})
                                .staggerLabels(true)
                                .tooltips(false)
                                .showValues(true);

                            d3.select('#chart_earnings svg')
                                    .datum(data_set)
                                    .transition().duration(500)
                                    .call(chart);

                            nv.utils.windowResize(chart.update);

                            return chart;
                        });
                    } else {
                        $('#chart_earnings').find('svg').remove();
                        $('#chart_earnings').append('<h3>Either the movies does not exists on BoxOfficeMojo.com, haven\'t had premiere yet. So there is no information about earnings</h3>');
                    }
                    $earningsgraph.fadeIn();
                    $earningsLoading.remove();

                },
                error: function(data) {
                    console.log(data);
                    $earningsLoading.remove();
                }
            });

            $.ajax({
                type: "POST",
                url: "/sentimentanalysisytcomments",
                data: {"youtubeid": step_3, "boxofficemojoname": step_2},
                cache: false,
                success: function(data) {
                    console.log(data);
                    $analysis.remove();
                },
                error: function(data) {
                    var error = $.parseJSON(data.responseText);
                    $('#analysis').append('<h3>' + error['error'] + '</h3>');
                    console.log(data);
                    $analysis.remove();
                }
            });
        }
    });
});