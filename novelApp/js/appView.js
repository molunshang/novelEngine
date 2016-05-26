var List = React.createClass({
		render: function() {
			var items = this.props.data.map(function(item) {
					return ( < Item key = {
							item._id
						}
						book = {
							item
						}
						/>);
					});
				return ( < ul id = "books"
					className = "mui-table-view mui-grid-view mui-grid-9" > {
						items
					} < /ul>
				);
			}
		});
	var Item = React.createClass({
			imgLoadError: function() {
				ReactDOM.findDOMNode(this).getElementsByTagName("img")[0].src = "images/nocover.jpg";
			},
			saveToLocal: function() {
				var book = new BookModel(this.props.book);
				api.addToLocal(book);
			},
			render: function() {
				var item = this.props.book;
				return ( < li onClick = {
						this.saveToLocal
					}
					className = "mui-table-view-cell mui-media mui-col-xs-4 mui-col-sm-3" > < img onError = {
						this.imgLoadError
					}
					src = {
						(item.Icon || 'images/nocover.jpg')
					}
					style = {
						{
							maxHeight: '125px',
							maxWidth: '100px'
						}
					}
					/ > < div className = "mui-media-body" > {
					item.BookName
				} < /div></li > );
		}
	});

mui.init({
	pullRefresh: {
		container: '#pullrefresh',
		down: {
			callback: pulldownRefresh
		}
	}
});

/**
 * 下拉刷新具体业务实现
 */
function pulldownRefresh() {
	setTimeout(function() {
			api.getLocalBooks();
			api.list(1).done(function(res) {
					if (res.isok) {
						ReactDOM.render( < List data = {
								res.data
							}
							/>, document.getElementById('content'));
						}
					}); mui('#pullrefresh').pullRefresh().endPulldownToRefresh(); //refresh completed
			}, 1500);
	}
	if (mui.os.plus) {
		mui.plusReady(function() {
			setTimeout(function() {
				mui('#pullrefresh').pullRefresh().pulldownLoading();
			}, 1000);
		});
	} else {
		mui.ready(function() {
			mui('#pullrefresh').pullRefresh().pulldownLoading();
		});
	}