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
		var link = config.host + "/list/" + index;
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
	}
};