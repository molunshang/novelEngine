(function() {
	function apiCall(url, type, data) {
		var task = $.Deferred();
		$.ajax({
			type: type || "GET",
			url: api.root + url,
			async: true,
			data: data,
			success: function(res) {
				task.resolve(res);
			},
			error: function() {
				task.reject(arguments);
			}
		});
		return task;
	}
	api = window.api || {};
	api.root = "";
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
})();