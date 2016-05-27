var config = {
	host: "http://192.168.1.78:5000"
};

(function initApp() {
	html5sql.openDatabase("novelDb", "novelDb", 1024 * 1024 * 5, function() {
		var sql = ["CREATE TABLE IF NOT EXISTS books (bookId primary key, name,author,isLocal,icon,lastReadTime,hasNew)", "CREATE TABLE IF NOT EXISTS links (linkId INTEGER PRIMARY KEY AUTOINCREMENT, name,num,links,content,bookId)"];
		html5sql.process(sql, function(res) {
		}, function(res) {
			mui.toast("本地初始化数据失败!");
		});
	});
})();
