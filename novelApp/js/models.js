function BookModel(book) {
	var self = this;
	self.BookId = book._id;
	self.BookName = book.BookName;
	self.Author = book.Author;
	self.Icon = book.Icon;
	self.IsLocal = false;
	self.LastReadTime = new Date();
	self.HasNew = false;
	self.Links = [];
	return self;
}

function LinkModel() {
	var self = this;
	return self;
}