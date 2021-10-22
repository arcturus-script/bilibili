import requests
import push
import os
import re
import time
from API import video_info_url, BiliBili_login_url, live_broadcast_url, Comics, Comics_info, recommend, video_Share, add_coin, video_click, video_heartbeat
'''
实现的功能
1.获取视频信息
2.获取用户信息
3.直播签到
4.漫画签到
5.投币
6.分享视频
7.每日看视频
'''
# Cookies
Cookies = os.getenv('Cookies').split(',')
# csrf = os.getenv('csrf').split(',')
# uid = os.getenv('uid').split(',')
# sid = os.getenv('sid').split(',')

# 正则好像有点 bug (╯▔皿▔)╯
csrf, uid, sid = [], [], []
for i in Cookies:
    csrf.append(re.findall('(?<=bili_jct=)(.+?);', i)[0])
    uid.append(re.findall('(?<=DedeUserID=)(.+?);', i)[0])
    sid.append(re.findall('(?<=sid=)(.+?);', i)[0])

# UA
UserAgent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/94.0.4606.81'


# 获取视频信息
def get_video_info(bv):
    params = {'bvid': bv}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': UserAgent
    }
    rep = requests.get(video_info_url, params=params, headers=headers).json()
    if rep['code'] == 0:
        data = rep['data']
        video_info = {
            'bvid': data['bvid'],  # 视频 BV 号
            'aid': data['aid'],  # 视频 AV 号
            'duration': data['duration'],
            'cid': data['cid']
        }
        return {'status': True, 'video_info': video_info}
    else:
        return {'status': False, 'message': rep['message']}


# 获取用户信息
def get_user_info(headers):
    rep = requests.get(BiliBili_login_url, headers=headers).json()

    if rep['code'] == 0:
        data = rep['data']
        level = data['level_exp']

        userInfo = {
            'name': data['name'],  # 用户名
            'level': data['level'],  # 等级
            'coins': data['coins'],  # 硬币数
            'level_exp': '%d/%d' % (level['current_exp'], level['next_exp']),
            'silence': data['silence']
        }

        return {'status': True, 'userInfo': userInfo}
    else:
        return {'status': False, 'message': rep['message']}


# 直播签到
def live_broadcast_checkin(headers):
    rep = requests.get(live_broadcast_url, headers=headers).json()

    if rep['code'] == 0:
        # 签到成功
        data = rep['data']
        print('直播签到成功🎉🎉')
        print('获得奖励:%s' % data['text'])
        info = {'raward': data['text'], 'specialText': data['specialText']}
        return {'status': True, 'info': info}
    else:
        print('直播签到失败,因为%s' % rep['message'])
        return {'status': False, 'message': rep['message']}


# 漫画签到
def comics_checkin(headers):
    data = {'platform': 'android'}
    rep = requests.post(Comics, headers=headers, data=data).json()
    if rep['code'] == 0:
        print('漫画签到成功🎉🎉')
        p = comics_checkin_info(Cookies)
        if p['status']:
            return {
                'status': True,
                'message': '签到成功',
                'day_count': p['day_count']
            }
    elif rep['code'] == 'invalid_argument':
        print('漫画签到失败,因为重复签到了')
        return {'status': False, 'message': '重复签到啦'}


# 查看漫画签到信息
def comics_checkin_info(headers):
    rep = requests.post(Comics_info, headers=headers).json()
    if rep['code'] == 0:
        return {'status': True, 'day_count': rep['data']['day_count']}
    else:
        return {'status': False, 'message': rep['msg']}


# 获取推荐视频列表
def video_suggest(num):
    params = {'tid': 23, 'order': 'new'}
    rep = requests.get(recommend, params=params).json()
    if rep['code'] == 0:
        vdict = {}
        vlist = rep['list']
        for index, item in enumerate(vlist):
            # 将视频主要信息保存到字典里
            v = {'aid': item['aid'], 'title': item['title']}
            vdict.update({index: v})
        return {'status': True, 'video_list': vdict}
    else:
        return {'status': False, 'msg': '获取推荐视频失败惹😥'}


# 投币
def give_coin(p, want_coin_num, headers, csrf, coinnum=1, select_like=0):
    has_coin_num = 0  # 已经投币次数
    list = {}
    for index, item in enumerate(p['video_list'].values()):
        data = {
            'aid': str(item['aid']),
            'multiply': coinnum,  # 每次投币多少个,默认 1 个
            'select_like': select_like,  # 是否同时点赞, 默认不点赞
            'cross_domain': 'true',
            'csrf': csrf
        }
        # 当已投币数超过想投币数时退出
        if has_coin_num < want_coin_num:
            rep = requests.post(add_coin, headers=headers, data=data).json()
            if rep['code'] == 0:
                # 投币成功
                print('给[%s]投币成功🎉🎉' % item['title'])
                list.update({index: {'status': True, 'title': item['title']}})
                has_coin_num = has_coin_num + 1  # 投币次数加 1
            else:
                # 投币失败
                print('给[%s]投币失败😥😥,因为%s' % (item['title'], rep['message']))
                list.update({index: {'status': False, 'title': item['title']}})
        else:
            print('投币完成,正在退出')
            break
    return list


# 分享视频
def share_video(p, headers, csrf):
    for item in p['video_list'].values():
        # 分享视频
        data = {'aid': item['aid'], 'csrf': csrf}
        rep = requests.post(video_Share, data=data, headers=headers).json()
        if rep['code'] == 0:
            # 如果分享成功,退出循环
            # 并返回分享的视频名
            print('分享视频[%s]成功🎉🎉' % item['title'])
            return {'status': True, 'msg': item['title']}
        else:
            print('分享视频[%s]失败,因为%s' % (item['title'], rep['message']))
    # 循环结束都没分享成功,返回分享失败
    print('分享视频失败😥😥')
    return {'status': False}


# 每日看视频
def watch(bvid, headers, uid, csrf):
    p = get_video_info(bvid)
    # 获取视频信息成功
    if p['status']:
        info = p['video_info']
        data = {
            'aid': info['aid'],
            'cid': info['cid'],
            'part': 1,
            'ftime': int(time.time()),
            'jsonp': "jsonp",
            'mid': uid,
            'csrf': csrf,
            'stime': int(time.time()),
        }
        rep = requests.post(video_click, data=data, headers=headers).json()

        # 进入视频页
        if rep['code'] == 0:
            data = {
                'aid': info['aid'],
                'cid': info['cid'],
                'jsonp': 'jsonp',
                'mid': uid,
                'csrf': csrf,
                'played_time': 0,
                'pause': False,
                'play_type': 1,
                'realtime': info['duration'],
                'start_ts': int(time.time()),
            }
            rep = requests.post(video_heartbeat, data=data,
                                headers=headers).json()

            if rep['code'] == 0:
                # 模拟看过视频
                time.sleep(5)
                data['played_time'] = info['duration'] - 1
                data['play_type'] = 0
                data['start_ts'] = int(time.time())
                rep = requests.post(video_heartbeat,
                                    data=data,
                                    headers=headers).json()

                if rep['code'] == 0:
                    print('观看视频成功🎉🎉')
                    return True
        print('观看视频失败惹😥😥')
        return False


def start():
    push_type = os.getenv('push_type', '0')
    want_watch = os.getenv('want_watch', '').split(',')
    want_coin_num = os.getenv('want_coin_num', '').split(',')
    want_share_num = os.getenv('want_share_num', '').split(',')
    want_comics_checkin = os.getenv('want_comics_checkin', '').split(',')
    want_lb_checkin = os.getenv('want_lb_checkin', '').split(',')

    msg = []
    for cindex, c in enumerate(Cookies):
        # 响应头
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': c,
            'Referer': 'https://www.bilibili.com/',
            'User-Agent': UserAgent
        }

        # 获取用户信息
        user = get_user_info(headers)
        if user['status']:
            userInfo = user['userInfo']
            content = '等级：lv%d\n硬币：%d\n经验：%s\n' % (
                userInfo['level'], userInfo['coins'], userInfo['level_exp'])
            print(content)
            # 配置需观看的视频 BV 号
            bvid = os.getenv('bvid', 'BV1if4y1g7Qp')
            if bvid and want_watch[cindex] == '1':
                # 如果 bvid 存在,且 is_watch 不是 '0'
                # 说明想要看视频
                print('正在观看视频...')
                is_watch = watch(bvid, headers, uid[cindex], csrf[cindex])
            else:
                print('不进行观看...')
                is_watch = False
            # 获取 50 个推荐视频
            p = video_suggest(50)
            if p['status']:
                print('获取 50 个视频成功🎉🎉')
                # 投币,默认不投币
                try:
                    wcn = int(want_coin_num[cindex])
                    print('今日欲投 %d 个硬币' % wcn)
                except (IndexError, ValueError):
                    wcn = 0
                    print('今日欲投 %d 个硬币' % wcn)
                coin_list = give_coin(p, wcn, headers, csrf[cindex])
                # 随机分享视频,默认不分享视频
                try:
                    wsn = want_share_num[cindex]
                except IndexError:
                    wsn = '0'
                if wsn == '1':
                    # 如果 want_share_num 是 '1'
                    # 说明需要分享
                    print('正在分享视频...')
                    is_share = share_video(p, headers, csrf[cindex])
                else:
                    print('今日不分享视频...')
                    is_share = {'status': False}
            else:
                print('获取视频失败😥😥')
                is_share = {'status': False}
                coin_list = {}

            # 漫画签到,默认不签到
            try:
                wcc = want_comics_checkin[cindex]
            except IndexError:
                wcc = '0'
            if wcc == '1':
                print('正在进行漫画签到...')
                cm = comics_checkin(headers)
            else:
                print('不启用漫画签到...')
                cm = {'status': False, 'message': '未启用'}

            # 直播签到,默认不签到
            try:
                wlc = want_lb_checkin[cindex]
            except IndexError:
                wlc = '0'
            if wlc == '1':
                print('正在尝试直播签到...')
                lb = live_broadcast_checkin(headers)
            else:
                print('今日不进行直播签到...')
                lb = {'status': False, 'message': '未启用'}

            # 开始推送
            if is_watch:
                content = content + '\n观看视频：完成'

            if is_share['status']:
                content = content + '\n分享视频[%s]：完成' % is_share['msg']

            if len(coin_list) != 0:
                for i in coin_list.values():
                    if i['status']:
                        content = content + '\n给视频[%s]投币：成功' % i['title']
                    else:
                        content = content + '\n给视频[%s]投币：失败' % i['title']
            if cm['status']:
                content = content + '\n漫画：%s\n连续签到：%d天' % (cm['message'],
                                                           cm['day_count'])
            else:
                content = content + '\n漫画未签到,因为：%s' % cm['message']

            if lb['status']:
                lb_info = lb['info']
                content = content + '\n直播签到成功\n今日奖励：%s\n其他：%s' % (
                    lb_info['raward'], lb_info['specialText'])
            else:
                content = content + '\n直播未签到,因为：%s' % lb['message']

            if push_type == '1':
                qiye_push_msg(content, userInfo['name'])
            else:
                msg.append('## %s\n%s\n' % (userInfo['name'], content))
        else:
            print('Cookies 失效啦')
            if push_type == '1':
                qiye_push_msg('Cookies 失效啦')
            else:
                msg.append('Cookies 失效啦')

    print('\n'.join(msg))
    if push_type != '0':
        if push_type == '2':
            key = os.getenv('key')
            p = push.server(key)
            p.push_message('BiliBili', '\n'.join(msg))
        elif push_type == '3':
            key = os.getenv('key')
            p = push.pushplus(key)
            p.push_message('BiliBili', '\n'.join(msg))


def qiye_push_msg(content, username=''):
    # 企业微信推送
    AgentId = os.getenv('AgentId')  # 应用 ID
    Secret = os.getenv('Secret')  # 应用密钥
    EnterpriseID = os.getenv('EnterpriseID')  # 企业 ID
    Touser = os.getenv('Touser', '@all')  # 用户 ID
    p = push.qiye_wechat(AgentId, Secret, EnterpriseID, Touser)
    p.push_text_message('BiliBili', content, username)


def main(*arg):
    return start()


if __name__ == '__main__':
    main()
