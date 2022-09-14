#include "ESP8266.h"
#include "SoftwareSerial.h"

byte nuidPICC[4];

//MPU6050配置部分开始***
#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

MPU6050 accelgyro;

int16_t ax, ay, az;
int16_t gx, gy, gz;

int8_t axx, ayy, azz;
int8_t gxx, gyy, gzz;
int8_t axx_l, ayy_l, azz_l;
int8_t gxx_l, gyy_l, gzz_l;
#define OUTPUT_READABLE_ACCELGYRO

//MPU6050配置部分结束***


//配置ESP8266WIFI设置
#define SSID "hsy"    //填写2.4GHz的WIFI名称，不要使用校园网,ChinaNet-6yRD,667788
#define PASSWORD "20001010"//填写自己的WIFI密码,pnqyntds,ab753951
#define HOST_NAME "192.168.137.1"  //API主机名称，连接到OneNET平台，无需修改，，192.168.56.1
#define DEVICE_ID "562324123"       //填写自己的OneNet设备ID,562324123
#define HOST_PORT (8080)                //API端口，连接到OneNET平台，无需修改
String APIKey = "LgaoqvCcR2SlZl861B1AVpZH9DE="; //与设备绑定的APIKey

//#define INTERVAL_SENSOR 1 //定义传感器采样及发送时间间隔


//定义ESP8266所连接的软串口
SoftwareSerial mySerial(3, 2);
ESP8266 wifi(mySerial);

void setup()
{
  ax = 0;
  ay = 0;
  az = 0;
  gx = 0;
  gy = 0;
  gz = 0;
  //
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif
    


    //mpu6050结束
  //

  
  mySerial.begin(115200); //初始化软串口
  Serial.begin(9600);     //初始化串口
  Serial.println("开始初始化");
  
  
  //ESP8266初始化
   if (wifi.setOprToStation()) {
    Serial.println("成功连接到站点");
  } else {
    Serial.println("连接站点失败");
  }

  //ESP8266接入WIFI
  if (wifi.joinAP(SSID, PASSWORD)) {
    Serial.println("成功接入WiFi");
    Serial.print("IP: ");
    Serial.println(wifi.getLocalIP().c_str());
  } else {
    Serial.println("连接WiFi失败");
  }


  mySerial.println("AT+UART_CUR=9600,8,1,0,0");
  mySerial.begin(9600);
  Serial.println("初始化完成");

//
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
//
    

}

//unsigned long net_time1 = millis(); //数据上传服务器时间

void loop(){
        
  //if (net_time1 > millis())
   // net_time1 = millis();

 // if (millis() - net_time1 > INTERVAL_SENSOR) //发送数据时间间隔
 // {
    if (wifi.createTCP(HOST_NAME, HOST_PORT)) { //建立TCP连接，如果失败，不能发送该数据
      Serial.print("成功建立TCP连接\r\n");
      //char buf[10];
      //拼接发送data字段字符串
      //String jsonToSend = "{\"需要发送的变量名\":";
      //jsonToSend += "\"" + String("需要发送的变量") + "\"";
      //jsonToSend += "}";
      //MPU6050开始
      
      //MPU6050结束

      //String jsonToSend = "{\"MPU6050-6维模拟参数\":";
      //jsonToSend += "\"" + String(ax) +"," + String(ay) +","+  String(az) +","+ String(gx) +","+ String(gy) +","+ String(gz) +"\"";
      
       /*accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
        Serial.print("a/g:\t");
        Serial.print(ax); Serial.print("\t");
        Serial.print(ay); Serial.print("\t");
        Serial.print(az); Serial.print("\t");
        Serial.print(gx); Serial.print("\t");
        Serial.print(gy); Serial.print("\t");
        Serial.println(gz);
        jsonToSend += "\"" + String(ax) +"," + String(ay) +","+  String(az) +","+ String(gx) +","+ String(gy) +","+ String(gz) +"\"";*/
      /*String jsonToSend = "{\"MPU6050-6维模拟参数\":";
      accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
      jsonToSend += "\"" + String(ax) +"," + String(ay) +","+  String(az) +","+ String(gx) +","+ String(gy) +","+ String(gz) +","+"\"";
      jsonToSend += "}";*/

      String jsonToSend = "";
      for (int i = 1; i < 20; i++) {
           accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
           //jsonToSend += String(ax) +"," + String(ay) +","+  String(az) +","+ String(gx) +","+ String(gy) +","+ String(gz) +","+ String(i) +";"+"\r\n";
           axx = ax;
           axx_l = ax >> 8;
           ayy = ay;
           ayy_l = ay >> 8;
           azz = az;
           azz_l = az >> 8;
           gxx = gx;
           gxx_l = gx >> 8;
           gyy = gy;
           gyy_l = gy >> 8;
           gzz = gz;
           gzz_l = gz >> 8;
           //char (axx);
           //ayy = ay;
           //char (ayy);
           //azz = az;
           //char (azz);
           //gxx = gx;
           //char (gxx);
           //gyy = gy;
           //char (gyy);
           //gzz = gz;
           //char (gzz);
           //jsonToSend += String(ax) +"," + String(ay)  +","+  String(az)  +","+ String(gx) +","+ String(gy)  +","+ String(gz) +","+ String(i)  +";"+"\r\n";
           jsonToSend += char(axx_l);
           jsonToSend += char(axx);
           jsonToSend += char(ayy_l);
           jsonToSend += char(ayy);
           jsonToSend += char(azz_l);
           jsonToSend += char(azz);
           jsonToSend += char(gxx_l);
           jsonToSend += char(gxx);
           jsonToSend += char(gyy_l);
           jsonToSend += char(gyy);
           jsonToSend += char(gzz_l);
           jsonToSend += char(gzz);
           jsonToSend += char(i);
           //+ char(axx_l)+"," + char(ayy)+char(ayy_l) +","+  char(azz)+ char(azz_l) +","+ char(gxx)+char(gxx_l) +","+ char(gyy)+char(gyy_l)  +","+ char(gzz)+char(gzz_l) +","+ String(i)  +";"+"\r\n";
           delay(100);
      }
      jsonToSend += "}";

      
      //拼接POST请求字符串
      String postString = "POST ";
      //postString += DEVICE_ID;
      //postString += "/datapoints?type=3 HTTP/1.1";
      //postString += "\r\n";
      //postString += "api-key:";
      //postString += APIKey;
      postString += "\r\n";
      postString += "TIME:";
      postString += millis();
      postString += "\r\n";
      //postString += "Host:api.heclouds.com\r\n";
      //postString += "Connection:close\r\n";
      postString += "Content-Length:";
      postString += jsonToSend.length();
      postString += "\r\n";
      //postString += "\r\n";
      postString += jsonToSend;
      //postString += "\r\n";
      //postString += "\r\n";
      postString += "\r\n";
      /*String postString = "PPPPPPPP";
      postString += jsonToSend;
      postString += "EEEEEEE";*/
      


      const char *postArray = postString.c_str(); //将str转化为char数组

      Serial.println(postArray);
      wifi.send((const uint8_t *)postArray, strlen(postArray)); //send发送命令，参数必须是这两种格式，尤其是(const uint8_t*)
      Serial.println("send success");
      /*if (wifi.releaseTCP()) { //释放TCP连接
        Serial.print("release tcp ok\r\n");
      } else {
        Serial.print("release tcp err\r\n");
      }*/
      postArray = NULL; //清空数组，等待下次传输数据
    } else {
      Serial.print("create tcp err\r\n");
    }

    Serial.println("");

   //net_time1 = millis();
 // }
}
