#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>

const char* ssid = "AA"; //name of wifi
const char* password = "BB";  //password of wifi

// Render API endpoint
const char* serverName = "https://project-api-am.onrender.com/api/v1/sensors/data";

//
// Data wire is plugged into GPIO port 4 on the ESP32
#define ONE_WIRE_BUS 4

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  
  sensors.begin();

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nSuccessfully connected to WiFi network!");
}

void loop() {
  // Only try to send data if the Wi-Fi is connected
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;

    // Issue a global temperature request to all devices on the bus
    sensors.requestTemperatures(); 
    
    // Read the temperature in Celsius
    float t = sensors.getTempCByIndex(0);

    // Error handling: Dallas sensors return -127.00 if they are disconnected or wired incorrectly
    if (t <= -100.0) {
      Serial.println("Failed to read from DS18B20 sensor! Check your wiring.");
      delay(2000);
      return; 
    }

    // Initialize the HTTP client
    http.begin(serverName);

    // Sending JSON data
    http.addHeader("Content-Type", "application/json");

    // Package the data into a JSON string
    String jsonPayload = "{\"sensor_id\":\"ESP32_NODE_01\",\"temperature\":" + String(t) + ",\"status\":\"active\"}";
    
    Serial.print("Sending payload: ");
    Serial.println(jsonPayload);

    // Send the POST request to the internet
    int httpResponseCode = http.POST(jsonPayload);

    // Print the server's response
    if (httpResponseCode > 0) {
      Serial.print("Server Responded: ");
      Serial.print(httpResponseCode);
      Serial.print(" - ");
      Serial.println(http.getString());
    } else {
      Serial.print("Error sending request: ");
      Serial.println(httpResponseCode);
    }
    
    // Free resources to prevent memory leaks
    http.end();
  } else {
    Serial.println("WiFi Disconnected. Reconnecting...");
  }
  
  // Wait 5 seconds before reading and sending the next data point
  delay(5000);
}