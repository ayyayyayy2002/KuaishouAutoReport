var callback = arguments[arguments.length - 1];
const pathParts = window.location.pathname.split('/');
const userId = pathParts[2]; // 提取路径中的第二部分作为 userId
const delay = 30
const timeout = 3000
let pcursor = '';

let output = ''
let lastoutput = '默认请求输出'












const floatingWindow = document.createElement('div');
floatingWindow.style.position = 'fixed';
floatingWindow.style.top = '110px';
floatingWindow.style.right = '20px';
floatingWindow.style.zIndex = '9999';
floatingWindow.style.background = 'white';
floatingWindow.style.border = '1px solid #ccc';
floatingWindow.style.padding = '10px';
floatingWindow.style.maxWidth = '340px';
floatingWindow.style.overflow = 'auto'; // Add overflow property for scrolling
floatingWindow.style.height = '200px'; // Set a height for the window
floatingWindow.style.scrollBehavior = 'smooth'; // Enable smooth scrolling
document.body.appendChild(floatingWindow);

// Create diagnostic info container
const diagnosticInfo = document.createElement('div');
floatingWindow.appendChild(diagnosticInfo);

// Function to scroll to the bottom of the floating window
function scrollToBottom() {
    floatingWindow.scrollTop = floatingWindow.scrollHeight;
    // Scroll the last element into view
    const lastElement = floatingWindow.lastElementChild;
    if (lastElement) {
        lastElement.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
}


//######################################################################################################################
function FollowUser(){
    const followdata = JSON.stringify({
        'operationName': 'visionFollow',
        'variables': {
            'touid': userId,
            'ftype': 1,
            'followSource': 1
        },
        'query': 'mutation visionFollow($touid: String, $ftype: Int, $followSource: Int, $expTag: String) {\n  visionFollow(touid: $touid, ftype: $ftype, followSource: $followSource, expTag: $expTag) {\n    result\n    followStatus\n    hostName\n    error_msg\n    __typename\n  }\n}\n'
    });

    let followxhr = new XMLHttpRequest();
    followxhr.withCredentials = true;
    followxhr.open('POST', 'https://www.kuaishou.cn/graphql');
    followxhr.setRequestHeader('Accept-Language', 'zh-CN,zh;q=0.9');
    followxhr.setRequestHeader('accept', '*/*');
    followxhr.setRequestHeader('content-type', 'application/json');
    followxhr.onload = function() {
        updateDiagnosticInfo(followxhr.response);
    };

    followxhr.send(followdata);
}
//######################################################################################################################


// Updating the diagnosticInfo.innerHTML with the scroll to bottom
function updateDiagnosticInfo(content) {
    diagnosticInfo.innerHTML += content;
    scrollToBottom();
}

function fetchPhotos(pcursor) {
    const data = JSON.stringify({
        'operationName': 'visionProfilePhotoList',
        'variables': {
            'userId': userId,
            'pcursor': pcursor,
            'page': 'profile'
        },
        'query': `query visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) { visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) { feeds { photo { ... on PhotoEntity { id } ... on recoPhotoEntity { id } } __typename } pcursor } }`
    });

    let xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.open('POST', 'https://www.kuaishou.cn/graphql');


    // 设置请求头
    setHeaders(xhr);

    xhr.onload = function() {
        try {
            const response = JSON.parse(xhr.response);
            const feeds = response.data.visionProfilePhotoList.feeds;

            if (feeds.length === 0) {
                updateDiagnosticInfo('<strong style="font-size: 2em;color: blue;">本页全部举报完成</strong><br>');
                callback(output += lastoutput)
                return;
            }

            const ids = feeds.map(feed => feed.photo.id);
            pcursor = response.data.visionProfilePhotoList.pcursor;

            reportPhotos(ids, 0, pcursor);

        } catch (error) {
            console.log('解析返回值时出错:', error);
        }
    };

    xhr.onerror = function() {
        console.log('请求发生错误');
    };

    xhr.send(data);
}

let reportCount = 0; // 添加一个变量用于记录举报次数

function reportPhotos(ids, index, pcursor) {
    if (index >= ids.length) {
        setTimeout(() => fetchPhotos(pcursor), 1);
        return;
    }

    reportCount++
    const photoId = ids[index];
    updateDiagnosticInfo(`开始举报稿件 <span style="color: red; font-weight: bold;">${reportCount}</span>，ID: ${photoId}<br>`);

    const reportData = JSON.stringify({
        'operationName': 'ReportSubmitMutation',
        'variables': {
            'targetId': photoId,
            'reportType': 1,
            'page': 'DETAIL',
            'reportItem': 2,
            'reportDetail': '色情游戏及色情视频剪辑内容', // 举报详情
            'reportedUserId': userId,
            'extraPhotoId': ''
        },
        'query': 'mutation ReportSubmitMutation($targetId: String, $reportType: Int, $page: String, $reportItem: Int, $reportDetail: String, $reportedUserId: String, $extraPhotoId: String) {\n  visionReportSubmit(targetId: $targetId, reportType: $reportType, page: $page, reportItem: $reportItem, reportDetail: $reportDetail, reportedUserId: $reportedUserId, extraPhotoId: $extraPhotoId) {\n    result\n    __typename\n  }\n}\n'
    });

    let reportXhr = new XMLHttpRequest();
    reportXhr.withCredentials = true;
    reportXhr.open('POST', 'https://www.kuaishou.cn/graphql');
    reportXhr.timeout = timeout;

    // 设置请求头
    setHeaders(reportXhr);

    reportXhr.onload = function() {
        const decodedResponse = JSON.parse(reportXhr.response); // 解码响应

        // 使用 JSON.stringify() 将对象转化为字符串，以便正确显示
        updateDiagnosticInfo(`举报请求返回值：<strong>${JSON.stringify(decodedResponse, null, 2).replace(/</g, '&lt;').replace(/>/g, '&gt;')}</strong><br>`);
        lastoutput = `${reportCount}, response: ${reportXhr.response}`
        if (reportCount % 20 === 1) {
            output += `${reportCount}, response: ${reportXhr.response}`;
        }
        if (reportCount  === 80) {
            callback(output += lastoutput);;
        }
        setTimeout(() => {
            reportPhotos(ids, index + 1, pcursor);
        }, delay);
    };

    reportXhr.onerror = function() {
        console.error('举报请求发生错误');
    };
    reportXhr.ontimeout = function() {
        callback(output += lastoutput, '请求超时');
    };
    reportXhr.send(reportData);
}

function setHeaders(xhr) {
    xhr.setRequestHeader('Accept-Language', 'zh-CN,zh;q=0.9'); // 设置接受语言
    xhr.setRequestHeader('Content-Type', 'application/json'); // 设置内容类型
    xhr.setRequestHeader('Accept', '*/*'); // 设置接受任何类型的响应
}


fetchPhotos();
FollowUser();
