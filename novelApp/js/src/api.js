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
	var db;

	function excuteSql(sql, args) {
		db = db || openDatabase("novelDb", "1.0", "novelDb", 1024 * 1024 * 5);
		args = args || [];
		var dfd = $.Deferred();
		if (typeof sql == "object") {
			var argIndex = 0;

			function excute(tx) {
				tx.executeSql(sql[argIndex], args[argIndex] || [], function() {
					if (argIndex >= sql.length - 1) {
						dfd.resolve(arguments, dfd);
						return;
					}
					argIndex++;
					excute(arguments[0]);
				}, function() {
					console.log(arguments);
					dfd.reject(arguments, dfd);
				});
			}
			db.transaction(function(tx) {
				excute(tx);
			});
		} else {
			db.transaction(function(tx) {
				tx.executeSql(sql, args, function(tx, results) {
					dfd.resolve(arguments, dfd);
				}, function() {
					dfd.reject(arguments, dfd);
				})
			});
		}
		return dfd;
	}
	api = window.api || {};
	api.debug = function(args) {
		for (var key in args) {
			try {
				console.log("key:" + key + ",data:" + args[key] + ",type:" + typeof args[key]);
				if (typeof args[key] == "object") {
					api.debug(args[key]);
				}
			} catch (e) {
				
			}
		}
	};
	api.errorImg = function imgLoadError(img) {
		img.target.src = "images/nocover.jpg";
	};
	api.root = "http://192.168.1.34:5000";
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
	api.initDb = function() {
		var sql = ["CREATE TABLE IF NOT EXISTS books (bookId primary key, name,author,isLocal,icon,lastReadTime,hasNew)", "CREATE TABLE IF NOT EXISTS links (linkId INTEGER PRIMARY KEY AUTOINCREMENT, name,num,links,content,bookId)", "CREATE TABLE IF NOT EXISTS SiteConfig (SiteHost primary key, SiteName,DetailMatch,MatchType)", "CREATE TABLE IF NOT EXISTS Configs (name primary key, value)"];
		return excuteSql(sql);
	};
	api.getLocalBooks = function() {
		var dfd = $.Deferred();
		excuteSql("select * from books order by lastReadTime desc").done(function(results) {
			var books = [];
			for (var i = 0; i < results[1].rows.length; i++) {
				var row = results[1].rows.item(i);
				if (!row)
					continue;
				var book = {
					"_id": row.bookId,
					"BookName": row.name,
					"Author": row.author,
					"IsLocal": row.isLocal,
					"Icon": row.icon,
					"LastReadTime": row.lastReadTime
				};
				books.push(book);
			}
			dfd.resolve(books);
		}).fail(function() {
			dfd.reject(arguments);
		});
		return dfd;
	};
	api.addToLocal = function(book) {
		return excuteSql("INSERT OR IGNORE INTO books(bookId, name,author,isLocal,icon,lastReadTime,hasNew) VALUES (?,?,?,?,?,?,?)", [book._id, book.BookName, book.Author, book.IsLocal, book.Icon, new Date().getTime(), 0]).done(function() {
			console.log(arguments);
		}).fail(function() {
			console.log(arguments);
		});
	};
	api.setNewRead = function(bookId) {
		return excuteSql("UPDATE books set lastReadTime=? WHERE bookId=?", [new Date().getTime(), bookId])
	};
	api.createConfig = function(config) {
		return excuteSql("REPLACE INTO SiteConfig(SiteHost, SiteName,DetailMatch,MatchType) VALUES(?,?,?,?)", [confing.SiteHost, config.SiteName, config.DetailMatch, config.MatchType]);
	};
	api.getLocalConfig = function() {
		return excuteSql("SELECT SiteHost, SiteName,DetailMatch,MatchType FROM SiteConfig");
	};
	api.createConfigs = function(configs) {
		var sql = [],
			args = [];
		configs.map(function(config) {
			sql.push("REPLACE INTO SiteConfig(SiteHost, SiteName,DetailMatch,MatchType) VALUES(?,?,?,?)");
			args.push([config.SiteHost, config.SiteName, config.DetailMatch, config.MatchType]);
		});
		return excuteSql(sql, args);
	};
})();