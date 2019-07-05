#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <MQ2.h>

void sendData(float);

int pin = 32;
float lpg, co, smoke;

//  MQ2 mq2(pin);

double val = 0;

const char* ssid     = "node343";
const char* password = "xyz10000";


const char* host = "script.google.com";
const int httpsPort = 443;

WiFiClientSecure client;            
// SHA1 fingerprint of the certificate, don't care with your GAS service

//https://script.google.com/macros/s/AKfycbxL8I2JytDN3q6UmgFoinArTptYlnxZEd__igfroDkqaYArXHFs/exec
const char* fingerprint = "46 B2 C3 44 9C 59 09 8B 01 B6 F8 BD 4C FB 00 74 91 2F EF F6";
String GAS_ID = "AKfycbxL8I2JytDN3q6UmgFoinArTptYlnxZEd__igfroDkqaYArXHFs";   // Replace by your GAS service id 

void setup() {
//  mq2.begin();
  initWifi();
  
  pinMode(32, INPUT);
  Serial.begin(115200);
  
 
}

void loop() {
  
/*  float* values = mq2.read(false); //set it true if you want to print the values in the Serial

  //* 1 = LPG in ppm
  //* 2 = CO in ppm
  //* 3 = SMOKE in ppm
  
  //lpg = values[0];
  lpg = mq2.readLPG();
  //co = values[1];
  co = mq2.readCO();
  //smoke = values[2];
  smoke = mq2.readSmoke();      */

  delay(20000);
  sendData(analogRead(32));
}

void initWifi() {
  Serial.print("Connecting to: "); 
  Serial.print(ssid);
  WiFi.begin(ssid, password);  

  int timeout = 10 * 4; // 10 seconds
  while(WiFi.status() != WL_CONNECTED  && (timeout-- > 0)) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("");

  if(WiFi.status() != WL_CONNECTED) {
     Serial.println("Failed to connect, going back to sleep");
  }

  Serial.print("WiFi connected in: "); 
  Serial.print(millis());
  Serial.print(", IP address: "); 
  Serial.println(WiFi.localIP());
}

void sendData(float val)
{
  Serial.print("connecting to ");
  Serial.println(host);
  if (!client.connect(host, httpsPort)) {
    Serial.println("connection failed");
    return;
  }

  if (client.verify(fingerprint, host)) {
  Serial.println("certificate matches");
  } else {
  Serial.println("certificate doesn't match");
  }
  //String string_person =  String(tem, DEC); 
  String url = "/macros/s/" + GAS_ID + "/exec?tempData=" + val;
  Serial.print("requesting URL: ");
  Serial.println(url);

  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
         "Host: " + host + "\r\n" +
         "User-Agent: BuildFailureDetectorESP8266\r\n" +
         "Connection: close\r\n\r\n");

  Serial.println("request sent");
  while (client.connected()) {
  String line = client.readStringUntil('\n');
  if (line == "\r") {
    Serial.println("headers received");
    break;
  }
  }
  String line = client.readStringUntil('\n');
  if (line.startsWith("{\"state\":\"success\"")) {
  Serial.println("esp8266/Arduino CI successfull!");
  } else {
  Serial.println("esp8266/Arduino CI has failed");
  }
  Serial.println("reply was:");
  //Serial.println("==========");
  //Serial.println(line);
  //Serial.println("==========");
  Serial.println("closing connection");
}
