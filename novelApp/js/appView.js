var ListBox = React.createClass({
			getInitialState: function() {
				return {
					data: this.props.data || []
				};
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
				var newBooks = [book].concat(books);
				this.setState({
					data: newBooks
				});
			},
			render: function() {
				return ( < List data = {
						this.state.data
					}
					contentChange = {
						this.listChange
					}
					/>)
				}
			});
		var List = React.createClass({
					listChange: function(book) {
						this.props.contentChange(book)
					},
					render: function() {
						var list = this;
						return ( < ul id = "books"
							className = "mui-table-view mui-grid-view mui-grid-9" > {
								this.props.data.map(function(item) {
										return ( < Item key = {
												item._id
											}
											book = {
												item
											}
											onSaveLocal = {
												this.listChange
											}
											/>);
										}.bind(this))
								} < /ul>
							);
						}
					});
				var Item = React.createClass({
					imgLoadError: function() {
						ReactDOM.findDOMNode(this).getElementsByTagName("img")[0].src = "images/nocover.jpg";
					},
					saveToLocal: function() {
						var self = this;
						var book = self.props.book;
						api.setNewRead(book._id);
						self.props.onSaveLocal(self.props.book);
					},
					render: function() {
						var item = this.props.book;
						return ( < li onTouchEnd = {
								this.saveToLocal
							}
							className = "mui-table-view-cell mui-media mui-col-xs-4 mui-col-sm-3" > < img onError = {
								this.imgLoadError
							}
							onTouchEnd = {
								this.saveToLocal
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
							/ > < div className = "mui-media-body" 
							onTouchEnd = {
								this.saveToLocal
							} > {
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
							api.getLocalBooks().done(function(data) {
									ReactDOM.render( < ListBox data = {
											data
										}
										/>, document.getElementById('content'));
									}); mui('#pullrefresh').pullRefresh().endPulldownToRefresh(); //refresh completed
							}, 1500);
					};
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