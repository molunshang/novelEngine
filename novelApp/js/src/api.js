(function() {
	function apiCall(url, type, data) {
		var task = $.Deferred();
		$.ajax({
			type: type || "GET",
			url: api.root + url,
			async: true,
			data: data,
			success: function(res) {
				console.log(JSON.stringify(res));
				task.resolve(res);
			},
			error: function() {
				task.reject(arguments);
			}
		});
		return task;
	}
	api = window.api || {};
	api.errorImg = function imgLoadError(img) {
		img.target.src = "images/nocover.jpg";
	};
	api.root = "http://192.168.31.126:5000";
	api.getConfig = function() {
		return apiCall("/api/config");
	};
	api.search = function(name) {
		return apiCall("/api/search/" + name);
	};
	api.getBooksNews = function(books, serverTime) {
		var data = {};
		if (typeof books == "string") {
			data["books"] = books;
		} else if (typeof books == "object") {
			data["books"] = books.join(",");
		}
		return apiCall("/api/newbooklist/" + serverTime, "GET", data);
	};
	api.getLocalBooks = function() {
		return apiCall("/api/list/1");
	}
})();