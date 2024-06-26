import dht
import json
from machine import Pin
from time import sleep
import socket


'''    顯示網頁    '''
def web_page():
    print(red, green, blue)
    if red.duty() == 0 and green.duty() == 0 and blue.duty() == 0: gpio_state = "OFF"
    else: gpio_state = "ON"

    html = """
    <!DOCTYPE html>
    <html lang="zh-Hant">

    <head>
        <meta charset="UTF-8">
        <title>溫溼度即時控制面板</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" type="image/png" href="https://i.ibb.co/cXWkK0c/itcnew.png">
        <style>
            html {
                font-family: Helvetica, Arial, sans-serif;
                display: inline-block;
                margin: 0px auto;
                text-align: center;
                background-color: #2E3440;
                /* Nord Polar Night */
                color: #D8DEE9;
                /* Nord Snow Storm */
            }

            h1 {
                color: #88C0D0;
                /* Nord Frost */
                padding: 2vh;
            }

            p {
                font-size: 1.5rem;
            }

            .button {
                display: inline-block;
                background-color: transparent;
                /* 背景設為透明 */
                border: 2px solid #5E81AC;
                /* 設定邊框顏色和厚度 */
                border-radius: 4px;
                color: #5E81AC;
                /* 改變文字顏色以搭配邊框 */
                padding: 16px 40px;
                text-decoration: none;
                font-size: 30px;
                margin: 10px;
                cursor: pointer;
            }

            .button2 {
                background-color: transparent;
                /* 背景設為透明 */
                border: 2px solid #BF616A;
                /* 設定邊框顏色和厚度 */
                color: #BF616A;
                /* 改變文字顏色以搭配邊框 */
            }

            .button3 {
                background-color: transparent;
                /* 背景設為透明 */
                border: 2px solid #EBCB8B;
                /* 設定邊框顏色和厚度 */
                color: #EBCB8B;
                /* 改變文字顏色以搭配邊框 */
            }

            .button4 {
                background-color: transparent;
                /* 背景設為透明 */
                border: 2px solid #A3BE8C;
                /* 設定邊框顏色和厚度 */
                color: #A3BE8C;
                /* 改變文字顏色以搭配邊框 */
            }

            table {
                margin: 20px auto;
                border-collapse: collapse;
                width: 50%;
                font-size: 1.2rem;
                color: #D8DEE9;
                /* Nord Snow Storm */
            }

            table,
            th,
            td {
                border: 1px solid #4C566A;
                /* Nord Polar Night */
            }

            th,
            td {
                padding: 12px;
                text-align: center;
            }

            th {
                background-color: #434C5E;
                /* Nord Polar Night */
            }

            #chartContainer {
                width: 80%;
                margin: 20px auto;
                display: flex;
                justify-content: space-around;
            }

            .chart {
                width: 45%;
            }

            /* 美化 range 輸入元素 */
            .slider {
                appearance: none;
                width: 80%;
                height: 15px;
                background: #4C566A;
                /* Nord Polar Night */
                outline: none;
                opacity: 0.7;
                transition: opacity .2s;
                border-radius: 5px;
                margin: 10px 0;
            }

            .slider:hover {
                opacity: 1;
            }

            .slider::-webkit-slider-thumb {
                appearance: none;
                width: 25px;
                height: 25px;
                background: #88C0D0;
                /* Nord Frost */
                cursor: pointer;
                border: none;
                border-radius: 4px;
            }

            .slider::-moz-range-thumb {
                width: 25px;
                height: 25px;
                background: #88C0D0;
                /* Nord Frost */
                cursor: pointer;
                border: none;
                border-radius: 4px;
            }

            .slider::-ms-thumb {
                width: 25px;
                height: 25px;
                background: #88C0D0;
                /* Nord Frost */
                cursor: pointer;
                border: none;
                border-radius: 4px;
            }

            .value {
                display: inline-block;
                width: 30px;
            }


            .icon {
                margin-right: 10px;
                vertical-align: middle;
            }

            .button .emoji {
                filter: grayscale(100%);
                /* emoji的初始灰階 */
            }

            .button:hover .emoji {
                filter: grayscale(0);
                /* hover時移除灰階 */
            }

            .button:hover {
                background-color: #5E81AC;
                /* 改為 Nord Frost Blue */
                color: #D8DEE9;
                /* 改為 Nord Snow Storm */
            }

            .button2:hover {
                background-color: #BF616A;
                /* 改為 Nord Red */
                color: #D8DEE9;
                /* 改為 Nord Snow Storm */
            }

            .button3:hover {
                background-color: #EBCB8B;
                color: #2E3440;
            }

            .button4:hover {
                background-color: #A3BE8C;
                color: #2E3440;
            }

            tr:hover {
                background-color: rgba(94, 129, 172, 0.3);
                /* 將背景色改為 30% 透明的 Nord Frost Blue */
                color: #D8DEE9;
                outline: 2px solid #88C0D0;
                outline-offset: -2px;
                cursor: pointer;
            }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/moment@2.29.1"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment@^1"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.17.0/xlsx.full.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2.0.5/FileSaver.min.js"></script>
        <script>
            var tempData = [];
            var humData = [];
            var labels = [];
            var maxDataPoints = 20;

            setInterval(updateData, 3000);

            function updateData() {
                fetch('http://""" + station.ifconfig()[0] + """/api/get-temp-hum')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('temp').innerText = `${data.temp} °C`;
                        document.getElementById('temp_f').innerText = `${data.temp_f} °F`;
                        document.getElementById('hum').innerText = `${data.hum} %`;

                        var now = new Date();
                        labels.push(now);
                        tempData.push(data.temp);
                        humData.push(data.hum);

                        if (labels.length > maxDataPoints) {
                            labels.shift();
                            tempData.shift();
                            humData.shift();
                        }

                        window.tempChart.update();
                        window.humChart.update();
                    })
                    .catch(error => console.error('Error fetching data:', error));
            }

            function updateLEDStatus(state) {
                document.getElementById('leddata').innerText = state;
            }

            function controllLEDV2(active) {
                var form = document.getElementById('ledForm');
                var formData = new FormData(form);
                var r = formData.get('red');
                var g = formData.get('green');
                var b = formData.get('blue');

                if (!active) {
                    r = 0;
                    g = 0;
                    b = 0;
                }
                console.log(r, g, b);

                fetch(`http://""" + station.ifconfig()[0] + """/api/led?r=${r}&g=${g}&b=${b}`)
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        updateLEDStatus(data.state); // 從伺服器回應中獲取 LED 狀態
                    })
                    .catch(error => console.error('Error controlling LED:', error));
            }

            window.onload = function () {
                var ctxTemp = document.getElementById('tempChart').getContext('2d');
                var ctxHum = document.getElementById('humChart').getContext('2d');
                window.tempChart = new Chart(ctxTemp, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: '溫度（°C）',
                            data: tempData,
                            borderColor: '#BF616A', /* Nord Red */
                            backgroundColor: 'rgba(191, 97, 106, 0.2)',
                            fill: true
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                type: 'time',
                                time: {
                                    unit: 'second'
                                },
                                grid: {
                                    color: '#4C566A' /* Nord Polar Night */
                                }
                            },
                            y: {
                                grid: {
                                    color: '#4C566A' /* Nord Polar Night */
                                }
                            }
                        }
                    }
                });

                window.humChart = new Chart(ctxHum, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: '溼度（%）',
                            data: humData,
                            borderColor: '#A3BE8C', /* Nord Green */
                            backgroundColor: 'rgba(163, 190, 140, 0.2)',
                            fill: true
                        }]
                    },
                    options: {
                        scales: {
                            x: {
                                type: 'time',
                                time: {
                                    unit: 'second'
                                },
                                grid: {
                                    color: '#4C566A' /* Nord Polar Night */
                                }
                            },
                            y: {
                                grid: {
                                    color: '#4C566A' /* Nord Polar Night */
                                }
                            }
                        }
                    }
                });
            };

            function randomizeRGB() {
                const redSlider = document.getElementById('redSlider');
                const greenSlider = document.getElementById('greenSlider');
                const blueSlider = document.getElementById('blueSlider');

                const redValue = Math.floor(Math.random() * 1024);
                const greenValue = Math.floor(Math.random() * 1024);
                const blueValue = Math.floor(Math.random() * 1024);

                redSlider.value = redValue;
                greenSlider.value = greenValue;
                blueSlider.value = blueValue;

                document.getElementById('redValue').innerText = redValue;
                document.getElementById('greenValue').innerText = greenValue;
                document.getElementById('blueValue').innerText = blueValue;

                controllLEDV2(true);
            }

            function exportToExcel() {
                let data = [];
                for (let i = 0; i < labels.length; i++) {
                    data.push({
                        '時間': labels[i].toLocaleString(),
                        '溫度 (°C)': tempData[i],
                        '溼度 (%)': humData[i]
                    });
                }

                let ws = XLSX.utils.json_to_sheet(data);
                let wb = XLSX.utils.book_new();
                XLSX.utils.book_append_sheet(wb, ws, '歷史資料');

                let wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'binary' });
                function s2ab(s) {
                    let buf = new ArrayBuffer(s.length);
                    let view = new Uint8Array(buf);
                    for (let i = 0; i < s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
                    return buf;
                }

                saveAs(new Blob([s2ab(wbout)], { type: "application/octet-stream" }), '歷史資料.xlsx');
            }

        </script>
    </head>

    <body>
        <h1>溫溼度即時控制面板</h1>

        <div>
            <span><button class="button" onclick="controllLEDV2(true)"><span class="emoji">💡</span></button></span>
            <span><button class="button button2" onclick="controllLEDV2(false)"><span
                        class="emoji">💤</span></button></span>
            <span><button class="button button3" onclick="randomizeRGB()"><span class="emoji">🎲</span></button></span>
            <span><button class="button button4" onclick="exportToExcel()"><span class="emoji">📊</span></button></span>
        </div>
        </div>

        <form id="ledForm">
            <div>
                R <span class="value" id="redValue">512</span>
                <input type="range" min="0" max="1023" name="red" class="slider" id="redSlider"
                    oninput="document.getElementById('redValue').innerText = this.value"><br>
            </div>
            <div>
                G <span class="value" id="greenValue">512</span>
                <input type="range" min="0" max="1023" name="green" class="slider" id="greenSlider"
                    oninput="document.getElementById('greenValue').innerText = this.value"><br>
            </div>
            <div>
                B <span class="value" id="blueValue">512</span>
                <input type="range" min="0" max="1023" name="blue" class="slider" id="blueSlider"
                    oninput="document.getElementById('blueValue').innerText = this.value"><br>
            </div>
        </form>

        <table>
            <tr>
                <td>攝氏溫度</td>
                <td id="temp">""" + str(temp) + """ °C</td>
            </tr>
            <tr>
                <td>華氏溫度</td>
                <td id="temp_f">""" + str(temp_f) + """ °F</td>
            </tr>
            <tr>
                <td>溼度</td>
                <td id="hum">""" + str(hum) + """ %</td>
            </tr>
            <tr>
                <td>LED狀態</td>
                <td id="leddata">""" + str(gpio_state) + """</td>
            </tr>

        </table>
        <div id="chartContainer">
            <div class="chart">
                <canvas id="tempChart"></canvas>
            </div>
            <div class="chart">
                <canvas id="humChart"></canvas>
            </div>
        </div>
    </body>

    </html>
    """

    return html


'''    更新 DHT11 資料    '''
def update_dht11_data():
    dht11.measure()
    temp = dht11.temperature()
    hum = dht11.humidity()
    temp_f = temp * (9/5) + 32.0
    print(temp, hum, temp_f)
    sleep(2.1)


'''    Return DHT11 資料給客戶端    '''
def api_response():
    data = {
        'temp': dht11.temperature(),
        'hum': dht11.humidity(),
        'temp_f': dht11.temperature() * (9/5) + 32.0
    }

    return 'HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n' + json.dumps(data)


def led_api_response(r, g, b):
    red.duty(r)
    green.duty(g)
    blue.duty(b)
    
    if r == 0 and g == 0 and b == 0:
        state = "OFF"
    else:
        state = "ON"

    data = {
        'Success': 'True',
        'state': state
    }

    return 'HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n' + json.dumps(data)


'''    Web Server 主程式    '''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
s.setblocking(False)


'''    ESP32 主程式    '''
while True:
    try:
        update_dht11_data()

        conn, addr = s.accept()
        print('------------------------------')
        print('客戶端 %s 已連線' % str(addr))
        print('------------------------------\n')



        request = conn.recv(1024)
        request = str(request)

        if request.find('/api/led') == 6:
            try:
                params = request.split('?')[1].split(' ')[0]
                params_dict = dict(x.split('=') for x in params.split('&'))
                r = int(params_dict.get('r', 0))
                g = int(params_dict.get('g', 0))
                b = int(params_dict.get('b', 0))
                response = led_api_response(r, g, b)
            except Exception as e:
                response = 'HTTP/1.1 400 Bad Request\n\n' + str(e)
                
            response = led_api_response(r, g, b)
            conn.send(response.encode())
            conn.close()
        elif request.find('/api/get-temp-hum') == 6:
            response = api_response()
            conn.send(response.encode())
            conn.close()
        else:
            temp = dht11.temperature()
            temp_f = temp * (9/5) + 32.0
            hum = dht11.humidity()
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n'.encode())
            conn.send('Content-Type: text/html; charset=UTF-8\n'.encode()) # 改成 UTF-8，可以正常顯示中文
            conn.send('Connection: close\n\n'.encode())
            conn.sendall(response.encode())
            conn.close()

    except OSError as e:
        if e.args[0] == 11: # EAGAIN，處理沒有客戶端連接時的狀況
            print('sleep!')
            sleep(0.001) # 短暫休眠，避免CPU佔用過高
            continue

        elif e.args[0] == 116: # ETIMEDOUT，處理 DHT11 讀不到數值時的狀況
            print('timeout!')
            sleep(0.001) # 短暫休眠，等待 DHT11 恢復正常
            continue
