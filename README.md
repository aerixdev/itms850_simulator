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

**[device.json]**
| Key | Data Type | Description | Example |
|-----|-----------|-------------|---------|
|'gateway'| Integer | 콤보디바이스 ID | 5000 |
|'eui' | Integer | 게이트웨이 ID(사업장 구분코드로 활용) | 80 |

**[mqtt.json]**
| Key | Data Type | Description | Example |
|-----|-----------|-------------|---------|
|'server'| String | MQTT브로커 접속주소 | 'data.thingarx.com' |
|'port' | Integer | MQTT브로커 통신포트 | 1883 |
|'topic' | String | 발행할 메시지의 토픽(TOPIC)명 | 'tharx/combo/data/lap01' |
|'interval' | Interval | 메시지 발행 시간간격(단위 : 초) | 5 |

**[sensors.json]**
| Key | Data Type | Description |
|-----|-----------|-------------|
|'di1'| Object | DI1 데이터 생성 옵션 |
|'di2'| Object | DI2 데이터 생성 옵션 |
|'di3'| Object | DI3 데이터 생성 옵션 |
|'di4'| Object | DI4 데이터 생성 옵션 |
|'ai1'| Object | AI1 데이터 생성 옵션 |
|'ai2'| Object | AI2 데이터 생성 옵션 |
|'diff_pres'| Object | 차압 데이터 생성 옵션 |
|'pressure'| Object | 압력 데이터 생성 옵션 |
|'temperature'| Object | 온도 데이터 생성 옵션 |
|'voltage'| Object | 전압 데이터 생성 옵션 |
|'current'| Object | 전류 데이터 생성 옵션 |
|'power'| Object | 전력 데이터 생성 옵션 |
|'active_power'| Object | 유료전력 데이터 생성 옵션 |

각각의 데이터 생성 옵션은 다음과 같이 구성됩니다.
| Key | Data Type | Description |
|-----|-----------|-------------|
|'min'| Object | 임의의 값 범위 : 최소값 |
|'max'| Object | 임의의 값 범위 : 최대값 |
|'value'| Object | 임의의 값을 생성하지 않고 항상 고정값을 사용(value가 존재하는 경우 min,max는 무시됨) |


## 관련 Repository ##

<a href="https://github.com/aerixdev/itms850_dataparser" target="_blank">스마트콤보(제품명 : ITMS-850) 데이터 MQTT 수신 예제</a>
