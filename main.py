# MQTT 函式庫
import paho.mqtt.client as mqtt

import datetime
import time

# Adafruit CircuitPython 函式庫
import adafruit_dht
import board
import digitalio

# === 選擇設定參數 =====================================

# 系統模式（0= 工作計算模式 ,1=背景學習模式）
pmv_system_mode = 1
# 變數設定
brokerIP = "192.168.10.32"
brokerTCP = 1883
brokerTIME = 60

version = "0.1.0"

main_topic = "mqtttopic"

# === 啟動操作 =====================================

# MQTT Broker 連線設定
client = mqtt.Client()
client.connect(brokerIP, brokerTCP, brokerTIME)
# 三個項目分別是 Broker-IP位址、Broker-連接埠、Broker-等待時間，只需要更改 IP 位址即可。

# 設定時間格式，傳輸數據時間用
ISOTIMEFORMAT = '%m/%d %H:%M:%S'

# 讀取 DHT22 資料使用 GPIO 17 (編號)
dht_device = adafruit_dht.DHT22(board.D17)

# === 主計算 =====================================

# 讀取跳針頻道 https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/gpio
gpio = []
gpio.append(digitalio.DigitalInOut(board.D27))
gpio.append(digitalio.DigitalInOut(board.D22))
gpio.append(digitalio.DigitalInOut(board.D5))
gpio.append(digitalio.DigitalInOut(board.D6))

for gpio_i in range(4):
        gpio[gpio_i].direction = digitalio.Direction.INPUT

# 讀取 DHT22 資料使用 GPIO 17 (編號)
dht_device = adafruit_dht.DHT22(board.D17, use_pulseio=False)

while True:
        timenow = datetime.datetime.now().strftime(ISOTIMEFORMAT)

        channel_int = 0

        # 讀取跳針狀態確認頻道。
        for gpio_i in range(4):
                if   gpio[gpio_i].value: channel_int = ( channel_int << 1 ) + 1
                else : channel_int = ( channel_int << 1 ) + 0

        # 讀取 DHT22 的溫度、濕度，如果不成功將會重複嘗試直到成功。
        if dht_device:
                while True:
                        try:
                                tem = dht_device.temperature
                                hum = dht_device.humidity
                        except:
                                time.sleep(1)
                        else:
                                timenow = datetime.datetime.now().strftime(ISOTIMEFORMAT)
                                break
        
        # 確認獲取新資料將會將資訊送到 Broker，並且重置資料。
        if not tem == None and not hum == None :
                timeaft = timenow
                print ("Channel: {:0>2d} . Time : {} . AirTemperature: {:3.1f}℃ Humidity: {:0>2.1f}% .".format(channel_int , timenow , tem , hum ),end="\r",flush=False)
                
                # 發布訊息到 MQTT Broker 上，主題可自行修改。
                mqtt_output_list = []
                mqtt_output_list.append(timenow)
                mqtt_output_list.append(time.time())
                mqtt_output_list.append("{:3.1f}".format(tem))
                mqtt_output_list.append("{:0>2.1f}".format(hum))
                client.publish(main_topic + "dht22/val", str(mqtt_output_list))

                tem = None
                hum = None

        time.sleep(1)


