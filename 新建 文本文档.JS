const axios = require('axios');
const qs = require('qs');

// 环境变量
const mtTokens = process.env.MTTokenD.split('&');
const mtVersion = process.env.Mt_Version;
const resMap = { "10941": "贵州茅台酒（甲辰龙年）", "10942": "贵州茅台酒（甲辰龙年）x2" };

console.log('拟预约商品：');
console.log(resMap);

async function mtAdd(itemId, shopId, sessionId, userId, token, deviceId) {
    const mtK = `${Date.now()}`;
    const r = await axios.get(`http://82.157.10.108:8086/get_mtv?DeviceID=${deviceId}&MTk=${mtK}&version=${mtVersion}&key=yaohuo`);
    const headers = {
        'User-Agent': 'iPhone 14',
        'MT-Token': token,
        'MT-Network-Type': 'WIFI',
        'MT-User-Tag': '0',
        'MT-R': mt_r,
        'MT-Lat': '',
        'MT-K': mtK,
        'MT-Lng': '',
        'MT-Info': '028e7f96f6369cafe1d105579c5b9377',
        'MT-APP-Version': mtVersion,
        'MT-Request-ID': `${Date.now()}`,
        'Accept-Language': 'zh-Hans-CN;q=1',
        'MT-Device-ID': deviceId,
        'MT-V': r.data,
        'MT-Bundle-ID': 'com.moutai.mall'
    };

    const d = {
        "itemInfoList": [{ "count": 1, "itemId": `${itemId}` }],
        "sessionId": sessionId,
        "userId": `${userId}`,
        "shopId": `${shopId}`
    };

    const actParam = await axios.get(`http://82.157.10.108:8086/get_actParam?key=yaohuo&actParam=${Buffer.from(JSON.stringify(d).replace(/\s+/g, '')).toString('base64')}`);
    d['actParam'] = actParam.data;
    
    const response = await axios.post('https://app.moutai519.com.cn/xhr/front/mall/reservation/add', d, { headers });
    const code = response.data.code || 0;
    if (code === 2000) {
        return response.data.data.successDesc || "未知";
    }
    return `申购失败: ${response.data.message || "未知原因"}`;
}

async function sendNotification(message) {
    const users = process.env.mtec_user.split(',');
    for (const user of users) {
        const url = `http://wxpusher.zjiecode.com/api/send/message/?appToken=&content=${message}&uid=${user}`;
        const response = await axios.get(url);
        console.log(response.data);
    }
}

async function getSessionId(deviceId, token) {
    const headers = {
        'mt-device-id': deviceId,
        'mt-user-tag': '0',
        'accept': '*/*',
        'mt-network-type': 'WIFI',
        'mt-token': token,
        'mt-bundle-id': 'com.moutai.mall',
        'accept-language': 'zh-Hans-CN;q=1',
        'mt-request-id': `${Date.now()}`,
        'mt-app-version': mtVersion,
        'user-agent': 'iPhone 14',
        'mt-r': mt_r,
        'mt-lng': lng,
        'mt-lat': lat
    };

    const response = await axios.get(`https://static.moutai519.com.cn/mt-backend/xhr/front/mall/index/session/get/${time_keys}`, { headers });
    const sessionId = response.data.data.sessionId;
    const itemList = response.data.data.itemList || [];
    const itemCodes = itemList.map(item => item.itemCode);
    return [sessionId, itemCodes];
}

async function getShopItems(sessionId, deviceId, token, province, city) {
    const headers = {
        'mt-device-id': deviceId,
        'mt-user-tag': '0',
        'accept': '*/*',
        'mt-network-type': 'WIFI',
        'mt-token': token,
        'mt-bundle-id': 'com.moutai.mall',
        'accept-language': 'zh-Hans-CN;q=1',
        'mt-request-id': `${Date.now()}`,
        'mt-app-version': mtVersion,
        'user-agent': 'iPhone 14',
        'mt-r': mt_r,
        'mt-lng': lng,
        'mt-lat': lat
    };

    const response = await axios.get(`https://static.moutai519.com.cn/mt-backend/xhr/front/mall/index/session/get/${time_keys}`, { headers });
    const itemList = response.data.data.itemList || [];
    const itemCodeTitleMap = {};
    itemList.forEach(item => {
        itemCodeTitleMap[item.itemCode] = item.title;
    });
    console.log('可预约商品列表：');
    console.log(itemCodeTitleMap);
    return itemCodeTitleMap;
}

async function getShopItem(sessionId, itemId, deviceId, token, province, city) {
    const headers = {
        'mt-device-id': deviceId,
        'mt-user-tag': '0',
        'accept': '*/*',
        'mt-network-type': 'WIFI',
        'mt-token': token,
        'mt-bundle-id': 'com.moutai.mall',
        'accept-language': 'zh-Hans-CN;q=1',
        'mt-request-id': `${Date.now()}`,
        'mt-app-version': mtVersion,
        'user-agent': 'iPhone 14',
        'mt-r': mt_r,
        'mt-lng': lng,
        'mt-lat': lat
    };

    const response = await axios.get(`https://static.moutai519.com.cn/mt-backend/xhr/front/mall/shop/list/slim/v3/${sessionId}/${province}/${itemId}/${time_keys}`, { headers });
    const shops = response.data.data.shops || [];
    const shopId_ = p_c_map[province][city];
    for (const shop of shops) {
        if (shopId_.includes(shop.shopId) && itemId.toString() in shop) {
            return shop.shopId;
        }
    }
}

async function getUserId(token, deviceId) {
    const headers = {
        'MT-User-Tag': '0',
        'Accept': '*/*',
        'MT-Network-Type': 'WIFI',
        'MT-Token': token,
        'MT-Bundle-ID': 'com.moutai.mall',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'MT-Request-ID': `${Date.now()}`,
        'MT-APP-Version': mtVersion,
        'User-Agent': 'iOS;16.0.1;Apple;iPhone 14 ProMax',
        'MT-R': mt_r,
        'MT-Device-ID': deviceId,
        'mt-lng': lng,
        'mt-lat': lat
    };

    const response = await axios.get('https://app.moutai519.com.cn/xhr/front/user/info', { headers });
    const userName = response.data.data.userName;
    const userId = response.data.data.userId;
    const mobile = response.data.data.mobile;
    return [userName, userId, mobile];
}

async function getUserEnergyAward(deviceId, ck) {
    const cookies = {
        'MT-Device-ID-Wap': deviceId,
        'MT-Token-Wap': ck,
        'YX_SUPPORT_WEBP': '1'
    };

    const headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_2_1 like Mac OS X)',
        'Referer': 'https://h5.moutai519.com.cn/gux/game/main?appConfig=2_1_2',
        'Client-User-Agent': 'iOS;15.0.1;Apple;iPhone 12 ProMax',
        'MT-R': mt_r,
        'Origin': 'https://h5.moutai519.com.cn',
        'MT-APP-Version': mtVersion,
        'MT-Request-ID': `${Date.now()}`,
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'MT-Device-ID': deviceId,
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'mt-lng': lng,
        'mt-lat': lat
    };

    const response = await axios.post('https://h5.moutai519.com.cn/game/isolationPage/getUserEnergyAward', {}, { headers, cookies });
    return response.data.message.includes('无法领取奖励') ? response.data.message : "领取奖励成功";
}

async function getMap() {
    const url = 'https://static.moutai519.com