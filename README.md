# 스마트콤보(제품명 : ITMS-850) MQTT 시뮬레이터

이 시뮬레이터는 에어릭스의 통합IoT센서 제품인 ```스마트콤보(제품명 : ITMS-850)``` 디바이스와 동일한 형식으로 가상의 센서데이터 값을 랜덤하게 생성하여 지정된 MQTT Broker로 전송하도록 기능이 구현되어 있습니다.

이 시뮬레이터를 활용하면 ```스마트콤보(제품명 : ITMS-850)``` 디바이스가 없더라도, MQTT브로커를 통해서 디바이스로부터 데이터를 수신하는 시스템을 개발하고 테스트하는 것이 가능합니다.

## 개요 ##

* 작성자 : 이상훈 (에어릭스 환경시스템사업부 기술연구소 / sanghoon.lee@aerix.co.kr)
* 프로그램 언어 : Python
* 작성일 : 2022-09-07

## 프로그램 실행방법 ##

repository의 src폴더에 예제 프로그램을 실행시키기 위해서 필요한 소스 코드가 위치해있습니다. src폴더로 이동하여 다음과 같이 프로그램을 실행할 수 있습니다.

```
python itms850_simul.py
```

**참고) 프로그램을 실행하는 PC에 파이썬이 설치되어 있어야 합니다.**

프로그램 실행시 참조되는 설정파일은 device.json, mqtt.json, sensors.json이며 모두 동일한 경로에 위치해야만 합니다.

[device.json]
| Key | Data Type | Description | Example |
|-----|-----------|-------------|---------|
|'gateway'| Integer | 콤보디바이스 ID | 5000 |
|'eui' | Integer | 게이트웨이 ID(사업장 구분코드로 활용) | 80 |


## 관련 Repository ##

<a href="https://github.com/aerixdev/itms850_dataparser" target="_blank">스마트콤보(제품명 : ITMS-850) 데이터 MQTT 수신 예제</a>
