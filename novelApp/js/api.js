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
var api = {
	//	list: function(index) {
	//		var worker = new workItem();
	//		if (index <= 0)
	//			index = 1;
	//		var link = "1.json"; //config.host + "/list/" + index;
	//		mui.getJSON(link, null, function(data) {
	//			worker.setResult(data);
	//		});
	//		return worker;
	//	},
	//	search: function(name) {
	//		var worker = new workItem();
	//		if (name == null || name.length <= 0) {
	//			worker.setResult({
	//				isok: false
	//			});
	//			return worker;
	//		}
	//		var link = config.host + "/search/" + name;
	//		mui.getJSON(link, null, function() {
	//			worker.setResult(data);
	//		});
	//		return worker;
	//	},
	//	getLocalBooks: function() {
	//		var worker = new workItem();
	//		html5sql.process("select * from books order by LastReadTime desc", function(transaction, results) {
	//			var books = [];
	//			for (var i = 0; i < results.rows.length; i++) {
	//				var row = results.rows[i];
	//				var book = {
	//					"_id": row.bookId,
	//					"BookName": row.name,
	//					"Author": row.author,
	//					isLocal: true,
	//					"Icon": row.icon,
	//					"LastReadTime": row.lastReadTime
	//				};
	//				books.push(book);
	//			}
	//			worker.setResult(books);
	//		});
	//		return worker;
	//	},
	//	addToLocal: function(book) {
	//		var worker = new workItem();
	//		var sql = "INSERT OR IGNORE INTO books(bookId, name,author,isLocal,icon,lastReadTime,hasNew) VALUES (?,?,?,?,?,?,?)";
	//		html5sql.process([{
	//			"sql": sql,
	//			"data": [book.BookId, book.BookName, book.Author, book.IsLocal, book.Icon, new Date(), 0],
	//			"success": function(transaction, results) {
	//				worker.setResult(true);
	//			},
	//		}], function() {}, function() {});
	//		return worker;
	//	},
	//	setNewRead: function(bookId) {
	//		var worker = new workItem();
	//		var sql = "UPDATE books set lastReadTime=? WHERE bookId=?";
	//		html5sql.process([{
	//			"sql": sql,
	//			"data": [new Date(), bookId],
	//			"success": function(transaction, results) {
	//				worker.setResult(true);
	//			},
	//		}], function() {}, function() {});
	//		return worker;
};