configs = {"http://www.23wx.com": {
    "encoding": "gbk",
    "list": {"regex": "/class/\d+_\d+.html|/quanben/\d+", "type": 1},
    "detail": {"regex": "http://www.23wx.com/book/\d+", "type": 2},
    "detailList": {"regex": "http://www.23wx.com/html/\d+/\d+/", "type": 3},
    "title": "<h1>(.+)\S* 最新章节更新列表</h1>|<h1>(.+)\S* 全文阅读</h1>",
    "author": "<h3>.+?作者：(.+?)</h3>|<th>文章作者</th><td>&nbsp;(.+?)</td>",
    "detailItem": "<a href=\"(\d+.html)\">(.+?)</a>",
    "time": "<td class=\"C\">(\d+-\d+-\d+)</td>",
    "lastTime": "00-00-00",
    "icon": "http://www.23wx.com/files/article/image/\d+/\d+/.+?\.jpg",
    "itemSort": False
},
    "http://www.7dsw.com": {
        "encoding": "gbk",
        "list": {"regex": "http://www.7dsw.com/sort\d+/\d+.html|/quanben/\d*|/toplastupdate/\d+.html", "type": 1},
        "detail": {"regex": "http://www.7dsw.com/book/\d+/\d+/", "type": 3},
        "detailList": {"regex": "http://www.7dsw.com/book/\d+/\d+/", "type": 3},
        "title": "<h1>(.+)?</h1>",
        "author": "<i>作者：(.+)?</i>",
        "detailItem": "<a href=\"(\d+.html)\" title=\"(.+)?\">",
        "time": "<span class=\"s5\">(\d+-\d+-\d+)</span>",
        "lastTime": "00-00-00",
        "icon": "http://www.7dsw.com/files/article/image/\d+/\d+/.+?\.jpg",
        "itemSort": False
    },
    "http://www.bxwx.org": {
        "encoding": "gbk",
        "list": {
            "regex": "http://www.bxwx.org/modules/article/toplist.php\?sort=[a-z]+|/bsort\d+/\d+/\d+.htm|/modules/article/index.php",
            "type": 1},
        "detail": {"regex": "/binfo/\d+/\d+.htm", "type": 2},
        "detailList": {"regex": "http://www.bxwx.org/b/\d+/\d+/index.html", "type": 3},
        "title": "<div id=\"title\">(.+)\S*全集下载</div>|<strong>(.+?)全集下载</strong>",
        "author": "作者：<a .+?>(.+?)</a>|\"/modules/article/searchh.php\?searchtype=author&searchkey=(.+?)\"",
        "detailItem": "<a href=\"(\d+.html)\">(.+?)</a>",
        "time": "<td class=\"odd\" align=\"center\">(\d+-\d+-\d+)</td>",
        "lastTime": "00-00-00",
        "icon": "http://www.bxwx.org/image/\d+/\d+/.+?\.jpg",
        "itemSort": True
    },
    "http://www.sqsxs.com/": {
        "encoding": "gbk",
        "list": {
            "regex": "http://www\.sqsxs\.com/sort\d+/\d+\.html|/quanben/\d*|/toplastupdate/\d+\.html",
            "type": 1},
        "detail": {"regex": "http://www.sqsxs.com/book/\d+/\d+/", "type": 3},
        "detailList": {"regex": "http://www.sqsxs.com/book/\d+/\d+/", "type": 3},
        "title": "<h1>(.+)?</h1>",
        "author": "<i>作者：(.+)?</i>",
        "detailItem": "<a href=\"(\d+.html)\" title=\"(.+)?\">",
        "time": "<span class=\"s5\">(\d+-\d+-\d+)</span>",
        "lastTime": "00-00-00",
        "icon": "http://www.sqsxs.com/files/article/image/\d+/\d+/.+?\.jpg",
        "itemSort": False
    },
    "http://www.aszw520.com/": {
        "encoding": "gbk",
        "list": {
            "regex": "/toplastupdate/\d+\.html",
            "type": 1},
        "detail": {"regex": "http://www.aszw520.com/book/\d+/\d+/", "type": 3},
        "detailList": {"regex": "http://www.aszw520.com/book/\d+/\d+/", "type": 3},
        "title": "<h1>(.+)?</h1>",
        "author": "<i>作者：(.+)?</i>",
        "detailItem": "<a href=\"(\d+.html)\">(.+?)</a>",
        "time": "<td class=\"C\">\d+-\d+-\d+</td>",
        "lastTime": "00-00-00",
        "icon": "http://www.aszw520.com/files/article/image/\d+/\d+/.+?\.jpg",
        "itemSort": False
    }
};
