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
							} < li className = "mui-table-view-cell mui-media mui-col-xs-4 mui-col-sm-3" > < img src = "images/addbook.png" / > < div className = "mui-media-body" > 添加小说 < /div > < /li > < /ul >
						);
					}
				});
			var Item = React.createClass({
					imgLoadError: function() {
						ReactDOM.findDOMNode(this).getElementsByTagName("img")[0].src = "images/nocover.jpg";
					},
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
						var self = this;
						var book = self.props.book;
						api.setNewRead(book._id);
						self.props.onSaveLocal(self.props.book);
					},
					selfData: {},
					render: function() {
						var item = this.props.book;
						return ( < li onTouchStart = {
								this.touchStart
							}
							onTouchMove = {
								this.touchMove
							}
							onTouchEnd = {
								this.touchEnd
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
							/ > < div className = "mui-media-body"> {
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
			React.initializeTouchEvents(true);