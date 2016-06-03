var Item = React.createClass({
	selfData: {},
	touchStart: function() {
		this.selfData.move = false;
	},
	touchMove: function() {
		this.selfData.move = true;
	},
	touchEnd: function() {
		if (this.selfData.move) {
			return;
		}
		this.saveToLocal();
	},
	saveToLocal: function() {
		api.setNewRead(this.props.data._id);
		this.props.onSaveLocal(this.props.data);
	},
	render: function() {
		var book = this.props.data;
		return ( < li className = "mui-table-view-cell mui-media mui-col-xs-4"
			onTouchStart = {
				this.touchStart
			}
			onTouchMove = {
				this.touchMove
			}
			onTouchEnd = {
				this.touchEnd
			} >
			< a href = "javascript:void(0)" >
			< img className = "mui-media-object"
			onError = {
				api.errorImg
			}
			src = {
				book.Icon || 'images/nocover.jpg'
			}
			style = {
				{					
					maxWidth: '100px',
					maxHeight: '125px'
				}
			}
			/> < div className = "mui-media-body" > {
			book.BookName
		} < /div> < /a > < /li>
	);
}
});
var List = React.createClass({
			getInitialState: function() {
				return {
					data: this.props.data || []
				}
			},
			listChange: function(book) {
				var books = this.state.data;
				var i = 0;
				for (; i < books.length; i++) {
					if (book == books[i]) {
						break;
					}
				}
				books.splice(i, 1);
				this.setState({
					data: [book].concat(books)
				});
			},
			refresh: function(data) {
				var list = data || this.state.data;
				this.setState({
					data: list
				});
			},
			render: function() {
				var listViews = this.state.data.map(function(book) {
						return ( < Item key = {
								book._id
							}
							data = {
								book
							}
							onSaveLocal = {
								this.listChange
							}
							/>);
						}.bind(this));
					return ( < ul className = "mui-table-view mui-grid-view mar_b140" > {
							listViews
						} < li className = "mui-table-view-cell mui-media mui-col-xs-4" >
						< a href = "javascript:void(0)"
						id = "menu-btn" >
						< img className = "mui-media-object"
						src = "images/addbook.png"
						style = {
							{
								minHeight: '125px',
								minWidth: '100px'
							}
						}
						/> < div className = "mui-media-body" > 添加图书 < /div > < /a > < /li > < /ul > );
					}
				});