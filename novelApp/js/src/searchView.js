var SearchItem = React.createClass({
	add: function() {
		var book = this.props.data;
		book.IsLocal = false;
		console.log(JSON.stringify(book));
		api.addToLocal(book).done(function() {
			console.log("back");
			mui.back();
		});
	},
	render: function() {
		var book = this.props.data;
		return ( < li className = "mui-table-view-cell mui-media"
				onClick = {
					this.add
				} >
				< a href = "javascript:void(0)"
				style = {
					{
						position: "relative"
					}
				} >
				< img className = "mui-pull-left"
				onError = {
					api.errorImg
				}
				src = {
					book.Icon || 'images/nocover.jpg'
				}
				style = {
					{
						maxHeight: '125px',
						maxWidth: '100px'
					}
				}
				/> < div className = "mui-media-body pad_l10" > {
				book.BookName
			} < div className = "mar_t20" >
			< p className = 'mui-ellipsis' > {
				book.Author
			} < /p> < p className = 'mui-ellipsis' > < /p > < /div> < p className = 'mui-ellipsis Seach_Cready' > < span className = "mui-badge-warning mui-badge-inverted" > 611 万 < /span > 人在读 < /p > < /div > < /a > < /li > );
}
});
var SearchList = React.createClass({
		render: function() {
			var list = this.props.data || [];
			var content = list.map(function(item) {
					return ( < SearchItem key = {
							item._id
						}
						data = {
							item
						}

						/> );
					});
				return ( < div className = "mui-content" > < ul className = "mui-table-view" > {
					content
				} < /ul></div > );
			}
		});
	var Header = React.createClass({
		changeSearch: function(e) {
			if (e.keyCode == 13) {
				var name = e.target.value;
				this.props.onSearchChange(name);
			}
		},		
		render: function() {
			return ( < header className = "mui-bar mui-bar-nav bgECECEC" >
				< a className = "mui-action-back mui-icon mui-icon-back mui-pull-left" > < /a> < a id = "offCanvasBtn"
				href = "#offCanvasSide"
				className = "mui-icon mui-action-menu mui-icon-bars mui-pull-right" > < /a> < div className = "mui-content-padded Seach_Htitle" > < div className = "mui-input-row mui-search" > < input type = "search"
				className = "mui-input-clear"
				placeholder = ""
				style = {
					{
						background: "#FFFFFF"
					}
				}
				onKeyUp = {
					this.changeSearch
				}
				/> < /div > < /div > < /header > );
		}
	});
	var SearchBox = React.createClass({
			getInitialState: function() {
				return {
					data: []
				};
			},
			search: function(name) {
				api.search(name).done(function(res) {
					if (res.isok) {
						console.log(JSON.stringify(res.data));
						this.setState({
							data: res.data
						});
					}
				}.bind(this));
			},
			render: function() {
				return ( < div > < Header onSearchChange = {
						this.search
					}
					/> < SearchList data = {
					this.state.data
				}
				/></div >
			);
		}
	});