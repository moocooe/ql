# 自用脚本 for 青龙面板
青龙环境变量
环境变量请使用环境变量列表直接添加，不要使用 export xxx="" 这种方式添加环境变量。

SMZDM_COOKIE: 抓包抓到的 Cookie 内容，需要所有 Cookie 内容，多用户可以用 & 分隔，或者使用多个同名环境变量。
SMZDM_SK: 这个值是可选值，会自动计算，如果你一定想用自己的，可以抓取，是从安卓 App 的 https://user-api.smzdm.com/checkin 请求参数中抓包抓到的，多用户可以用 & 分隔，或者使用多个同名环境变量，顺序要保持与 SMZDM_COOKIE 多用户顺序一致。
SMZDM_USER_AGENT_APP: 这个值是可选值，是指 APP 的 User-Agent，从 APP 的 API 请求头中抓包得到，建议抓取 Android 的 User-Agent，不填使用脚本默认值。
SMZDM_USER_AGENT_WEB: 这个值是可选值，是指 APP 中访问网页的 User-Agent，一般在 APP 内的转盘网页中抓包得到，建议抓取 Android 的 User-Agent，不填使用脚本默认值。
SMZDM_COMMENT: 如果要完成评论文章的任务请设置这个环境变量，环境变量的内容是评论的文案，文案要大于 10 个汉字，建议用比较个性化的文案，脚本发布评论后会删除这条评论，但是为防止删除失败的情况，请尽量用好一点的文案，防止被判定为恶意灌水。
SMZDM_CROWD_SILVER_5: 每日抽奖任务默认只进行免费抽奖，如要进行 5 碎银子的抽奖，请设置这个环境变量的值为 yes。
SMZDM_CROWD_KEYWORD: 抽奖关键词，执行非免费抽奖时，会优先选择包含此关键词的抽奖，如果未找到包含此关键词的抽奖，则会随机选择一个。
SMZDM_TASK_TESTING: 是否运行全民众测能量值任务，如要运行此任务，请设置这个环境变量的值为 yes，否则不运行。
