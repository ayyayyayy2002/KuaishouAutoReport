var callback = arguments[arguments.length - 1]; 

let ids = [];
function makeRequest(keyword, pcursor) {
    const data = JSON.stringify({
        'operationName': 'visionSearchPhoto',
        'variables': {
            'keyword': keyword,
            'pcursor': pcursor,
            'page': 'search'
        },
        'query': 'fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n' // 省略长查询内容
  });

    let xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.open('POST', 'https://www.kuaishou.com/graphql');
    xhr.setRequestHeader('Accept-Language', 'zh-CN,zh;q=0.9');
    xhr.setRequestHeader('accept', '*/*');
    xhr.setRequestHeader('content-type', 'application/json');

    xhr.onload = function() {
        let response = JSON.parse(xhr.response);
        
        // 收集作者ID
        response.data.visionSearchPhoto.feeds.forEach(feed => {
            ids.push(feed.author.id);
        });

        // 检查是否获取到最后一页
        if (pcursor === '1') {
            console.warn(ids)
            callback(ids); // 将结果作为返回值
        } else {
            makeRequest(keyword, String(parseInt(pcursor) + 1));
        }
    };

    xhr.send(data);
}

// 调用 makeRequest 函数并传递关键字
makeRequest(arguments[0], '0');