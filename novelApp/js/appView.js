var ListBox = React.createClass({
			getInitialState: function() {
				return {
					data: this.props.data || []
				};
			},
			listChange: function(book) {
				var books = this.state.data;
				book = JSON.parse(JSON.stringify(book));
				book._id = book._id + "0000" + book._id;
				var newBooks = books.concat([book]);
				this.setState({
					data: newBooks
				});
				console.log(this.state.data);
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
						var book = new BookModel(self.props.book);
						book.IsLocal = true;
						api.addToLocal(book);
						self.props.onSaveLocal(self.props.book);
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
								ReactDOM.render( < ListBox data = {
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