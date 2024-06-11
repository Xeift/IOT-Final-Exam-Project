#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>


#define SCREEN_WIDTH 128 // OLED display width
#define SCREEN_HEIGHT 64 // OLED display height
#define OLED_RESET     -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET); // Declaration for SSD1306

const char* ssid     = "Xeift";
const char* password = "13241324";  

std::tuple<String, String, String> getDHT11Data();

void setup() {
    Serial.begin(9600);
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    delay(2000);
    display.clearDisplay();
    display.setTextColor(WHITE);

    // Connect to Wi-Fi
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.print("Connecting to: ");
    display.println(ssid);
    display.display(); 
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
        display.print(".");
        display.display(); 
    }

    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.print("Connected!");
    display.println("IP: ");
    display.println(WiFi.localIP());
    display.print("Ready to display =w=");
    display.display(); 
}

std::tuple<String, String, String> getDHT11Data() {
    HTTPClient http;
    http.begin("http://192.168.242.51/api/get-temp-hum");
    int httpCode = http.GET();

    if (httpCode > 0) {
        String payload = http.getString();
        http.end();
        DynamicJsonDocument doc(1024);
        deserializeJson(doc, payload);

        double temp_f = doc["temp_f"];
        double hum = doc["hum"];
        double temp = doc["temp"];

        String temp_f_str = String(temp_f);
        String hum_str = String(hum);
        String temp_str = String(temp);

        return std::make_tuple(temp_f_str, hum_str, temp_str);
    }
    else {
        Serial.println(httpCode);
        http.end();
        return std::make_tuple("-1.0", "-1.0", "-1.0");
    }
}

void loop() {
    auto [temp_f, hum, temp] = getDHT11Data();

    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.print(temp);
    display.println("  C");
    display.println(temp_f + "  F");
    display.println(hum + "% Hum");
    display.display();

    delay(2100);
}

