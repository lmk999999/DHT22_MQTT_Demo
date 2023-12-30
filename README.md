# DHT22_MQTT_Demo

## 簡介
本程式範本僅用於技術應用測試，與程式碼紀錄。
### main.py
主要程式碼，獲取 DHT22 的溫度與濕度數據後，透過 MQTT 發送。

### 接線圖
![接線架構圖](/document/20230205-01_架構圖.png)

## 版本
- 模組版本：`version 1.0`
- 更新日期：`2023-12-30`

## 使用套件
- paho-mqtt
- adafruit_dht
- board
- digitalio

## 參考資料
- [Digital humidity and temperature sensor AM2302](/document/Digital+humidity+and+temperature+sensor+AM2302.pdf)