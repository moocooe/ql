
# cron: 11 6,9,12,15,18 * * *
# const $ = new Env("˳������");
import hashlib
import json
import os
import random
import time
import re
from datetime import datetime, timedelta
from sys import exit
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
# from sendNotify import send
from urllib.parse import unquote

os.environ['NEW_VAR'] ='sfsyUrl'

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


#IS_DEV = False
IS_DEV = True

send_msg = ''
one_msg = ''

def Log(cont=''):
    global send_msg, one_msg
    print(cont)
    if cont:
        one_msg += f'{cont}\n'
        send_msg += f'{cont}\n'
        
inviteId = ['']

def sunquote(sfurl):
    decode = unquote(sfurl)
    if "3A//" in decode:
        decode = unquote(decode)
    return decode

class RUN:
    def __init__(self, info, index):
        global one_msg
        one_msg = ''
        split_info = info.split('@')
        url = split_info[0]
        len_split_info = len(split_info)
        last_info = split_info[len_split_info - 1]
        self.send_UID = None
        self.all_logs = []
        if len_split_info > 0 and "UID_" in last_info:
            self.send_UID = last_info
        self.index = index + 1
        Log(f"\n---------��ʼִ�е�{self.index}���˺�>>>>>")
        self.s = requests.session()
        self.s.verify = False
        self.headers = {
            'Host': 'mcs-mimp-web.sf-express.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090551) XWEB/6945 Flue',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh',
            'platform': 'MINI_PROGRAM',

        }
        self.anniversary_black = False
        self.member_day_black = False
        self.member_day_red_packet_drew_today = False
        self.member_day_red_packet_map = {}
        self.login_res = self.login(url)
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.answer = False
        self.max_level = 8
        self.packet_threshold = 1 << (self.max_level - 1)

    def get_deviceId(self, characters='abcdef0123456789'):
        result = ''
        for char in 'xxxxxxxx-xxxx-xxxx':
            if char == 'x':
                result += random.choice(characters)
            elif char == 'X':
                result += random.choice(characters).upper()
            else:
                result += char
        return result

    def encode_url(self,url):
        if '%' in url:
            return url  
        base_url, params = url.split('?', 1)
        encoded_params = urllib.parse.quote(params, safe='&=')
        encoded_url = f"{base_url}?{encoded_params}"
        return encoded_url
    def login(self, sfurl):
        sfurl2=self.encode_url(sfurl)
        ress = self.s.get(sfurl2, headers=self.headers)
        # print(ress.text)
        self.user_id = self.s.cookies.get_dict().get('_login_user_id_', '')
        self.phone = self.s.cookies.get_dict().get('_login_mobile_', '')
        self.mobile = self.phone[:3] + "*" * 4 + self.phone[7:]
        if self.phone != '':
            Log(f'�û�:��{self.mobile}����½�ɹ�')
            return True
        else:
            Log(f'��ȡ�û���Ϣʧ��')
            return False

    def getSign(self):
        timestamp = str(int(round(time.time() * 1000)))
        token = 'wwesldfs29aniversaryvdld29'
        sysCode = 'MCS-MIMP-CORE'
        data = f'token={token}&timestamp={timestamp}&sysCode={sysCode}'
        signature = hashlib.md5(data.encode()).hexdigest()
        data = {
            'sysCode': sysCode,
            'timestamp': timestamp,
            'signature': signature
        }
        self.headers.update(data)
        return data
    def do_request(self, url, data={}, req_type='post'):
        try:
            if req_type.lower() == 'get':
                response = self.s.get(url, headers=self.headers)
            elif req_type.lower() == 'post':
                response = self.s.post(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Invalid request type: {req_type}")

            try:
                res = response.json()
            except json.JSONDecodeError:
                Log(f"JSON ����ʧ�ܣ���Ӧ����: {response.text}")
                return {"success": False, "errorMessage": "JSON ����ʧ��"}

            return res
        except requests.exceptions.RequestException as e:
            Log(f"��������ʧ��: {e}")
            return {"success": False, "errorMessage": "��������ʧ��"}
        except Exception as e:
            Log(f"δ֪����: {e}")
            return {"success": False, "errorMessage": "δ֪����"}

    def sign(self):
        print(f'>>>>>>��ʼִ��ǩ��')
        json_data = {"comeFrom": "vioin", "channelFrom": "WEIXIN"}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~automaticSignFetchPackage'
        url2 ='https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~queryPointSignAwardList'
        url3 ='https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskSignPlusService~getUnFetchPointAndDiscount'
        result = self.do_request(url2, data={"channelType": "1"})
        result2=self.do_request(url3, data={})
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            count_day = response.get('obj', {}).get('countDay', 0)
            if response.get('obj') and response['obj'].get('integralTaskSignPackageVOList'):
                packet_name = response["obj"]["integralTaskSignPackageVOList"][0]["packetName"]
                Log(f'>>>ǩ���ɹ�����á�{packet_name}���������ۼ�ǩ����{count_day + 1}����')
            else:
                Log(f'������ǩ���������ۼ�ǩ����{count_day + 1}����')
        else:
            print(f'ǩ��ʧ�ܣ�ԭ��{response.get("errorMessage")}')

    def superWelfare_receiveRedPacket(self):
        print(f'>>>>>>��ֵ����ǩ��')
        json_data = {
            'channel': 'czflqdlhbxcx'
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberActLengthy~redPacketActivityService~superWelfare~receiveRedPacket'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            gift_list = response.get('obj', {}).get('giftList', [])
            if response.get('obj', {}).get('extraGiftList', []):
                gift_list.extend(response['obj']['extraGiftList'])
            gift_names = ', '.join([gift['giftName'] for gift in gift_list])
            receive_status = response.get('obj', {}).get('receiveStatus')
            status_message = '��ȡ�ɹ�' if receive_status == 1 else '����ȡ��'
            Log(f'��ֵ����ǩ��[{status_message}]: {gift_names}')
        else:
            error_message = response.get('errorMessage') or json.dumps(response) or '�޷���'
            print(f'��ֵ����ǩ��ʧ��: {error_message}')



    def get_SignTaskList(self, END=False):
        if not END: print(f'>>>��ʼ��ȡǩ�������б�')
        json_data = {
            'channelType': '3',
            'deviceId': self.get_deviceId(),
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~queryPointTaskAndSignFromES'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True and response.get('obj') != []:
            totalPoint = response["obj"]["totalPoint"]
            if END:
                Log(f'��ǰ���֣���{totalPoint}��')
                return
            Log(f'ִ��ǰ���֣���{totalPoint}��')
            for task in response["obj"]["taskTitleLevels"]:
                self.taskId = task["taskId"]
                self.taskCode = task["taskCode"]
                self.strategyId = task["strategyId"]
                self.title = task["title"]
                status = task["status"]
                skip_title = ['����ҵģ��ļ��µ�', 'ȥ����һ���ռ�ƫ��', '������ֻ']
                if status == 3:
                    print(f'>{self.title}-�����')
                    continue
                if self.title in skip_title:
                    print(f'>{self.title}-����')
                    continue
                if self.title =='������������Ȩ����':
                    json_data = {
                        "memGrade": 2,
                        "categoryCode": "SHTQ",
                        "showCode": "SHTQWNTJ"
                    }
                    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~mallGoodsLifeService~list'
                    response = self.do_request(url, data=json_data)
                    if response.get('success') == True:
                        goodsList = response["obj"][0]["goodsList"]
                        for goods in goodsList:
                            exchangeTimesLimit = goods['exchangeTimesLimit']
                            if exchangeTimesLimit >= 1:
                                self.goodsNo = goods['goodsNo']
                                print(f'��ȡ����Ȩ�棺��ǰѡ��ȯ�ţ�{self.goodsNo}')
                                self.get_coupom()
                                break
                    else:
                        print(f'>��ȯʧ�ܣ�ԭ��{response.get("errorMessage")}')
                else:
                    self.doTask()
                    time.sleep(3)
                self.receiveTask()

    def doTask(self):
        print(f'>>>��ʼȥ��ɡ�{self.title}������')
        json_data = {
            'taskCode': self.taskCode,
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonRoutePost/memberEs/taskRecord/finishTask'

        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'>��{self.title}������-�����')
        else:

            print(f'>��{self.title}������-{response.get("errorMessage")} 1{response}')

    def receiveTask(self):
        print(f'>>>��ʼ��ȡ��{self.title}��������')
        json_data = {
            "strategyId": self.strategyId,
            "taskId": self.taskId,
            "taskCode": self.taskCode,
            "deviceId": self.get_deviceId()
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~fetchIntegral'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'>��{self.title}����������ȡ�ɹ���')
        else:
            print(f'>��{self.title}������-{response.get("errorMessage")}')

    def do_honeyTask(self):
        json_data = {"taskCode": self.taskCode}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'>��{self.taskType}������-�����')
        else:
            print(f'>��{self.taskType}������-{response.get("errorMessage")}')

    def receive_honeyTask(self):
        print('>>>ִ����ȡ��������')
        self.headers['syscode'] = 'MCS-MIMP-CORE'
        self.headers['channel'] = 'wxwdsj'
        self.headers['accept'] = 'application/json, text/plain, */*'
        self.headers['content-type'] = 'application/json;charset=UTF-8'
        self.headers['platform'] = 'MINI_PROGRAM'
        json_data = {"taskType": self.taskType}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~receiveHoney'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'��ȡ����{self.taskType}���ɹ���')
        else:
            print(f'��ȡ����{self.taskType}��ʧ�ܣ�ԭ��{response.get("errorMessage")}')

    def get_coupom(self):
        print('>>>ִ����ȡ����Ȩ����ȯ����')

        json_data = {
            "from": "Point_Mall",
            "orderSource": "POINT_MALL_EXCHANGE",
            "goodsNo": self.goodsNo,
            "quantity": 1,
            "taskCode": self.taskCode
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~pointMallService~createOrder'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'>��ȯ�ɹ���')
        else:
            print(f'>��ȯʧ�ܣ�ԭ��{response.get("errorMessage")}')

    def get_coupom_list(self):
        print('>>>��ȡ����Ȩ��ȯ�б�')

        json_data = {
            "memGrade": 1,
            "categoryCode": "SHTQ",
            "showCode": "SHTQWNTJ"
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberGoods~mallGoodsLifeService~list'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            goodsList = response["obj"][0]["goodsList"]
            for goods in goodsList:
                exchangeTimesLimit = goods['exchangeTimesLimit']
                if exchangeTimesLimit >= 1:
                    self.goodsNo = goods['goodsNo']
                    print(f'��ǰѡ��ȯ�ţ�{self.goodsNo}')
                    self.get_coupom()
                    break
        else:
            print(f'>��ȯʧ�ܣ�ԭ��{response.get("errorMessage")}')

    def get_honeyTaskListStart(self):
        print('>>>��ʼ��ȡ���ۻ����������б�')
        json_data = {}
        self.headers['channel'] = 'wxwdsj'
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~taskDetail'

        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            for item in response["obj"]["list"]:
                self.taskType = item["taskType"]
                status = item["status"]
                if status == 3:
                    print(f'>��{self.taskType}��-�����')
                    if self.taskType == 'BEES_GAME_TASK_TYPE':
                        self.bee_need_help = False
                    continue
                if "taskCode" in item:
                    self.taskCode = item["taskCode"]
                    if self.taskType == 'DAILY_VIP_TASK_TYPE':
                        self.get_coupom_list()
                    else:
                        self.do_honeyTask()
                if self.taskType == 'BEES_GAME_TASK_TYPE':
                    self.honey_damaoxian()
                time.sleep(2)

    def honey_damaoxian(self):
        print('>>>ִ�д�ð������')
        gameNum = 5
        for i in range(1, gameNum):
            json_data = {
                'gatherHoney': 20,
            }
            if gameNum < 0: break
            print(f'>>��ʼ��{i}�δ�ð��')
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeGameService~gameReport'
            response = self.do_request(url, data=json_data)
            stu = response.get('success')
            if stu:
                gameNum = response.get('obj')['gameNum']
                print(f'>��ð�ճɹ���ʣ�������{gameNum}��')
                time.sleep(2)
                gameNum -= 1
            elif response.get("errorMessage") == '��������':
                print(f'> ��Ҫ����')
                self.honey_expand()
            else:
                print(f'>��ð��ʧ�ܣ���{response.get("errorMessage")}��')
                break

    def honey_expand(self):
        print('>>>��������')
        gameNum = 5

        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~expand'
        response = self.do_request(url, data={})
        stu = response.get('success', False)
        if stu:
            obj = response.get('obj')
            print(f'>�ɹ����ݡ�{obj}������')
        else:
            print(f'>����ʧ�ܣ���{response.get("errorMessage")}��')

    def honey_indexData(self, END=False):
        if not END: print('\n>>>>>>>��ʼִ�в��ۻ���������')
        random_invite = random.choice([invite for invite in inviteId if invite != self.user_id])
        self.headers['channel'] = 'wxwdsj'
        json_data = {"inviteUserId": random_invite}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~receiveExchangeIndexService~indexData'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            usableHoney = response.get('obj').get('usableHoney')
            if END:
                Log(f'��ǰ���ۣ���{usableHoney}��')
                return
            Log(f'ִ��ǰ���ۣ���{usableHoney}��')
            taskDetail = response.get('obj').get('taskDetail')
            activityEndTime = response.get('obj').get('activityEndTime', '')
            activity_end_time = datetime.strptime(activityEndTime, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()

            if current_time.date() == activity_end_time.date():
                Log("���ڻ���ս������뼰ʱ�һ�")
            else:
                print(f'���ڻ����ʱ�䡾{activityEndTime}��')

            if taskDetail != []:
                for task in taskDetail:
                    self.taskType = task['type']
                    self.receive_honeyTask()
                    time.sleep(2)

    def EAR_END_2023_TaskList(self):
        print('\n>>>>>>��ʼ���ռ�������')
        json_data = {
            "activityCode": "YEAR_END_2023",
            "channelType": "MINI_PROGRAM"
        }
        self.headers['channel'] = 'xcx23nz'
        self.headers['platform'] = 'MINI_PROGRAM'
        self.headers['syscode'] = 'MCS-MIMP-CORE'

        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'

        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            for item in response["obj"]:
                self.title = item["taskName"]
                self.taskType = item["taskType"]
                status = item["status"]
                if status == 3:
                    print(f'>��{self.taskType}��-�����')
                    continue
                if self.taskType == 'INTEGRAL_EXCHANGE':
                    self.EAR_END_2023_ExchangeCard()
                elif self.taskType == 'CLICK_MY_SETTING':
                    self.taskCode = item["taskCode"]
                    self.addDeliverPrefer()
                if "taskCode" in item:
                    self.taskCode = item["taskCode"]
                    self.doTask()
                    time.sleep(3)
                    self.EAR_END_2023_receiveTask()
                else:
                    print(f'��ʱ��֧�֡�{self.title}������')
        self.EAR_END_2023_getAward()
        self.EAR_END_2023_GuessIdiom()

    def addDeliverPrefer(self):
        print(f'>>>��ʼ��{self.title}������')
        json_data = {
            "country": "�й�",
            "countryCode": "A000086000",
            "province": "������",
            "provinceCode": "A110000000",
            "city": "������",
            "cityCode": "A111000000",
            "county": "������",
            "countyCode": "A110101000",
            "address": "1��¥1��Ԫ101",
            "latitude": "",
            "longitude": "",
            "memberId": "",
            "locationCode": "010",
            "zoneCode": "CN",
            "postCode": "",
            "takeWay": "7",
            "callBeforeDelivery": 'false',
            "deliverTag": "2,3,4,1",
            "deliverTagContent": "",
            "startDeliverTime": "",
            "selectCollection": 'false',
            "serviceName": "",
            "serviceCode": "",
            "serviceType": "",
            "serviceAddress": "",
            "serviceDistance": "",
            "serviceTime": "",
            "serviceTelephone": "",
            "channelCode": "RW11111",
            "taskId": self.taskId,
            "extJson": "{\"noDeliverDetail\":[]}"
        }
        url = 'https://ucmp.sf-express.com/cx-wechat-member/member/deliveryPreference/addDeliverPrefer'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print('����һ���ռ�ƫ�ã��ɹ�')
        else:
            print(f'>��{self.title}������-{response.get("errorMessage")}')

    def Exchangee_2025(self):
        json_data = {
            "exchangeNum": 1,
            "activityCode": "DISNEY2"
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2025TaskService~integralExchange'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'> ���һ�γ齱����')
        else:
            print(f'>�����ֶһ�����������-{response.get("errorMessage")}')

    def EAR_END_2023_getAward(self):
        print(f'>>>��ʼ�鿨')
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~yearEnd2023GardenPartyService~getAward'
        for l in range(10):
            for i in range(0, 3):
                json_data = {
                    "cardType": i
                }
                response = self.do_request(url, data=json_data)
                if response.get('success') == True:
                    receivedAccountList = response['obj']['receivedAccountList']
                    for card in receivedAccountList:
                        print(f'>��ã���{card["currency"]}������{card["amount"]}���ţ�')
                elif response.get('errorMessage') == '�ﵽ������ֵ�����Ժ�����':
                    break
                elif response.get('errorMessage') == '�û���ϢʧЧ�����˳����½���':
                    break
                else:
                    print(f'>�鿨ʧ�ܣ�{response.get("errorMessage")}')
                time.sleep(3)
    def ifLogin(self):
        response = self.do_request('https://mcs-mimp-web.sf-express.com/mcs-mimp/ifLogin')
        # print(response)
    def game202505(self):
        self.headers['channel']='25dwappty'
        response = self.do_request("https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoatGame2025Service~init")
        if response.get("obj",{}).get("alreadyDayPass",True):
            print(f'����������Ϸ�����')
        else:
            print(f'>>>��ʼ������')
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoatGame2025Service~win'
            for i in range(1, 5):
                json_data = {
                    "levelIndex": i
                }
                response = self.do_request(url, data=json_data)
                if response.get('success') == True:
                    print(f'��{i}�سɹ���')
                else:
                    print(f'��{i}��ʧ�ܣ�')

    def EAR_END_2023_receiveTask(self):
        print(f'>>>��ʼ��ȡ��{self.title}��������')
        json_data = {
            "taskType": self.taskType,
            "activityCode": "YEAR_END_2023",
            "channelType": "MINI_PROGRAM"
        }
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonNoLoginPost/~memberNonactivity~yearEnd2023TaskService~fetchMixTaskReward'
        response = self.do_request(url, data=json_data)
        if response.get('success') == True:
            print(f'>��{self.title}����������ȡ�ɹ���')
        else:
            print(f'>��{self.title}������-{response.get("errorMessage")}')

    def anniversary2024_weekly_gift_status(self):
        print(f'\n>>>>>>>��ʼ����������')
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024IndexService~weeklyGiftStatus'
        response = self.do_request(url)
        if response.get('success') == True:
            weekly_gift_list = response.get('obj', {}).get('weeklyGiftList', [])
            for weekly_gift in weekly_gift_list:
                if not weekly_gift.get('received'):
                    receive_start_time = datetime.strptime(weekly_gift['receiveStartTime'], '%Y-%m-%d %H:%M:%S')
                    receive_end_time = datetime.strptime(weekly_gift['receiveEndTime'], '%Y-%m-%d %H:%M:%S')
                    current_time = datetime.now()
                    if receive_start_time <= current_time <= receive_end_time:
                        self.anniversary2024_receive_weekly_gift()
        else:
            error_message = response.get('errorMessage') or json.dumps(response) or '�޷���'
            print(f'��ѯÿ����ȯʧ��: {error_message}')
            if 'ϵͳ��æ' in error_message or '�û��ֻ���У��δͨ��' in error_message:
                self.anniversary_black = True

    def anniversary2024_receive_weekly_gift(self):
        print(f'>>>��ʼ��ȡÿ����ȯ')
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024IndexService~receiveWeeklyGift'
        response = self.do_request(url)
        if response.get('success'):
            product_names = [product['productName'] for product in response.get('obj', [])]
            print(f'ÿ����ȯ: {product_names}')
        else:
            error_message = response.get('errorMessage') or json.dumps(response) or '�޷���'
            print(f'ÿ����ȯʧ��: {error_message}')
            if 'ϵͳ��æ' in error_message or '�û��ֻ���У��δͨ��' in error_message:
                self.anniversary_black = True

    def anniversary2024_taskList(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'
        data = {
            'activityCode': 'ANNIVERSARY_2024',
            'channelType': 'MINI_PROGRAM'
        }
        response = self.do_request(url, data)
        if response and response.get('success'):
            tasks = response.get('obj', [])
            for task in filter(lambda x: x['status'] == 1, tasks):
                if self.anniversary_black:
                    return
                for _ in range(task['canReceiveTokenNum']):
                    self.anniversary2024_fetchMixTaskReward(task)
            for task in filter(lambda x: x['status'] == 2, tasks):
                if self.anniversary_black:
                    return
                if task['taskType'] in ['PLAY_ACTIVITY_GAME', 'PLAY_HAPPY_ELIMINATION', 'PARTAKE_SUBJECT_GAME']:
                    pass
                elif task['taskType'] == 'FOLLOW_SFZHUNONG_VEDIO_ID':
                    pass
                elif task['taskType'] in ['BROWSE_VIP_CENTER', 'GUESS_GAME_TIP', 'CREATE_SFID', 'CLICK_MY_SETTING',
                                          'CLICK_TEMPLATE', 'REAL_NAME', 'SEND_SUCCESS_RECALL', 'OPEN_SVIP',
                                          'OPEN_FAST_CARD', 'FIRST_CHARGE_NEW_EXPRESS_CARD', 'CHARGE_NEW_EXPRESS_CARD',
                                          'INTEGRAL_EXCHANGE']:
                    pass
                else:
                    for _ in range(task['restFinishTime']):
                        if self.anniversary_black:
                            break
                        self.anniversary2024_finishTask(task)

    def anniversary2024_finishTask(self, task):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonRoutePost/memberEs/taskRecord/finishTask'
        data = {'taskCode': task['taskCode']}
        response = self.do_request(url, data)
        if response and response.get('success'):
            print('�������[%s]�ɹ�' % task['taskName'])
            self.anniversary2024_fetchMixTaskReward(task)
        else:
            print('�������[%s]ʧ��: %s' % (
                task['taskName'], response.get('errorMessage') or (json.dumps(response) if response else '�޷���')))

    def anniversary2024_fetchMixTaskReward(self, task):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024TaskService~fetchMixTaskReward'
        data = {
            'taskType': task['taskType'],
            'activityCode': 'ANNIVERSARY_2024',
            'channelType': 'MINI_PROGRAM'
        }
        response = self.do_request(url, data)
        if response and response.get('success'):
            reward_info = response.get('obj', {}).get('account', {})
            received_list = [f"[{item['currency']}]X{item['amount']}" for item in
                             reward_info.get('receivedAccountList', [])]
            turned_award = reward_info.get('turnedAward', {})
            if turned_award.get('productName'):
                received_list.append(f"[�Ż�ȯ]{turned_award['productName']}")
            print('��ȡ����[%s]����: %s' % (task['taskName'], ', '.join(received_list)))
        else:
            error_message = response.get('errorMessage') or json.dumps(response) or '�޷���'
            print('��ȡ����[%s]����ʧ��: %s' % (task['taskName'], error_message))
            if '�û��ֻ���У��δͨ��' in error_message:
                self.anniversary_black = True

    def anniversary2024_unbox(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024CardService~unbox'
        response = self.do_request(url, {})
        if response and response.get('success'):
            account_info = response.get('obj', {}).get('account', {})
            unbox_list = [f"[{item['currency']}]X{item['amount']}" for item in
                          account_info.get('receivedAccountList', [])]
            print('�����: %s' % ', '.join(unbox_list) or '����')
        else:
            error_message = response.get('errorMessage') or json.dumps(response) or '�޷���'
            print('�����ʧ��: %s' % error_message)
            if '�û��ֻ���У��δͨ��' in error_message:
                self.anniversary_black = True

    def anniversary2024_game_list(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024GameParkService~list'
        response = self.do_request(url, {})
        try:
            if response['success']:
                topic_pk_info = response['obj'].get('topicPKInfo', {})
                search_word_info = response['obj'].get('searchWordInfo', {})
                happy_elimination_info = response['obj'].get('happyEliminationInfo', {})

                if not topic_pk_info.get('isPassFlag'):
                    print('��ʼ����PK��')
                    self.anniversary2024_TopicPk_topicList()

                if not search_word_info.get('isPassFlag') or not search_word_info.get('isFinishDailyFlag'):
                    print('��ʼ������Ϸ')
                    for i in range(1, 11):
                        wait_time = random.randint(1000, 3000) / 1000.0
                        time.sleep(wait_time)
                        if not self.anniversary2024_SearchWord_win(i):
                            break

                if not happy_elimination_info.get('isPassFlag') or not happy_elimination_info.get('isFinishDailyFlag'):
                    print('��ʼ������')
                    for i in range(1, 31):
                        wait_time = random.randint(2000, 4000) / 1000.0
                        time.sleep(wait_time)
                        if not self.anniversary2024_HappyElimination_win(i):
                            break
            else:
                error_message = response['errorMessage'] or json.dumps(response) or '�޷���'
                print('��ѯ��Ϸ״̬ʧ��: ' + error_message)
                if '�û��ֻ���У��δͨ��' in error_message:
                    self.anniversary_black = True
        except Exception as e:
            print(str(e))

    def anniversary2024_SearchWord_win(self, index):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024SearchWordService~win'
        success = True
        try:
            data = {'index': index}
            response = self.do_request(url, data)
            if response and response.get('success'):
                currency_list = response.get('obj', {}).get('currencyDTOList', [])
                rewards = ', '.join([f"[{c.get('currency')}]X{c.get('amount')}" for c in currency_list])
                print(f'������Ϸ��{index}��ͨ�سɹ�: {rewards if rewards else "δ��ý���"}')
            else:
                error_message = response.get('errorMessage') or json.dumps(response) or '�޷���'
                print(f'������Ϸ��{index}��ʧ��: {error_message}')
                if 'ϵͳ��æ' in error_message:
                    success = False
        except Exception as e:
            print(e)
        finally:
            return success

    def anniversary2024_HappyElimination_win(self, index):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024HappyEliminationService~win'
        success = True
        data = {'index': index}
        response = self.do_request(url, data)
        try:
            if response and response.get('success'):
                is_award = response['obj'].get('isAward')
                currency_dto_list = response['obj'].get('currencyDTOList', [])
                rewards = ', '.join([f"[{c.get('currency')}]X{c.get('amount')}" for c in currency_dto_list])
                print(f'��{index}��ͨ��: {rewards if rewards else "δ��ý���"}')
            else:
                error_message = response.get('errorMessage') or json.dumps(response) or '�޷���'
                print(f'��{index}��ʧ��: {error_message}')
                if 'ϵͳ��æ' in error_message:
                    success = False
        except Exception as e:
            print(e)
            success = False
        finally:
            return success

    def anniversary2024_TopicPk_chooseSide(self, index):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024TopicPkService~chooseSide'
        success = True
        data = {'index': index, 'choose': 0}
        response = self.do_request(url, data)
        try:
            if response and response.get('success'):
                currency_dto_list = response['obj'].get('currencyDTOList', [])
                rewards = ', '.join([f"[{c.get('currency')}]X{c.get('amount')}" for c in currency_dto_list])
                print(f'����PK��ѡ����{index}�ɹ��� {rewards if rewards else "δ��ý���"}')
            else:
                error_message = response['errorMessage'] or json.dumps(response) or '�޷���'
                print(f'����PK��ѡ����{index}ʧ�ܣ� {error_message}')
                if 'ϵͳ��æ' in error_message:
                    success = False
        except Exception as e:
            print(e)
            success = False
        finally:
            return success

    def anniversary2024_TopicPk_topicList(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024TopicPkService~topicList'
        response = self.do_request(url, {})
        try:
            if response and response.get('success'):
                topics = response['obj'].get('topics', [])
                for topic in topics:
                    if not topic.get('choose'):
                        index = topic.get('index', 1)
                        wait_time = random.randint(2000, 4000) / 1000.0
                        time.sleep(wait_time)
                        if not self.anniversary2024_TopicPk_chooseSide(index):
                            break
            else:
                error_message = response['errorMessage'] or json.dumps(response) or '�޷���'
                print(f'��ѯ����PK����¼ʧ�ܣ� {error_message}')
        except Exception as e:
            print(e)

    def anniversary2024_queryAccountStatus_refresh(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024CardService~queryAccountStatus'
        response = self.do_request(url, {})
        try:
            if not response or not response.get('success'):
                error_message = response['errorMessage'] or json.dumps(response) or '�޷���'
                print(f'��ѯ�˻�״̬ʧ�ܣ� {error_message}')
        except Exception as e:
            print(e)

    def anniversary2024_TopicPk_chooseSide(self, index):
        success = True
        data = {
            'index': index,
            'choose': 0
        }
        self.headers['channel'] = '31annizyw'
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024TopicPkService~chooseSide'
        result = self.do_request(url, data, 'post')

        if result and result.get('success'):
            currency_dto_list = result.get('obj', {}).get('currencyDTOList', [])
            if currency_dto_list:
                rewards = [f"[{currency['currency']}]{currency['amount']}��" for currency in currency_dto_list]
                print(f'����PK����{index}������ѡ��ɹ�: {", ".join(rewards)}')
            else:
                print(f'����PK����{index}������ѡ��ɹ�')
        else:
            error_message = result.get('errorMessage') if result else '�޷���'
            print(f'����PK����{index}������ʧ��: {error_message}')
            if error_message and 'ϵͳ��æ' in error_message:
                success = False

        return success

    def anniversary2024_titleList(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024GuessService~titleList'
        response = self.do_request(url)

        if response and response.get('success'):

            guess_title_info_list = response.get('obj', {}).get('guessTitleInfoList', [])
            today_titles = [title for title in guess_title_info_list if title['gameDate'] == self.today]
            for title_info in today_titles:
                if title_info['answerStatus']:
                    print('�����ѻش������')
                else:
                    answer = self.answer
                    if answer:
                        self.anniversary2024_answer(title_info, answer)
                        print(f'�����˴���: {answer}')
        else:
            error_message = response.get('errorMessage') if response else '�޷���'
            print(f'��ѯÿ�տ����ʧ��: {error_message}')

    def anniversary2024_titleList_award(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024GuessService~titleList'
        response = self.do_request(url)

        if response and response.get('success'):

            guess_title_info_list = response.get('obj', {}).get('guessTitleInfoList', [])
            today_awards = [title for title in guess_title_info_list if title['gameDate'] == self.today]

            for award_info in today_awards:
                if award_info['answerStatus']:
                    awards = award_info.get('awardList', []) + award_info.get('puzzleList', [])
                    awards_description = ', '.join([f"{award['productName']}" for award in awards])
                    print(f'����½���: {awards_description}' if awards_description else '�����޽���')
                else:
                    print('���ջ�û�ش𾺲�')
        else:
            error_message = response.get('errorMessage') if response else '�޷���'
            print(f'��ѯÿ�տ���½���ʧ��: {error_message}')

    def anniversary2024_answer(self, answer_info):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024GuessService~answer'
        data = {'period': answer_info['period'], 'answerInfo': answer_info}
        response = self.do_request(url, data)
        if response and response.get('success'):
            print('����»ش�ɹ�')
            self.anniversary2024_titleList_award()
        else:
            error_message = response.get('errorMessage') if response else '�޷���'
            print(f'����»ش�ʧ��: {error_message}')

    def anniversary2024_queryAccountStatus(self):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024CardService~queryAccountStatus'
        result = self.do_request(url)
        if result.get('success'):
            account_currency_list = result.get('obj', {}).get('accountCurrencyList', [])
            unbox_chance_currency = [currency for currency in account_currency_list if
                                     currency.get('currency') == 'UNBOX_CHANCE']
            unbox_chance_balance = unbox_chance_currency[0].get('balance') if unbox_chance_currency else 0

        else:
            error_message = result.get('errorMessage') or json.dumps(result) or '�޷���'
            print('��ѯ���ռ�ƴͼʧ��: ' + error_message)

        result = self.do_request(url)
        if result.get('success'):
            account_currency_list = result.get('obj', {}).get('accountCurrencyList', [])
            account_currency_list = [currency for currency in account_currency_list if
                                     currency.get('currency') != 'UNBOX_CHANCE']
            if account_currency_list:
                cards_li = account_currency_list
                card_info = []
                self.cards = {
                    'CARD_1': 0,
                    'CARD_2': 0,
                    'CARD_3': 0,
                    'CARD_4': 0,
                    'CARD_5': 0,
                    'CARD_6': 0,
                    'CARD_7': 0,
                    'CARD_8': 0,
                    'CARD_9': 0,
                    'COMMON_CARD': 0
                }
                for card in cards_li:
                    currency_key = card.get('currency')
                    if currency_key in self.cards:
                        self.cards[currency_key] = int(card.get('balance'))
                    card_info.append('[' + card.get('currency') + ']X' + str(card.get('balance')))

                Log(f'���ռ�ƴͼ: {card_info}')
                cards_li.sort(key=lambda x: x.get('balance'), reverse=True)

            else:
                print('��û���ռ���ƴͼ')
        else:
            error_message = result.get('errorMessage') or json.dumps(result) or '�޷���'
            print('��ѯ���ռ�ƴͼʧ��: ' + error_message)

    def do_draw(self, cards):
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~anniversary2024CardService~collectDrawAward'
        data = {"accountList": cards}
        response = self.do_request(url, data)
        if response and response.get('success'):
            data = response.get('obj', {})
            productName = data.get('productName', '')
            Log(f'�齱�ɹ�,���{productName}')
            return True
        else:
            error_message = response.get('errorMessage') if response else '�޷���'
            print(f'�齱ʧ��: {error_message}')
            return False

    def convert_common_card(self, cards, target_card):
        if cards['COMMON_CARD'] > 0:
            cards['COMMON_CARD'] -= 1
            cards[target_card] += 1
            return True
        return False

    def can_draw(self, cards, n):
        distinct_cards = sum(1 for card, amount in cards.items() if card != 'COMMON_CARD' and amount > 0)
        return distinct_cards >= n

    def draw(self, cards, n):
        drawn_cards = []
        for card, amount in sorted(cards.items(), key=lambda item: item[1]):
            if card != 'COMMON_CARD' and amount > 0:
                cards[card] -= 1
                drawn_cards.append(card)
                if len(drawn_cards) == n:
                    break
        if len(drawn_cards) == n:
            "û���㹻�Ŀ����г齱"
        if self.do_draw(drawn_cards):
            return drawn_cards
        else:
            return None

    def simulate_lottery(self, cards):
        while self.can_draw(cards, 9):
            used_cards = self.draw(cards, 9)
            print("������һ��9���齱�����Ŀ�Ƭ: ", used_cards)
        while self.can_draw(cards, 7) or self.convert_common_card(cards, 'CARD_1'):
            if not self.can_draw(cards, 7):
                continue
            used_cards = self.draw(cards, 7)
            print("������һ��7���齱�����Ŀ�Ƭ: ", used_cards)
        while self.can_draw(cards, 5) or self.convert_common_card(cards, 'CARD_1'):
            if not self.can_draw(cards, 5):
                continue
            used_cards = self.draw(cards, 5)
            print("������һ��5���齱�����Ŀ�Ƭ: ", used_cards)
        while self.can_draw(cards, 3) or self.convert_common_card(cards, 'CARD_1'):
            if not self.can_draw(cards, 3):
                continue
            used_cards = self.draw(cards, 3)
            print("������һ��3���齱�����Ŀ�Ƭ: ", used_cards)

    def anniversary2024_task(self):
        self.anniversary2024_weekly_gift_status()
        if self.anniversary_black:
            return
        self.anniversary2024_queryAccountStatus()
        target_time = datetime(2024, 4, 3, 14, 0)
        if datetime.now() > target_time:
            print('������������������ʼ�Զ��齱')
            self.simulate_lottery(self.cards)
        else:
            print('δ���Զ��齱ʱ��')

    def member_day_index(self):
        print('====== ��Ա�ջ ======')
        try:
            invite_user_id = random.choice([invite for invite in inviteId if invite != self.user_id])
            payload = {'inviteUserId': invite_user_id}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayIndexService~index'

            response = self.do_request(url, data=payload)
            if response.get('success'):
                lottery_num = response.get('obj', {}).get('lotteryNum', 0)
                can_receive_invite_award = response.get('obj', {}).get('canReceiveInviteAward', False)
                if can_receive_invite_award:
                    self.member_day_receive_invite_award(invite_user_id)
                self.member_day_red_packet_status()
                Log(f'��Ա�տ��Գ齱{lottery_num}��')
                for _ in range(lottery_num):
                    self.member_day_lottery()
                if self.member_day_black:
                    return
                self.member_day_task_list()
                if self.member_day_black:
                    return
                self.member_day_red_packet_status()
            else:
                error_message = response.get('errorMessage', '�޷���')
                Log(f'��ѯ��Ա��ʧ��: {error_message}')
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_receive_invite_award(self, invite_user_id):
        try:
            payload = {'inviteUserId': invite_user_id}

            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayIndexService~receiveInviteAward'

            response = self.do_request(url, payload)
            if response.get('success'):
                product_name = response.get('obj', {}).get('productName', '����')
                Log(f'��Ա�ս���: {product_name}')
            else:
                error_message = response.get('errorMessage', '�޷���')
                Log(f'��ȡ��Ա�ս���ʧ��: {error_message}')
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_lottery(self):
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayLotteryService~lottery'

            response = self.do_request(url, payload)
            if response.get('success'):
                product_name = response.get('obj', {}).get('productName', '����')
                Log(f'��Ա�ճ齱: {product_name}')
            else:
                error_message = response.get('errorMessage', '�޷���')
                Log(f'��Ա�ճ齱ʧ��: {error_message}')
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_task_list(self):
        try:
            payload = {'activityCode': 'MEMBER_DAY', 'channelType': 'MINI_PROGRAM'}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'

            response = self.do_request(url, payload)
            if response.get('success'):
                task_list = response.get('obj', [])
                for task in task_list:
                    if task['status'] == 1:
                        if self.member_day_black:
                            return
                        self.member_day_fetch_mix_task_reward(task)
                for task in task_list:
                    if task['status'] == 2:
                        if self.member_day_black:
                            return
                        if task['taskType'] in ['SEND_SUCCESS', 'INVITEFRIENDS_PARTAKE_ACTIVITY', 'OPEN_SVIP',
                                                'OPEN_NEW_EXPRESS_CARD', 'OPEN_FAMILY_CARD', 'CHARGE_NEW_EXPRESS_CARD',
                                                'INTEGRAL_EXCHANGE']:
                            pass
                        else:
                            for _ in range(task['restFinishTime']):
                                if self.member_day_black:
                                    return
                                self.member_day_finish_task(task)
            else:
                error_message = response.get('errorMessage', '�޷���')
                Log('��ѯ��Ա������ʧ��: ' + error_message)
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_finish_task(self, task):
        try:
            payload = {'taskCode': task['taskCode']}

            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'

            response = self.do_request(url, payload)
            if response.get('success'):
                Log('��ɻ�Ա������[' + task['taskName'] + ']�ɹ�')
                self.member_day_fetch_mix_task_reward(task)
            else:
                error_message = response.get('errorMessage', '�޷���')
                Log('��ɻ�Ա������[' + task['taskName'] + ']ʧ��: ' + error_message)
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_fetch_mix_task_reward(self, task):
        try:
            payload = {'taskType': task['taskType'], 'activityCode': 'MEMBER_DAY', 'channelType': 'MINI_PROGRAM'}

            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~fetchMixTaskReward'

            response = self.do_request(url, payload)
            if response.get('success'):
                Log('��ȡ��Ա������[' + task['taskName'] + ']�����ɹ�')
            else:
                error_message = response.get('errorMessage', '�޷���')
                Log('��ȡ��Ա������[' + task['taskName'] + ']����ʧ��: ' + error_message)
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_receive_red_packet(self, hour):
        try:
            payload = {'receiveHour': hour}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayTaskService~receiveRedPacket'

            response = self.do_request(url, payload)
            if response.get('success'):
                print(f'��Ա����ȡ{hour}�����ɹ�')
            else:
                error_message = response.get('errorMessage', '�޷���')
                print(f'��Ա����ȡ{hour}����ʧ��: {error_message}')
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_red_packet_status(self):
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketStatus'
            response = self.do_request(url, payload)
            if response.get('success'):
                packet_list = response.get('obj', {}).get('packetList', [])
                for packet in packet_list:
                    self.member_day_red_packet_map[packet['level']] = packet['count']

                for level in range(1, self.max_level):
                    count = self.member_day_red_packet_map.get(level, 0)
                    while count >= 2:
                        self.member_day_red_packet_merge(level)
                        count -= 2
                packet_summary = []
                remaining_needed = 0

                for level, count in self.member_day_red_packet_map.items():
                    if count == 0:
                        continue
                    packet_summary.append(f"[{level}��]X{count}")
                    int_level = int(level)
                    if int_level < self.max_level:
                        remaining_needed += 1 << (int_level - 1)

                Log("��Ա�պϳ��б�: " + ", ".join(packet_summary))

                if self.member_day_red_packet_map.get(self.max_level):
                    Log(f"��Ա����ӵ��[{self.max_level}��]���X{self.member_day_red_packet_map[self.max_level]}")
                    self.member_day_red_packet_draw(self.max_level)
                else:
                    remaining = self.packet_threshold - remaining_needed
                    Log(f"��Ա�վ���[{self.max_level}��]�������: [1��]���X{remaining}")

            else:
                error_message = response.get('errorMessage', '�޷���')
                Log(f'��ѯ��Ա�պϳ�ʧ��: {error_message}')
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_red_packet_merge(self, level):
        try:
            payload = {'level': level, 'num': 2}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketMerge'

            response = self.do_request(url, payload)
            if response.get('success'):
                Log(f'��Ա�պϳ�: [{level}��]���X2 -> [{level + 1}��]���')
                self.member_day_red_packet_map[level] -= 2
                if not self.member_day_red_packet_map.get(level + 1):
                    self.member_day_red_packet_map[level + 1] = 0
                self.member_day_red_packet_map[level + 1] += 1
            else:
                error_message = response.get('errorMessage', '�޷���')
                Log(f'��Ա�պϳ�����[{level}��]���ʧ��: {error_message}')
                if 'û���ʸ����' in error_message:
                    self.member_day_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def member_day_red_packet_draw(self, level):
        try:
            payload = {'level': str(level)}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~memberDayPacketService~redPacketDraw'
            response = self.do_request(url, payload)
            if response and response.get('success'):
                coupon_names = [item['couponName'] for item in response.get('obj', [])] or []

                Log(f"��Ա����ȡ[{level}��]���: {', '.join(coupon_names) or '����'}")
            else:
                error_message = response.get('errorMessage') if response else "�޷���"
                Log(f"��Ա����ȡ[{level}��]���ʧ��: {error_message}")
                if "û���ʸ����" in error_message:
                    self.memberDay_black = True
                    print("��Ա��������")
        except Exception as e:
            print(e)

    def DRAGONBOAT_2024_index(self):
        print('====== ��ѯ���ۻ״̬ ======')
        invite_user_id = random.choice([invite for invite in inviteId if invite != self.user_id])
        try:
            self.headers['channel'] = 'newExpressWX'
            self.headers[
                'referer'] = f'https://mcs-mimp-web.sf-express.com/origin/a/mimp-activity/dragonBoat2024?mobile={self.mobile}&userId={self.user_id}&path=/origin/a/mimp-activity/dragonBoat2024&supportShare=&inviteUserId={invite_user_id}&from=newExpressWX'
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonNoLoginPost/~memberNonactivity~dragonBoat2024IndexService~index'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                acEndTime = obj.get('acEndTime', '')
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                comparison_time = datetime.strptime(acEndTime, "%Y-%m-%d %H:%M:%S")
                is_less_than = datetime.now() < comparison_time
                if is_less_than:
                    print('�����ζ�������....')
                    return True
                else:
                    print('���ۻ�ѽ���')
                    return False
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('��Ա��������')
                return False
        except Exception as e:
            print(e)
            return False

    def DRAGONBOAT_2024_Game_indexInfo(self):
        Log('====== ��ʼ��������Ϸ ======')
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2024GameService~indexInfo'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                maxPassLevel = obj.get('maxPassLevel', '')
                ifPassAllLevel = obj.get('ifPassAllLevel', '')
                if maxPassLevel != 30:
                    self.DRAGONBOAT_2024_win(maxPassLevel)
                else:
                    self.DRAGONBOAT_2024_win(0)

            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('��Ա��������')
                return False
        except Exception as e:
            print(e)
            return False

    def DRAGONBOAT_2024_Game_init(self):
        Log('====== ��ʼ��������Ϸ ======')
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2024GameService~init'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                currentIndex = obj.get('currentIndex', '')
                ifPassAllLevel = obj.get('ifPassAllLevel', '')
                if currentIndex != 30:
                    self.DRAGONBOAT_2024_win(currentIndex)
                else:
                    self.DRAGONBOAT_2024_win(0)

            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('��Ա��������')
                return False
        except Exception as e:
            print(e)
            return False

    def DRAGONBOAT_2024_weeklyGiftStatus(self):
        print('====== ��ѯÿ�������ȡ״̬ ======')
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2024IndexService~weeklyGiftStatus'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                for gift in obj:
                    received = gift['received']
                    receiveStartTime = gift['receiveStartTime']
                    receiveEndTime = gift['receiveEndTime']
                    print(f'>>> ��ȡʱ�䣺��{receiveStartTime} �� {receiveEndTime}��')
                    if received:
                        print('> ���������ȡ')
                        continue
                    receive_start_time = datetime.strptime(receiveStartTime, "%Y-%m-%d %H:%M:%S")
                    receive_end_time = datetime.strptime(receiveEndTime, "%Y-%m-%d %H:%M:%S")
                    is_within_range = receive_start_time <= datetime.now() <= receive_end_time
                    if is_within_range:
                        print(f'>> ��ʼ��ȡ�����')
                        self.DRAGONBOAT_2024_receiveWeeklyGift()
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def DRAGONBOAT_2024_receiveWeeklyGift(self):
        invite_user_id = random.choice([invite for invite in inviteId if invite != self.user_id])
        try:
            payload = {"inviteUserId": invite_user_id}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2024IndexService~receiveWeeklyGift'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                if obj == [{}]:
                    print('> ��ȡʧ��')
                    return False
                for gifts in obj:
                    productName = gifts['productName']
                    amount = gifts['amount']
                    print(f'> ��ȡ��{productName} x {amount}���ɹ�')
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def DRAGONBOAT_2024_taskList(self):
        print('====== ��ѯ�Ʊ������б� ======')
        try:
            payload = {
                "activityCode": "DRAGONBOAT_2024",
                "channelType": "MINI_PROGRAM"
            }
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                for task in obj:
                    taskType = task['taskType']
                    self.taskName = task['taskName']
                    status = task['status']
                    if status == 3:
                        Log(f'> ����{self.taskName}�������')
                        continue
                    self.taskCode = task.get('taskCode', None)
                    if self.taskCode:
                        self.DRAGONBOAT_2024_finishTask()
                    if taskType == 'PLAY_ACTIVITY_GAME':
                        self.DRAGONBOAT_2024_Game_init()
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def DRAGONBOAT_2024_coinStatus(self, END=False):
        Log('====== ��ѯ�����Ϣ ======')
        # try:
        payload = {}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2024CoinService~coinStatus'

        response = self.do_request(url, payload)
        if response.get('success'):
            obj = response.get('obj', None)
            if obj == None: return False
            accountCurrencyList = obj.get('accountCurrencyList', [])
            pushedTimesToday = obj.get('pushedTimesToday', '')
            pushedTimesTotal = obj.get('pushedTimesTotal', '')
            PUSH_TIMES_balance = 0
            self.COIN_balance = 0
            WELFARE_CARD_balance = 0
            for li in accountCurrencyList:
                if li['currency'] == 'PUSH_TIMES':
                    PUSH_TIMES_balance = li['balance']
                if li['currency'] == 'COIN':
                    self.COIN_balance = li['balance']
                if li['currency'] == 'WELFARE_CARD':
                    WELFARE_CARD_balance = li['balance']

            PUSH_TIMES = PUSH_TIMES_balance
            if END:
                if PUSH_TIMES_balance > 0:
                    for i in range(PUSH_TIMES_balance):
                        print(f'>> ��ʼ�ڡ�{PUSH_TIMES_balance + 1}�����Ʊ�')
                        self.DRAGONBOAT_2024_pushCoin()
                        PUSH_TIMES -= 1
                        pushedTimesToday += 1
                        pushedTimesTotal += 1
                Log(f'> ʣ���ƱҴ�������{PUSH_TIMES}��')
                Log(f'> ��ǰ��ң���{self.COIN_balance}��')
                Log(f'> �����Ʊң���{pushedTimesToday}����')
                Log(f'> ���Ʊң���{pushedTimesTotal}����')
            else:
                print(f'> ʣ���ƱҴ�������{PUSH_TIMES_balance}��')
                print(f'> ��ǰ��ң���{self.COIN_balance}��')
                print(f'> �����Ʊң���{pushedTimesToday}����')
                print(f'> ���Ʊң���{pushedTimesTotal}����')

            self.DRAGONBOAT_2024_givePushTimes()
        else:
            error_message = response.get('errorMessage', '�޷���')
            if 'û���ʸ����' in error_message:
                self.DRAGONBOAT_2024_black = True
                Log('��Ա��������')

    def DRAGONBOAT_2024_pushCoin(self):
        try:
            payload = {"plateToken": None}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2024CoinService~pushCoin'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                drawAward = obj.get('drawAward', '')
                self.COIN_balance += drawAward
                print(f'> ��ã���{drawAward}�����')

            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def DRAGONBOAT_2024_givePushTimes(self):
        Log('====== ��ȡ�����ƱҴ��� ======')
        try:
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2024CoinService~givePushTimes'

            response = self.do_request(url)
            if response.get('success'):
                obj = response.get('obj', 0)
                print(f'> ��ã���{obj}�����Ʊһ���')
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('> ��Ա��������')
                print(error_message)
        except Exception as e:
            print(e)

    def DRAGONBOAT_2024_finishTask(self):
        try:
            payload = {
                "taskCode": self.taskCode
            }
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', False)
                Log(f'> �������{self.taskName}���ɹ�')
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.DRAGONBOAT_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def DRAGONBOAT_2024_win(self, level):
        try:
            for i in range(level, 31):
                print(f'��ʼ�ڡ�{i}����')
                payload = {"levelIndex": i}
                url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2024GameService~win'

                response = self.do_request(url, payload)
                if response.get('success'):
                    obj = response.get('obj', [{}])
                    currentAwardList = obj.get('currentAwardList', [])
                    if currentAwardList != []:
                        for award in currentAwardList:
                            currency = award.get('currency', '')
                            amount = award.get('amount', '')
                            print(f'> ��ã���{currency}��x{amount}')
                    else:
                        print(f'> �����޽���')
                else:
                    error_message = response.get('errorMessage', '�޷���')
                    print(error_message)
                    if 'û���ʸ����' in error_message:
                        self.DRAGONBOAT_2024_black = True
                        Log('��Ա��������')
        except Exception as e:
            print(e)


    def MIDAUTUMN_2024_index(self):
        print('====== ��ѯ����״̬ ======')
        invite_user_id = random.choice([invite for invite in inviteId if invite != self.user_id])
        try:
            self.headers['channel'] = '24zqxcx'
            self.headers[
                'referer'] = f'https://mcs-mimp-web.sf-express.com/origin/a/mimp-activity/midAutumn2024?mobile={self.mobile}&userId={self.user_id}&path=/origin/a/mimp-activity/midAutumn2024&supportShare=&inviteUserId={invite_user_id}&from=24zqxcx'
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonNoLoginPost/~memberNonactivity~midAutumn2024IndexService~index'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                acEndTime = obj.get('acEndTime', '')
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                comparison_time = datetime.strptime(acEndTime, "%Y-%m-%d %H:%M:%S")
                is_less_than = datetime.now() < comparison_time
                if is_less_than:
                    print('�����ζ�������....')
                    return True
                else:
                    print('�����ѽ���')
                    return False
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('��Ա��������')
                return False
        except Exception as e:
            print(e)
            return False

    def MIDAUTUMN_2024_Game_indexInfo(self):
        Log('====== ��ʼ��������Ϸ ======')
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~midAutumn2024GameService~indexInfo'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                maxPassLevel = obj.get('maxPassLevel', '')
                ifPassAllLevel = obj.get('ifPassAllLevel', '')
                if maxPassLevel != 30:
                    self.MIDAUTUMN_2024_win(maxPassLevel)
                else:
                    self.MIDAUTUMN_2024_win(0)

            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('��Ա��������')
                return False
        except Exception as e:
            print(e)
            return False

    def MIDAUTUMN_2024_Game_init(self):
        Log('====== ��ʼ��������Ϸ ======')
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~midAutumn2024GameService~init'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                currentIndex = obj.get('currentIndex', '')
                ifPassAllLevel = obj.get('ifPassAllLevel', '')
                if currentIndex != 30:
                    self.MIDAUTUMN_2024_win(currentIndex)
                else:
                    self.MIDAUTUMN_2024_win(0)

            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('��Ա��������')
                return False
        except Exception as e:
            print(e)
            return False

    def MIDAUTUMN_2024_weeklyGiftStatus(self):
        print('====== ��ѯÿ�������ȡ״̬ ======')
        try:
            payload = {}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~midAutumn2024IndexService~weeklyGiftStatus'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                for gift in obj:
                    received = gift['received']
                    receiveStartTime = gift['receiveStartTime']
                    receiveEndTime = gift['receiveEndTime']
                    print(f'>>> ��ȡʱ�䣺��{receiveStartTime} �� {receiveEndTime}��')
                    if received:
                        print('> ���������ȡ')
                        continue
                    receive_start_time = datetime.strptime(receiveStartTime, "%Y-%m-%d %H:%M:%S")
                    receive_end_time = datetime.strptime(receiveEndTime, "%Y-%m-%d %H:%M:%S")
                    is_within_range = receive_start_time <= datetime.now() <= receive_end_time
                    if is_within_range:
                        print(f'>> ��ʼ��ȡ�����')
                        self.MIDAUTUMN_2024_receiveWeeklyGift()
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def MIDAUTUMN_2024_receiveWeeklyGift(self):
        invite_user_id = random.choice([invite for invite in inviteId if invite != self.user_id])
        try:
            payload = {"inviteUserId": invite_user_id}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~midAutumn2024IndexService~receiveWeeklyGift'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                if obj == [{}]:
                    print('> ��ȡʧ��')
                    return False
                for gifts in obj:
                    productName = gifts['productName']
                    amount = gifts['amount']
                    print(f'> ��ȡ��{productName} x {amount}���ɹ�')
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def MIDAUTUMN_2024_taskList(self):
        print('====== ��ѯ�Ʊ������б� ======')
        try:
            payload = {
                "activityCode": "MIDAUTUMN_2024",
                "channelType": "MINI_PROGRAM"
            }
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                for task in obj:
                    taskType = task['taskType']
                    self.taskName = task['taskName']
                    status = task['status']
                    if status == 3:
                        Log(f'> ����{self.taskName}�������')
                        continue
                    self.taskCode = task.get('taskCode', None)
                    if self.taskCode:
                        self.MIDAUTUMN_2024_finishTask()
                    if taskType == 'PLAY_ACTIVITY_GAME':
                        self.MIDAUTUMN_2024_Game_init()
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def MIDAUTUMN_2024_coinStatus(self, END=False):
        Log('====== ��ѯ�����Ϣ ======')
        # try:
        payload = {}
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~midAutumn2024CoinService~coinStatus'

        response = self.do_request(url,payload)
        if response.get('success'):
            obj = response.get('obj', None)
            if obj == None: return False
            accountCurrencyList = obj.get('accountCurrencyList', [])
            pushedTimesToday = obj.get('pushedTimesToday', '')
            pushedTimesTotal = obj.get('pushedTimesTotal', '')
            PUSH_TIMES_balance = 0
            self.COIN_balance = 0
            WELFARE_CARD_balance = 0
            for li in accountCurrencyList:
                if li['currency'] == 'PUSH_TIMES':
                    PUSH_TIMES_balance = li['balance']
                if li['currency'] == 'COIN':
                    self.COIN_balance = li['balance']
                if li['currency'] == 'WELFARE_CARD':
                    WELFARE_CARD_balance = li['balance']

            PUSH_TIMES = PUSH_TIMES_balance
            if END:
                if PUSH_TIMES_balance > 0:
                    for i in range(PUSH_TIMES_balance):
                        print(f'>> ��ʼ�ڡ�{PUSH_TIMES_balance + 1}�����Ʊ�')
                        self.MIDAUTUMN_2024_pushCoin()
                        PUSH_TIMES -= 1
                        pushedTimesToday += 1
                        pushedTimesTotal += 1
                Log(f'> ʣ���ƱҴ�������{PUSH_TIMES}��')
                Log(f'> ��ǰ��ң���{self.COIN_balance}��')
                Log(f'> �����Ʊң���{pushedTimesToday}����')
                Log(f'> ���Ʊң���{pushedTimesTotal}����')
            else:
                print(f'> ʣ���ƱҴ�������{PUSH_TIMES_balance}��')
                print(f'> ��ǰ��ң���{self.COIN_balance}��')
                print(f'> �����Ʊң���{pushedTimesToday}����')
                print(f'> ���Ʊң���{pushedTimesTotal}����')

            self.MIDAUTUMN_2024_givePushTimes()
        else:
            error_message = response.get('errorMessage', '�޷���')
            if 'û���ʸ����' in error_message:
                self.MIDAUTUMN_2024_black = True
                Log('��Ա��������')

    def MIDAUTUMN_2024_pushCoin(self):
        try:
            payload = {"plateToken": None}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~midAutumn2024CoinService~pushCoin'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', [{}])
                drawAward = obj.get('drawAward', '')
                self.COIN_balance += drawAward
                print(f'> ��ã���{drawAward}�����')

            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def MIDAUTUMN_2024_givePushTimes(self):
        Log('====== ��ȡ�����ƱҴ��� ======')
        try:
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~midAutumn2024CoinService~givePushTimes'

            response = self.do_request(url)
            if response.get('success'):
                obj = response.get('obj', 0)
                print(f'> ��ã���{obj}�����Ʊһ���')
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('> ��Ա��������')
                print(error_message)
        except Exception as e:
            print(e)

    def MIDAUTUMN_2024_finishTask(self):
        try:
            payload = {
                "taskCode": self.taskCode
            }
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'

            response = self.do_request(url, payload)
            if response.get('success'):
                obj = response.get('obj', False)
                Log(f'> �������{self.taskName}���ɹ�')
            else:
                error_message = response.get('errorMessage', '�޷���')
                if 'û���ʸ����' in error_message:
                    self.MIDAUTUMN_2024_black = True
                    Log('��Ա��������')
        except Exception as e:
            print(e)

    def MIDAUTUMN_2024_win(self, level):
        try:
            for i in range(level, 31):
                print(f'��ʼ�ڡ�{i}����')
                payload = {"levelIndex": i}
                url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~midAutumn2024GameService~win'

                response = self.do_request(url, payload)
                if response.get('success'):
                    obj = response.get('obj', [{}])
                    currentAwardList = obj.get('currentAwardList', [])
                    if currentAwardList != []:
                        for award in currentAwardList:
                            currency = award.get('currency', '')
                            amount = award.get('amount', '')
                            print(f'> ��ã���{currency}��x{amount}')
                    else:
                        print(f'> �����޽���')
                else:
                    error_message = response.get('errorMessage', '�޷���')
                    print(error_message)
                    if 'û���ʸ����' in error_message:
                        self.MIDAUTUMN_2024_black = True
                        Log('��Ա��������')
        except Exception as e:
            print(e)
    def csy2025(self):
        """
        ��ѯ����ү�����б������������߼���
        """
        Log('>>>>>>��ʼ��ʿ��')
        try:
            _id=random.choice([invite for invite in inviteId if invite != self.user_id])
            self.do_request("https://mcs-mimp-web.sf-express.com/mcs-mimp/commonNoLoginPost/~memberNonactivity~disneyService~index")
            payload = {"activityCode": "DISNEY", "channelType": "MINI_PROGRAM"}
            url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~activityTaskService~taskList"

            response = self.do_request(url, payload)
            if isinstance(response, dict) and response.get('success'):
                tasks = response.get('obj', [])
                for task in tasks:
                    taskType = task.get('taskType', None)
                    taskName = task.get('taskName', 'δ֪����')
                    taskCode = task.get('taskCode', None)
                    taskStatus = task.get('status', 0)

                    #�·�����'BROWSE_VIP_CENTER'����taskType��ID
                    if taskType not in ['BROWSE_LIFE_SERVICE','INTEGRAL_EXCHANGE','BROWSE_VIP_CENTER','BROWSE_STUDENT_BENEFIT','LOOK_BRAND_VIDEO']:
                        continue
                    Log(f"> ���ڴ�������{taskName}��")

                    if taskStatus == 3:
                        Log(f"> ����{taskName}������ɣ�����")
                        continue

                    if taskCode:
                        self.DISNEY2_finishTask(taskCode, taskName)
                        self.fetchTasksReward()
        except Exception as e:
            import traceback
            Log(f"�����ѯʱ�����쳣��{e}\n{traceback.format_exc()}")


    def DISNEY2_finishTask(self, taskCode, taskName):
        try:
            payload = {"taskCode": taskCode}
            url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberEs~taskRecord~finishTask'

            response = self.do_request(url, payload)

            if isinstance(response, dict) and response.get('success'):
                obj = response.get('obj', None)
                if obj is True:
                    Log(f"> {taskName}-�����")
                    return True
                elif obj is False:
                    # Log(f"> {taskName}-δ��ɣ�ʧ��ԭ�򣺷��ص� obj Ϊ False�����������Ч�������")
                    self.fetchTasksReward()
                    return False
                elif isinstance(obj, dict):
                    data = obj.get('data', [])
                    Log(f"> {taskName}-����ɣ��������ݣ�{data}")
                    return True
                else:
                    Log(f"> {taskName}-δ��ɣ�ʧ��ԭ�򣺷��ص� obj ����δ֪��ʵ��Ϊ: {obj}")
                    return False
            else:
                error_message = response.get('errorMessage', '�޷���') if isinstance(response, dict) else 'δ֪����'
                Log(f"> {taskName}-δ��ɣ�ʧ��ԭ��{error_message}")
                return False
        except Exception as e:
            import traceback
            Log(f"{taskName}-δ��ɣ�������룺��{taskCode}�����쳣��Ϣ��{e}\n{traceback.format_exc()}")
            return False
    def sendMsg(self, help=False):
        if self.send_UID:
            push_res = CHERWIN_TOOLS.wxpusher(self.send_UID, one_msg, APP_NAME, help)
            print(push_res)

    def duanwuChoujiang(self):
        Log('====== ��ʼ��ʿ��齱 ======')
        try:
            # ��ѯ�齱״̬
            query_url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~disneyService~getStatus"
            query_payload = {}
            query_response = self.do_request(query_url, query_payload)
    
            if query_response.get('success') and query_response.get('obj'):
                obj = query_response['obj']
                remain_times = obj.get('remainTimes', 0)
                Log(f'??ʣ��齱����Ϊ = {remain_times}')
                if remain_times <= 0:
                    Log('??���޿��ó齱����')
                    return
    
                # ֱ�Ӹ��� remain_times ѭ���齱�������ֱ���
                total_drawn = 0
                for i in range(remain_times):
                    Log(f'>>> �� {i + 1} �γ齱')
                    draw_url = "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~disneyService~openPackage"
                    draw_payload = {}  # �������ֲ���
                    draw_response = self.do_request(draw_url, draw_payload)
    
                    if draw_response.get('success') and draw_response.get('obj'):
                        obj = draw_response['obj']
                        # �ȳ���ȡ award
                        award = obj.get('award')
                        if award:
                            product_name = award.get('productName', 'δ֪��Ʒ')
                            price_desc = award.get('denomination', '')
                        else:
                            # �ٳ���ȡ paidProductPacket
                            paid_product = obj.get('paidProductPacket', {})
                            product_name = paid_product.get('productName', 'δ֪��Ʒ')
                            price_desc = paid_product.get('priceDesc', '')
                        Log(f'?? �齱�ɹ���{product_name} - {price_desc}')
                    else:
                        error_message = draw_response.get('errorMessage') or draw_response.get('msg') or '�޷���'
                        Log(f'? �齱ʧ��: {error_message}')
                    total_drawn += 1
                    time.sleep(1)  # ��ֹ�������
    
                Log(f'���齱 {total_drawn} �Σ�����')
    
            else:
                error_message = query_response.get('msg') or str(query_response)
                Log(f'��ȡ�齱״̬ʧ��: {error_message}')
    
        except Exception as e:
            import traceback
            Log(f'��ʿ���齱ʱ�����쳣: {e}\n{traceback.format_exc()}')


        Log('====== ��ʿ���齱���� ======')

    def fetchTasksReward(self):
        response = self.do_request(
            "https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~dragonBoat2025TaskService~fetchTasksReward",
            {"channelType":"MINI_PROGRAM"}
        )
        if response.get('success'):
            if len(response.get('obj',{}).get('receivedAccountList',[])):
                Log(f">��ȡ����������� {len(response.get('obj',{}).get('receivedAccountList',[]))} ��")
    def qiandao(self):
        self.superWelfare_receiveRedPacket()
        self.get_SignTaskList()
        self.get_SignTaskList(True)
    def fengmi(self):
        self.honey_indexData()
        self.get_honeyTaskListStart()
        self.honey_indexData(True)
        activity_end_date = get_quarter_end_date()
        days_left = (activity_end_date - datetime.now()).days
        if days_left == 0:
            message = "������ۻ��ֹ�һ���ʣ���0���ˣ��뼰ʱ���жһ�"
            Log(message)
        else:
            message = f"������ۻ��ֹ�һ�����{days_left}�죬�뼰ʱ���жһ�"
            Log(message)
        target_time = datetime(2024, 4, 8, 19, 0)
        if datetime.now() < target_time:
            self.anniversary2024_task()
        else:
            print('#######################################')
    def huiyuanri(self):
        current_date = datetime.now().day
        if 26 <= current_date <= 28:
            self.member_day_index()

        else:
            print('δ��ָ��ʱ�䲻ִ�л�Ա������')

            self.sendMsg()
            return True
    def duanwu(self):
        target_time = datetime(2025, 6, 3, 19, 0)
        if datetime.now() < target_time:#�����Ƿ����
            self.csy2025()
            # self.Exchangee_2025()#���ֶһ�����
            self.game202505()
            self.fetchTasksReward()
            # self.cxcs()
            # self.index2025()
            self.duanwuChoujiang()# ִ�ж���齱
        else:
            print('�����ѽ���')

    def main(self):
        global one_msg
        wait_time = random.randint(1000, 3000) / 1000.0
        time.sleep(wait_time)  # �ȴ�
        one_msg = ''
        if not self.login_res: return False

        self.duanwu()#����
        self.qiandao()#�ճ�ǩ������
        self.fengmi()#��������
        self.huiyuanri()#��Ա��

        


def get_quarter_end_date():
    current_year = datetime.now().year
    current_month = datetime.now().month

    if current_month in [1, 2, 3]:
        next_quarter_first_day = datetime(current_year, 4, 1)
    elif current_month in [4, 5, 6]:
        next_quarter_first_day = datetime(current_year, 7, 1)
    elif current_month in [7, 8, 9]:
        next_quarter_first_day = datetime(current_year, 10, 1)
    else:
        next_quarter_first_day = datetime(current_year + 1, 1, 1)
    return next_quarter_first_day

def is_activity_end_date(end_date):
    if isinstance(end_date, datetime):
        end_date = end_date.date()
    elif isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    else:
        raise TypeError("end_date must be a string or datetime object")

    return end_date




if __name__ == '__main__':
    APP_NAME = '˳������'
    ENV_NAME = 'sfsyUrl'
    CK_NAME = 'url'
    print(f'''
        2025/1/4�����ջ������û�г齱����Щ��ӡ��ʾ���ⲻ���ˣ���Ӱ��������ɡ�
        2025/1/5�����ջ�������޸�������
        2025/03/17���ջ�������޸�32�����죬��Ҫ�ֶ���˳��С�������ҳ��
        2025/05/23 ��Ϊ��ʿ��
      ��������֡������¼���url֮һ��
        https://mcs-mimp-web.sf-express.com/mcs-mimp/share/weChat/shareGiftReceiveRedirect
        https://mcs-mimp-web.sf-express.com/mcs-mimp/share/app/shareRedirect
    ���˺Ż���
    ��������sfsyUrl �������Ʊ�����

    ''')
    token = os.getenv(ENV_NAME)
    tokens = re.split("@|#|\n", os.environ.get(ENV_NAME))
    local_version = '2024.06.02'
    all_logs = []
    if len(tokens) > 0:
        
        print(f"\n>>>>>>>>>>����ȡ��{len(tokens)}���˺�<<<<<<<<<<")
        for index, infos in enumerate(tokens):
            run_instance = RUN(infos, index)
            run_result = run_instance.main()
            if run_instance.all_logs:
                all_logs.extend(run_instance.all_logs)
            if not run_result:
                continue
            
def wxpusher_notify(content):
    WXPUSHER_APP_TOKEN = ''
    WXPUSHER_UIDS = ''  # ���UID��Ӣ�Ķ��ŷָ�
    WXPUSHER_TOPIC_IDS = ''

    if not WXPUSHER_APP_TOKEN:
        print("δ����WXPUSHER_APP_TOKEN��������")
        return

    url = "https://wxpusher.zjiecode.com/api/send/message"
    headers = {"Content-Type": "application/json"}
    payload = {
        "appToken": WXPUSHER_APP_TOKEN,
        "content": content,
        "summary": "˳�����˵�ʿ������֪ͨ",
        "contentType": 1,  # 1=�ı�
        "topicIds": [int(i) for i in WXPUSHER_TOPIC_IDS.split(',') if i.strip()],
    }

    if WXPUSHER_UIDS:
        payload["uids"] = [i for i in WXPUSHER_UIDS.split(',') if i.strip()]

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            print("Wxpusher ���ͳɹ���")
        else:
            print(f"Wxpusher ����ʧ��: {response.text}")
    except Exception as e:
        print(f"Wxpusher �����쳣: {str(e)}")


if __name__ == "__main__":
    # ���ͳһ����
    if send_msg:
        wxpusher_notify(send_msg)