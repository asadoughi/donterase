var image_fn = function (result) {
    if (result.length == 0) {
	$("#images").append("<div style='padding-top:10px;'>Image not found.</div>");	
	return;
    }

    for (i in result) {
	result[i].tags.reverse();
	$("#images").append(
	    '<div style="padding-top: 10px;">' +
		'<a href="/get/?id=' + result[i].id +'" rel="external">' +
		'<img style="width: 100%;" src="' + result[i].url + '" alt="' + result[i].id + '" />' +
		'</a>' +
		'<div class="ui-grid-a" style="padding-top: 5px; max-width: 400px; margin: 0 auto;">' +
		'<div class="ui-block-a">' + result[i].tags + '</div>' +
		'<div class="ui-block-b">' + result[i].datetime + '</div>' +
		'</div>' +
		'</div>');
    }
}

$(document).on("pageinit","#indexpage", function() {
    $.ajax({
	url: '/files/latest',
        cache: false,
        dataType: 'json',
	success: image_fn,
    });
});

$('#search-form').submit(function() {
    var query = $('#search-basic')[0].value;
    if (query.length == 0) {
	return false;
    }
    $.ajax({
	url: '/files/tags',
        dataType: 'json',
	type: 'GET',
	data: { 'q' : query },
	success: function(result) {
	    $("#images").empty();
	    if (result.length == 0) {
		$("#images").append("<div style='padding-top:10px;'>No images found.</div>");
	    } else {
		image_fn(result);
	    }
	    $('#search-basic').blur();
	},
    });
    return false;
});

$(document).on("pageshow", "#getpage", function() {
    var index = window.location.href.lastIndexOf('id=');
    var id_param = window.location.href.substring(index+3);
    $.ajax({
	url: '/files/get',
        cache: true,
	data : { 'id' : id_param },
        dataType: 'json',
	success: function(result) {
	    image_fn(result);
	    document.title = "Don't Erase: Image " + result[0].id + ": " + result[0].tags;
	    stWidget.addEntry({
		"service":"facebook",
		"element":document.getElementById('st_button_1'),
		"url":window.location.href,
		"title":document.title,
		"type":"large",
		"text":result[0].tags.join(","),
		"image":result[0].url,
		"summary":result[0].tags.join(",")
	    });
	    stWidget.addEntry({
		"service":"twitter",
		"element":document.getElementById('st_button_2'),
		"url":window.location.href,
		"title":document.title,
		"type":"large",
		"text":result[0].tags.join(","),
		"image":result[0].url,
		"summary":result[0].tags.join(",")
	    });
	    stWidget.addEntry({
		"service":"tumblr",
		"element":document.getElementById('st_button_3'),
		"url":window.location.href,
		"title":document.title,
		"type":"large",
		"text":result[0].tags.join(","),
		"image":result[0].url,
		"summary":result[0].tags.join(",")
	    });
	    stWidget.addEntry({
		"service":"email",
		"element":document.getElementById('st_button_4'),
		"url":window.location.href,
		"title":document.title,
		"type":"large",
		"text":result[0].tags.join(","),
		"image":result[0].url,
		"summary":result[0].tags.join(",")
	    });
	}
    });
});
