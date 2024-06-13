# IOT-Final-Exam-Project
人工智慧與物聯網期末專題

# 檔案目錄說明
`ESP32C3_Glass` 眼鏡的程式碼，使用 Arduino 和 C++。

`ESP32_Main` 溫溼度感測器 + RGB LED + Web Server 的程式碼，使用 Thonny 和 MicroPython。

`images` 截圖。

# 功能與改進部分
在眼鏡上可以即時顯示溫溼度，網頁端新增了即時圖表 + 隨機調色 + 導出歷史溫溼度資料成 Excel 檔案的功能。眼鏡使用 Seeed Studio XIAO ESP32C3 這塊開發板（另外買的），與 ESP 通訊。眼鏡使用的材料參考：https://github.com/Xeift/Arduino-Crypto-Glass。

| 編號 | 改進部分 |
| --- | ------- |
|  1  | 在 ESP32 上新增 API，透過 API 將即時資訊顯示在眼鏡上 |
|  2  | 網頁上每 2 秒自動更新溫溼度 |
|  3  | 網頁上記錄溫溼度並導出成 excel |
|  4  | 網頁上新增即時圖表 |
|  5  | CSS 最佳化，改用 Nord 主題 |
|  6  | 結合 LED 顯示，可以開燈、關燈、產生隨機的 RGB 組合 |
|  7  | 新增 SO_REUSEADDR，解決 address in use 的報錯 |
|  8  | 改成 UTF-8 編碼，可以正常顯示中文 |
|  9  | 新增網頁 icon |
|  10 | 修正了調光時會超出範圍的報錯 |
|  11 | LED 狀態也改成即時更新，不需要再重新整理網頁才能刷新。|

# 截圖
Web 控制界面
![Web.jpg](https://github.com/Xeift/IOT-Final-Exam-Project/raw/main/images/Web.png)

開發板實體接線圖
![Board.jpg](https://github.com/Xeift/IOT-Final-Exam-Project/raw/main/images/Board.jpg)

眼鏡實體圖（近）
![Glass.jpg](https://github.com/Xeift/IOT-Final-Exam-Project/raw/main/images/Glass.jpg)

眼鏡實體圖（遠）
![Glass2.jpg](https://github.com/Xeift/IOT-Final-Exam-Project/raw/main/images/Glass2.jpg)

導出 Excel
![Excel.jpg](https://github.com/Xeift/IOT-Final-Exam-Project/raw/main/images/Excel.png)

Arduino IDE
![ArduinoIDE.png](https://github.com/Xeift/IOT-Final-Exam-Project/raw/main/images/ArduinoIDE.png)

Thonny IDE
![Thonny.png](https://github.com/Xeift/IOT-Final-Exam-Project/raw/main/images/Thonny.png)