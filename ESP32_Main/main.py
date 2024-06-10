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
    <html>
        <head>
            <title>ESP Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,">
            <style>
                html {
                    font-family: Helvetica;
                    display: inline-block;
                    margin: 0px auto;
                    text-align: center;
                }
                h1 {
                    color: #0F3376;
                    padding: 2vh;
                }
                p {
                    font-size: 1.5rem;
                }
                .button {
                    display: inline-block;
                    background-color: #e7bd3b;
                    border: none;
                    border-radius: 4px;
                    color: white;
                    padding: 16px 40px;
                    text-decoration: none;
                    font-size: 30px;
                    margin: 2px;
                    cursor: pointer;
                }
                .button2 {
                    background-color: #4286f4;
                }
                table {
                    margin: 20px auto;
                    border-collapse: collapse;
                    width: 50%;
                    font-size: 1.2rem;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 12px;
                    text-align: center;
                }
                th {
                    background-color: #f2f2f2;
                }
                #chartContainer {
                    width: 80%;
                    margin: 20px auto;
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
                    document.getElementById('temp').innerText = data.temp;
                    document.getElementById('hum').innerText = data.hum;
                    document.getElementById('temp_f').innerText = data.temp_f;

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

              function controlLED(state) {
                fetch('http://""" + station.ifconfig()[0] + """/api/led/' + state)
                  .then(response => response.json())
                  .then(data => {
                    document.getElementById('gpio_state').innerText = data.led_state;
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
                      label: 'Temperature (°C)',
                      data: tempData,
                      borderColor: 'rgba(255, 99, 132, 1)',
                      backgroundColor: 'rgba(255, 99, 132, 0.2)',
                      fill: true
                    }]
                  },
                  options: {
                    scales: {
                      x: {
                        type: 'time',
                        time: {
                          unit: 'second'
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
                      label: 'Humidity (%)',
                      data: humData,
                      borderColor: 'rgba(54, 162, 235, 1)',
                      backgroundColor: 'rgba(54, 162, 235, 0.2)',
                      fill: true
                    }]
                  },
                  options: {
                    scales: {
                      x: {
                        type: 'time',
                        time: {
                          unit: 'second'
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
            <p><button class="button" onclick="controlLED('on')">ON</button></p>
            <p><button class="button button2" onclick="controlLED('off')">OFF</button></p>
            <table>
            <tr>
              <td>Celsius temperature</td>
              <td id="temp">""" + str(temp) + """</td>
            </tr>
            <tr>
              <td>Humidity</td>
              <td id="hum">""" + str(hum) + """</td>
            </tr>
            <tr>
              <td>Fahrenheit temperature</td>
              <td id="temp_f">""" + str(temp_f) + """</td>
            </tr>
            </table>
            <div id="chartContainer">
                <canvas id="tempChart"></canvas>
                <canvas id="humChart"></canvas>
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


'''    LED 開/關 API 回應    '''
def led_api_response(state):
    if state == "on":
        led.value(1)
    elif state == "off":
        led.value(0)

    data = {
        'led_state': "ON" if led.value() == 1 else "OFF"
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

        if request.find('/api/led/on') == 6:
            response = led_api_response("on")
            conn.send(response.encode())
            conn.close()
        elif request.find('/api/led/off') == 6:
            response = led_api_response("off")
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
