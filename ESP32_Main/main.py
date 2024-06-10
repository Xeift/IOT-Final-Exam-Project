import dht
import json
from machine import Pin
from time import sleep


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
                    margin: 20px auto; /* Center the table */
                    border-collapse: collapse;
                    width: 50%;
                    font-size: 1.2rem;
                }
                table, th, td {
                    border: 1px solid black;
                }
                th, td {
                    padding: 12px;
                    text-align: center; /* Center text in table cells */
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
            <script>
              setInterval(updateData, 2200);

              function updateData() {
                fetch(\'http://""" + station.ifconfig()[0] + """/api/get-temp-hum\')
                  .then(response => response.json())
                  .then(data => {
                    document.getElementById('temp').innerText = data.temp;
                    document.getElementById('hum').innerText = data.hum;
                    document.getElementById('temp_f').innerText = data.temp_f;
                  })
                  .catch(error => console.error('Error fetching data:', error));
              }
            </script>
        </head>
        <body>
            <h1>ESP Web Server</h1>
            <p>GPIO state: <strong>""" + str(gpio_state) + """</strong></p>
            <p><a href="/?led=on"><button class="button">ON</button></a></p>
            <p><a href="/?led=off"><button class="button button2">OFF</button></a></p>
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


'''    Web Server 主程式    '''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 新增 SO_REUSEADDR，解決 address in use 的報錯
s.bind(('', 80))
s.listen(5)  # 監聽 80 port
s.setblocking(False)  # 設置為非阻塞模式


'''    ESP32 主程式    '''
while True:
    try:
        update_dht11_data()
    

        conn, addr = s.accept()  # 當網頁端連接時
        print('------------------------------')
        print('客戶端 %s 已連線' % str(addr))
        print('------------------------------\n')

        request = conn.recv(1024)
        request = str(request)


        if request.find('/?led=on') == 6:
            led.value(1)
            
        elif request.find('/?led=off') == 6:
            led.value(0)

        elif request.find('/api/get-temp-hum') == 6: #
            response = api_response()
            conn.send(response)
            conn.close()
            
        else:
            temp = dht11.temperature()
            temp_f = temp * (9/5) + 32.0
            hum = dht11.humidity()
            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response) # return 網頁
            conn.close()


        '''    處理例外情況    '''
    except OSError as e:
        
        if e.args[0] == 11: # EAGAIN，處理沒有客戶端連接時的狀況
            print('sleep!')
            sleep(0.001) # 短暫休眠，避免CPU佔用過高
            continue

        elif e.args[0] == 116: # ETIMEDOUT，處理 DHT11 讀不到數值時的狀況
            print('timeout!')
            sleep(1) # 暫停一下，等待 DHT11 恢復正常
            continue

