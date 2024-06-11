import dht
import json
from machine import Pin
from time import sleep
import socket


led = Pin(2, Pin.OUT)
dht11 = dht.DHT11(Pin(14))


'''    顯示網頁    '''
def web_page():
    if led.value() == 1:
        gpio_state = "ON"
    else:
        gpio_state = "OFF"

    html = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <title>ESP Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" type="image/png" href="https://cdn.discordapp.com/attachments/936236816141541408/1249975125290385408/itcnew.png?ex=6669418d&is=6667f00d&hm=2c49a94eabc06b8fffd954c7b1b273e1e623a8b8d04f5db0ac7c63e00da9f681&">
    <style>
        html {
            font-family: Helvetica, Arial, sans-serif;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
            background-color: #2E3440; /* Nord Polar Night */
            color: #D8DEE9; /* Nord Snow Storm */
        }
        h1 {
            color: #88C0D0; /* Nord Frost */
            padding: 2vh;
        }
        p {
            font-size: 1.5rem;
        }
        .button {
            display: inline-block;
            background-color: #5E81AC; /* Nord Frost */
            border: none;
            border-radius: 4px;
            color: #ECEFF4; /* Nord Snow Storm */
            padding: 16px 40px;
            text-decoration: none;
            font-size: 30px;
            margin: 10px;
            cursor: pointer;
        }
        .button2 {
            background-color: #BF616A; /* Nord Red */
        }
        table {
            margin: 20px auto;
            border-collapse: collapse;
            width: 50%;
            font-size: 1.2rem;
            color: #D8DEE9; /* Nord Snow Storm */
        }
        table, th, td {
            border: 1px solid #4C566A; /* Nord Polar Night */
        }
        th, td {
            padding: 12px;
            text-align: center;
        }
        th {
            background-color: #434C5E; /* Nord Polar Night */
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
            background: #4C566A; /* Nord Polar Night */
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
            background: #88C0D0; /* Nord Frost */
            cursor: pointer;
            border: none;
            border-radius: 4px;
        }
        .slider::-moz-range-thumb {
            width: 25px;
            height: 25px;
            background: #88C0D0; /* Nord Frost */
            cursor: pointer;
            border: none;
            border-radius: 4px;
        }
        .slider::-ms-thumb {
            width: 25px;
            height: 25px;
            background: #88C0D0; /* Nord Frost */
            cursor: pointer;
            border: none;
            border-radius: 4px;
        }
        .icon {
            margin-right: 10px;
            vertical-align: middle;
        }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/moment@2.29.1"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment@^1"></script>
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
                })
                .catch(error => console.error('Error controlling LED:', error));
        }

        window.onload = function() {
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
    </script>
</head>
<body>
    <h1>ESP Web Server</h1>
    <p>GPIO state: <strong id="gpio_state">""" + str(gpio_state) + """</strong></p>

    <div>
        <span><button class="button" onclick="controllLEDV2(true)"><img src="https://img.icons8.com/ios-filled/50/ffffff/light-on.png" class="icon">ON</button></span>
        <span><button class="button button2" onclick="controllLEDV2(false)"><img src="https://img.icons8.com/ios-filled/50/ffffff/light-off.png" class="icon">OFF</button></span>
    </div>

    <form id="ledForm">
        <div>
            R: <input type="range" min="0" max="1023" name="red" class="slider"><br>
        </div>
        <div>
            G: <input type="range" min="0" max="1023" name="green" class="slider"><br>
        </div>
        <div>
            B: <input type="range" min="0" max="1023" name="blue" class="slider"><br>
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


'''    LED API 回應    '''
def led_api_response(r, g, b):
    red.duty(r)
    green.duty(g)
    blue.duty(b)

    data = {
        'Success': 'True'
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
            # TODO: 解析參數
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
