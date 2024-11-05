import requests

cookies = {
    'kpf': 'PC_WEB',
    'clientid': '3',
    'did': 'web_907b36d79f318a5ef82247f1dd586d5f',
    'userId': '2663075008',
    'kuaishou.server.webday7_st': 'ChprdWFpc2hvdS5zZXJ2ZXIud2ViZGF5Ny5zdBKwAfnALcv8aF4VY06oXcsYHPvGuwavE0zhkYMNra0RV0X1uYsjPH3mLhWlbF9O6UFBd1dBED5biFan_mIQGRoDvzrx6ch2GGBWQ2zmb5HW8rgs-zI02mAS9Fos5lYEqoma6Udgvg-LOscB9fdfpZ5ONyc8jnBcZ9XOawX8NnSJKbFLCABFoNI6T7P-l_QwDSOLTcq6dfzwCWskNbbSDNux_wQcgQLHPD0CFaSJh3Ebqh0QGhJD7YlmW-_sv6V67wWUp_0VYZkiIPt1S0KsFIJGfrQbcEPdJBQ35cphfF3VsilKBCpMHZTrKAUwAQ',
    'kuaishou.server.webday7_ph': 'a4ca60e3c8fe2c88aee7d2436d64d4855849',
    'kpn': 'KUAISHOU_VISION',
}

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    # 'Cookie': 'kpf=PC_WEB; clientid=3; did=web_907b36d79f318a5ef82247f1dd586d5f; userId=2663075008; kuaishou.server.webday7_st=ChprdWFpc2hvdS5zZXJ2ZXIud2ViZGF5Ny5zdBKwAfnALcv8aF4VY06oXcsYHPvGuwavE0zhkYMNra0RV0X1uYsjPH3mLhWlbF9O6UFBd1dBED5biFan_mIQGRoDvzrx6ch2GGBWQ2zmb5HW8rgs-zI02mAS9Fos5lYEqoma6Udgvg-LOscB9fdfpZ5ONyc8jnBcZ9XOawX8NnSJKbFLCABFoNI6T7P-l_QwDSOLTcq6dfzwCWskNbbSDNux_wQcgQLHPD0CFaSJh3Ebqh0QGhJD7YlmW-_sv6V67wWUp_0VYZkiIPt1S0KsFIJGfrQbcEPdJBQ35cphfF3VsilKBCpMHZTrKAUwAQ; kuaishou.server.webday7_ph=a4ca60e3c8fe2c88aee7d2436d64d4855849; kpn=KUAISHOU_VISION',
    'Origin': 'https://www.kuaishou.com',
    'Referer': 'https://www.kuaishou.com/search/video?searchKey=DASDAD',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    'accept': '*/*',
    'content-type': 'application/json',
    'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

json_data = {
    'operationName': 'visionSearchPhoto',
    'variables': {
        'keyword': 'DASDAD',
        'pcursor': '1',
        'page': 'search',
        'searchSessionId': 'MTRfMjY2MzA3NTAwOF8xNzMwNzc0NzY3ODEwX0RBU0RBRF81OTY1',
    },
    'query': 'fragment photoContent on PhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment recoPhotoFragment on recoPhotoEntity {\n  __typename\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  commentCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  riskTagContent\n  riskTagUrl\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    ...recoPhotoFragment\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    searchSessionId\n    pcursor\n    aladdinBanner {\n      imgUrl\n      link\n      __typename\n    }\n    __typename\n  }\n}\n',
}

response = requests.post('https://www.kuaishou.com/graphql', cookies=cookies, headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
data = '{"operationName":"visionSearchPhoto","variables":{"keyword":"DASDAD","pcursor":"1","page":"search","searchSessionId":"MTRfMjY2MzA3NTAwOF8xNzMwNzc0NzY3ODEwX0RBU0RBRF81OTY1"},"query":"fragment photoContent on PhotoEntity {\\n  __typename\\n  id\\n  duration\\n  caption\\n  originCaption\\n  likeCount\\n  viewCount\\n  commentCount\\n  realLikeCount\\n  coverUrl\\n  photoUrl\\n  photoH265Url\\n  manifest\\n  manifestH265\\n  videoResource\\n  coverUrls {\\n    url\\n    __typename\\n  }\\n  timestamp\\n  expTag\\n  animatedCoverUrl\\n  distance\\n  videoRatio\\n  liked\\n  stereoType\\n  profileUserTopPhoto\\n  musicBlocked\\n  riskTagContent\\n  riskTagUrl\\n}\\n\\nfragment recoPhotoFragment on recoPhotoEntity {\\n  __typename\\n  id\\n  duration\\n  caption\\n  originCaption\\n  likeCount\\n  viewCount\\n  commentCount\\n  realLikeCount\\n  coverUrl\\n  photoUrl\\n  photoH265Url\\n  manifest\\n  manifestH265\\n  videoResource\\n  coverUrls {\\n    url\\n    __typename\\n  }\\n  timestamp\\n  expTag\\n  animatedCoverUrl\\n  distance\\n  videoRatio\\n  liked\\n  stereoType\\n  profileUserTopPhoto\\n  musicBlocked\\n  riskTagContent\\n  riskTagUrl\\n}\\n\\nfragment feedContent on Feed {\\n  type\\n  author {\\n    id\\n    name\\n    headerUrl\\n    following\\n    headerUrls {\\n      url\\n      __typename\\n    }\\n    __typename\\n  }\\n  photo {\\n    ...photoContent\\n    ...recoPhotoFragment\\n    __typename\\n  }\\n  canAddComment\\n  llsid\\n  status\\n  currentPcursor\\n  tags {\\n    type\\n    name\\n    __typename\\n  }\\n  __typename\\n}\\n\\nquery visionSearchPhoto($keyword: String, $pcursor: String, $searchSessionId: String, $page: String, $webPageArea: String) {\\n  visionSearchPhoto(keyword: $keyword, pcursor: $pcursor, searchSessionId: $searchSessionId, page: $page, webPageArea: $webPageArea) {\\n    result\\n    llsid\\n    webPageArea\\n    feeds {\\n      ...feedContent\\n      __typename\\n    }\\n    searchSessionId\\n    pcursor\\n    aladdinBanner {\\n      imgUrl\\n      link\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}'
response = requests.post('https://www.kuaishou.com/graphql', cookies=cookies, headers=headers, data=data)
print(response.text)