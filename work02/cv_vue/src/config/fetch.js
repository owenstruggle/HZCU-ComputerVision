import {baseUrl} from './env'

export default async (url = '', data = {}, type = 'GET', method = 'fetch') => {
    type = type.toUpperCase();
    url = baseUrl + url;

    // 此处规定get请求的参数使用时放在data中，如同post请求
    if (type === 'GET') {
        let dataStr = ''; // 数据拼接字符串
        Object.keys(data).forEach(key => {
            dataStr += key + '=' + data[key] + '&';
        })

        if (dataStr !== '') {
            dataStr = dataStr.substr(0, dataStr.lastIndexOf('&'));
            url = url + '?' + dataStr;
        }
    }

    // 对于支持fetch方法的浏览器，处理如下：
    if (window.fetch && method === 'fetch') {
        let requestConfig = {
            // fetch默认不会带cookie，需要添加配置项credentials允许携带cookie
            credentials: 'include',
            method: type,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            mode: "cors",  // 以CORS的形式跨域
            // cache: "force-cache"
            cache: "no-cache"	// 无缓存
        }

        // 添加了 PUT 方法的打包请求体操作
        if (type === 'POST' || type === 'PUT') {
            Object.defineProperty(requestConfig, 'body', {
                value: JSON.stringify(data)
            })
        }

        try {
            const response = await fetch(url, requestConfig);
            return await response.json()
        } catch (error) {
            throw new Error(error)
        }
    } else {
        // 对于不支持fetch的浏览器，便自动使用 ajax + promise
        return new Promise((resolve, reject) => {
            let requestObj;
            if (window.XMLHttpRequest) {
                requestObj = new XMLHttpRequest();
            } else {
                // 忽略下一行的代码警告
                // eslint-disable-next-line
                requestObj = new ActiveXObject;  // 兼容IE
            }

            let sendData = '';
            if (type === 'POST') {
                sendData = JSON.stringify(data);
            }

            requestObj.open(type, url, true);
            requestObj.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            requestObj.send(sendData);

            requestObj.onreadystatechange = () => {
                if (requestObj.readyState === 4) {
                    if (requestObj.status === 200) {
                        let obj = requestObj.response
                        if (typeof obj !== 'object') {
                            obj = JSON.parse(obj);
                        }
                        resolve(obj)
                    } else {
                        reject(requestObj)
                    }
                }
            }
        })
    }
}