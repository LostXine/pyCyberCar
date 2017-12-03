# pyCyberCar

CyberCar driver on Raspberry Pi 3 in Python 2.

The project includes a driver for CyberCar and a visualization tool [cybercar.html](/html/cybercar.html).

CyberCar is made from FREESCALE Type B. We use Raspberry Pi 3B+ as a controller. Then we added a CSI camera, a S-D5 servo motor, a 540 DC motor and other DC-DC modules. It can perform several image processing experiments and can work with many extensions.

本工程包括使用python2编写的智能小车CyberCar驱动pyCyberCar以及配套的可视化网页[cybercar.html](/html/cybercar.html)。

CyberCar是在飞思卡尔B型车基础上，添加树莓派3B+作为上位机的改造型。全车搭载CSI摄像头，S-D5舵机，540直流电机以及相关电源模块，可以执行多种图像处理实验。而且支持多种模块的拓展。

***
### Dependence
* [RPi.GPIO](https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/): To output PWM (输出控制信号)
* [nrf24pihub](https://github.com/riyas-org/nrf24pihub): To drive NRF24L01+ module (驱动2.4G通讯模块NRF24L01+)
* [OpenCV](http://www.opencv.org/): To process images from camera (处理图像)
* [simple-websocket-server](https://github.com/dpallot/simple-websocket-server): To push data to the viewer (使用websockt推送数据)
* [bootstarp](https://getbootstrap.com/): To build CyberCar Viewer's framework (用于搭建CyberCar Viewer)
* [echarts](http://echarts.baidu.com/): To draw line charts (用来绘制折线统计图)

### Usage
* Run the car's [server](/run_server.py) first (-d: debug mode):
```
python run_server.py
```
* Open another terminal
* (For OpenCV user) Edit [dip.py](/dip.py), then run [run_cybercar.py](/run_cybercar.py)(-f: show fps | -mp: using multi-processing pool):
```
python run_cybercar.py
```
OR
* (For NRF24 user) Run the nrf24 receiver:
```
python run_nrf24.py
```

### 使用方法
* 运行底层服务器[run_server.py](/run_server.py)(-d: 打开debug模式):
```
python run_server.py
```
* 打开另一个控制台窗口
* (使用OpenCV控制) 编辑[dip.py](/dip.py)以设计图像处理算法，然后运行[run_cybercar.py](/run_cybercar.py)(-f: 显示fps | -mp: 使用进程池处理图像):
```
python run_cybercar.py
```
或者
* (使用2.4G遥控) 运行nrf24接收模块:
```
python run_nrf24.py
```
### 请参加“数字图像处理基础”的同学注意:

为了方便代码评阅，建议只修改 [dip.py](/dip.py) 和 [config.py](/config.py) 两个文件，最后使用git提交代码。

***
### Developer
* [Yue ZHOU](http://cvpr.sjtu.edu.cn/aboutme.aspx), A.P. Department of Automation, Shanghai Jiao Tong University.
* [Xiang LI](http://xxli.me), MEng Department of Automation, Shanghai Jiao Tong University. 
* Shuo Shan, MEng Department of Automation, Shanghai Jiao Tong University. 

### Contact me
* Email: lostxine@gmail.com
* Address: Room 2#302B, SEIEE Building, 800 DongchuanRd., Shanghai, PR China (200240)
