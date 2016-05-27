function workItem() {
	var self = this;
	self.workQueue = [];
	self.done = function(func) {
		self.workQueue.push(func);
		if (self.result) {
			while (self.workQueue.length > 0) {
				var work = self.workQueue.pop();
				work(self.result);
			}
		}
	};
	self.setResult = function(res) {
		self.result = res;
		while (self.workQueue.length > 0) {
			var work = self.workQueue.pop();
			work(self.result);
		}
	};
}

function imgLoadError(img) {
	img.src = "images/nocover.jpg";
}
var api = {
	list: function(index) {
		var worker = new workItem();
		if (index <= 0)
			index = 1;
		var link = "1.json"; //config.host + "/list/" + index;
		mui.getJSON(link, null, function(data) {
			worker.setResult(data);
		});
		return worker;
	},
	search: function(name) {
		var worker = new workItem();
		if (name == null || name.length <= 0) {
			worker.setResult({
				isok: false
			});
			return worker;
		}
		var link = config.host + "/search/" + name;
		mui.getJSON(link, null, function() {
			worker.setResult(data);
		});		
		return worker;
	},
	getLocalBooks: function() {
		var worker = new workItem();
		console.log("books_local");
		html5sql.process("select * from books", function(transaction, results) {
			for (var i = 0; i < results.rows.length; i++) {
				var row = results.rows[i];
				var books = [];
				console.log(row);
			}
		});
		return worker;
	},
	addToLocal: function(book) {
		var worker = new workItem();
		var sql = "INSERT OR IGNORE INTO books(bookId, name,author,isLocal,icon,lastReadTime,hasNew) VALUES (?,?,?,?,?,?,?)";
		html5sql.process([{
			"sql": sql,
			"data": [book.BookId, book.BookName, book.Author, book.IsLocal, book.Icon, new Date(), 0],
			"success": function(transaction, results) {
				worker.setResult(true);
			},
		}], function() {}, function() {});
		return worker;
	}
};