/**
 * new Env("云闪付签到");
 * cron "5 8 * * *" script-path=ysfqd.js, tag=云闪付签到
 * 脚本的路径和标签
 * 变量名: ysfqd_data
 * 多账户用 @ 或换行分隔
 * 变量值: ej...xx
 * 通过在https://youhui.95516.com/newsign/api获取Authorization头部，不需要Bearer，只要其后的值
 */

const $ = new Env("云闪付签到");
const ckName = "ysfqd_data";
const Notify = 1; // 0为关闭通知,1为打开通知,默认为1
let envSplitor = ["@", "\n"]; // 多账号分隔符
let strSplitor = '&'; // 单账号多变量分隔符

let scriptVersionNow = "0.0.1";

let msg = "";

async function start() {
    await getVersion("smallfawn/QLScriptPublic@main/ysfqd.js");
    await getNotice();
    $.DoubleLog(`---------------------------`);
    let taskall = [];
    for (let user of $.userList) {
        taskall.push(await user.sign());
        await $.wait(1000);
    }
    await Promise.all(taskall);
}

class UserInfo {
    constructor(str) {
        this.index = ++$.userIdx;
        this.ck = str.split(strSplitor)[0]; // 单账号多变量分隔符
        this.ckStatus = true;
    }

    async sign() {
        try {
            let options = {
                method: 'POST',
                url: 'https://youhui.95516.com/newsign/api/daily_sign_in',
                headers: {
                    'Accept': '*/*',
                    'Authorization': `Bearer ${this.ck}`,
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 /sa-sdk-ios/sensors-verify/analytics.95516.com?production   (com.unionpay.chsp) (cordova 4.5.4) (updebug 0) (version 929) (UnionPay/1.0 CloudPay) (clientVersion 189) (language zh_CN) (upHtml) (walletMode 00) ',
                    'Connection': 'keep-alive',
                },
            }, result = await httpRequest(options);
            if ('signedIn' in result) {
                $.DoubleLog(`账号[${this.index}]  今天是第${result["signInDays"]["current"]["days"]}天签到 今日已签到成功,目前已连续签到${result["signInDays"]["days"]}天🎉`);
            } else {
                $.DoubleLog(`账号[${this.index}]  用户查询:失败 ❌ 了呢,原因未知！`);
            }
        } catch (e) {
            console.log(e);
        }
    }
}

!(async () => {
    if (!(await checkEnv())) return;
    if ($.userList.length > 0) {
        await start();
    }
    await $.SendMsg(msg);
})().catch((e) => console.log(e)).finally(() => $.done());

async function checkEnv() {
    let userCookie = ($.isNode() ? process.env[ckName] : $.getdata(ckName)) || "";
    if (userCookie) {
        let e = envSplitor[0];
        for (let o of envSplitor)
            if (userCookie.indexOf(o) > -1) {
                e = o;
                break;
            }
        for (let n of userCookie.split(e)) n && $.userList.push(new UserInfo(n));
    } else {
        console.log("未找到CK");
        $.msg($.name, '【提示】⚠️', 'Can not find any scripts');
        return;
    }
    if ($.userList.length === 0) {
        $.msg($.name, '【提示】⚠️', 'Can not find any scripts');
    }
    return console.log(`共找到${$.userList.length}个账号`), true;
}

function httpRequest(options, method = null) {
    method = options.method ? options.method.toLowerCase() : options.body ? "post" : "get";
    return new Promise((resolve) => {
        $[method](options, (err, resp, data) => {
            if (err) {
                console.log(`${method}请求失败`);
                $.logErr(err);
            } else {
                if (data) {
                    try { data = JSON.parse(data); } catch (error) { }
                    resolve(data);
                } else {
                    console.log(`请求api返回数据为空，请检查自身原因`);
                }
            }
            resolve();
        });
    });
}

function getVersion(scriptUrl, timeout = 3 * 1000) {
    return new Promise((resolve) => {
        const options = { url: `https://fastly.jsdelivr.net/gh/${scriptUrl}` };
        $.get(options, (err, resp, data) => {
            try {
                const regex = /scriptVersionNow\s*=\s*(["'`])([\d.]+)\1/;
                const match = data.match(regex);
                const scriptVersionLatest = match ? match[2] : "";
                console.log(`\n====== 当前版本：${scriptVersionNow} 📌 最新版本：${scriptVersionLatest} ======`);
            } catch (e) {
                $.logErr(e, resp);
            }
            resolve();
        }, timeout);
    });
}

async function getNotice() {
    try {
        const urls = [
            "https://fastly.jsdelivr.net/gh/smallfawn/Note@main/Notice.json",
            "https://gcore.jsdelivr.net/gh/smallfawn/Note@main/Notice.json",
            "https://cdn.jsdelivr.net/gh/smallfawn/Note@main/Notice.json",
            "https://ghproxy.com/https://raw.githubusercontent.com/smallfawn/Note/main/Notice.json",
            "https://gitee.com/smallfawn/Note/raw/master/Notice.json",
        ];
        let notice = null;
        for (const url of urls) {
            const options = { url, headers: { "User-Agent": "" } };
            const result = await httpRequest(options);
            if (result && "notice" in result) {
                notice = result.notice.replace(/\\n/g, "\n");
                break;
            }
        }
        if (notice) { $.DoubleLog(notice); }
    } catch (e) {
        console.log(e);
    }
}

function Env(t, e) { class s { constructor(t) { this.env = t } send(t, e = "GET") { t = "string" == typeof t ? { url: t } : t; let s = this.get; return ("POST" === e && (s = this.post), new Promise((e, a) => { s.call(this, t, (t, s, r) => { t ? a(t) : e(s) }) })) } get(t) { return this.send.call(this.env, t) } post(t) { return this.send.call(this.env, t, "POST") } } return new (class { constructor(t, e) { this.userList = []; this.userIdx = 0; (this.name = t), (this.http = new s(this)), (this.data = null), (this.dataFile = "box.dat"), (this.logs = []), (this.isMute = !1), (this.isNeedRewrite = !1), (this.logSeparator = "\n"), (this.encoding = "utf-8"), (this.startTime = new Date().getTime()), Object.assign(this, e), this.log("", `🔔${this.name},开始!`) } getEnv() { return "undefined" != typeof $environment && $environment["surge-version"] ? "Surge" : "undefined" != typeof $environment && $environment["stash-version"] ? "Stash" : "undefined" != typeof module && module.exports ? "Node.js" : "undefined" != typeof $task ? "Quantumult X" : "undefined" != typeof $loon ? "Loon" : "undefined" != typeof $rocket ? "Shadowrocket" : void 0 } isNode() { return "Node.js" === this.getEnv() } isQuanX() { return "Quantumult X" === this.getEnv() } isSurge() { return "Surge" === this.getEnv() } isLoon() { return "Loon" === this.getEnv() } isShadowrocket() { return "Shadowrocket" === this.getEnv() } isStash() { return "Stash" === this.getEnv() } toObj(t, e = null) { try { return JSON.parse(t) } catch { return e } } toStr(t, e = null) { try { return JSON.stringify(t) } catch { return e } } getjson(t, e) { let s = e; const a = this.getdata(t); if (a) try { s = JSON.parse(this.getdata(t)) } catch { }