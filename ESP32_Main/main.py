import dht
import json
from machine import Pin
from time import sleep

def web_page(temp, hum, temp_f):  # 顯示網頁 html 內容
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
            <scrip>
              setInterval(updateData, 5000);
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
              <td>""" + str(temp) + """</td>
          </tr>
            <tr>
              <td>Humifity</td>
              <td>""" + str(hum) + """</td>
          </tr>
            <tr>
              <td>Fahrenheit temperature</td>
              <td>""" + str(temp_f) + """</td>
          </tr>
          </table>
        </body>
    </html>
    """

    return html


def read_sensor():
    dht11.measure()
    temp = dht11.temperature()
    hum = dht11.humidity()
    temp_f = temp * (9/5) + 32.0
    return temp, hum, temp_f


def api_response(temp, hum, temp_f):
    data = {
        'temp': temp,
        'hum': hum,
        'temp_f': temp_f
    }
    return 'HTTP/1.1 200 OK\nContent-Type: application/json\nConnection: close\n\n' + json.dumps(data)

# Web Server 主程式
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 新增 SO_REUSEADDR，解決 address in use 的報錯
s.bind(('', 80))
s.listen(5)  # 監聽 80 port


while True:
    conn, addr = s.accept()  # 當網頁端連接時
    print('------------------------------')
    print('客戶端 %s 已連線' % str(addr))
    print('------------------------------\n')
    
    request = conn.recv(1024)
    request = str(request)

    led_on = request.find('/?led=on')  # 確定目前 led 燈是否開啟
    led_off = request.find('/?led=off')
    
    if led_on == 6:  # 如果開啟就顯示 LED ON
        print('LED ON')
        led.value(1)
        
    if led_off == 6:
        print('LED OFF')
        led.value(0)

    if request.find('/api/get-temp-hum') == 6:
        print('asdasdasdsadasdsa')
        temp, hum, temp_f = read_sensor()
        response = api_response(temp, hum, temp_f)
        conn.send(response)
        conn.close()
        
    else:
        sleep(2)
        sensor = dht11
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9/5) + 32.0
        print('Temperature: %3.1f C' %temp)
        print('Temperature: %3.1f F' %temp_f)
        print('Humidity: %3.1f %%' %hum)


        response = web_page(temp,hum,temp_f) # 顯示網頁
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response) # return 網頁
        conn.close()

