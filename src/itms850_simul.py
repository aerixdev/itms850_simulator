
from multiprocessing.sharedctypes import Value
import paho.mqtt.client as mqtt
import logging
import json
import random
import datetime
import time

'''
MQTT 브로커에 연결될 떄 호출되는 콜백 함수
'''
def on_connect(client,userdata,flags,rc):
    global logger
    
    if(rc==0):
        logger.info("MQTT broker is connected.")
    else:
        logger.info("Connection error is occured.")

'''
MQTT 브로커에 연결이 해제될 떄 호출되는 콜백 함수
'''
def on_disconnect(client,userdata,flags,rc):
    logger.info("MQTT broker is disconnected.")

'''
MQTT 브로커에 메시지가 발행되었을 때 호출되는 콜백 함수
'''
def on_publish(client,userdata,mid):
    logger.info("Message is published : mid={}".format(mid))

'''
logger 객체를 초기화하는 함수
'''
def logger_init(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    return logger

'''
MQTT 브로커로 전송할 임의의 센서 데이터를 생성하는 함수
'''
def generate_sensor_value(sensors):
    result = {}
    for key in sensors: #di1
        option = sensors[key]
        if 'value' in option:
            result[key] = option['value']
        else:
            min = option['min']
            max = option['max']
            result[key] = random.randrange(min,max+1)
    
    return result

def generate_newsensor_value(sensors):
    result = {}
    for key in sensors:
        
        if key == 'id':
            continue
        option = sensors[key]
        if 'value' in option:
            result[key] = option['value']
        else:
            min = option['min']
            max = option['max']
            result[key] = random.randrange(min,max+1)
    
    return result

'''
임의의 값으로 생성된 센서 데이터를 MQTT 메시지로 변환하는 함수
'''
def get_new_message(data,eui,gateway_id,sensors_config):
    msg = {}
 
    msg['time'] = str(datetime.datetime.now()).replace(' ','T')+'Z'
    msg['eui'] = eui
    
    payload = {}
    payload['id'] = sensors_config["id"]


    di = [data['di1'],data['di2'],data['di3'],data['di4']]
    payload['di'] = di
    
    aidatas =[]
    aidata = {}
    result = {}
    for key in sensors_config: 
        if "ai" in key:
            result = sensors_config[key]
            aidata['type'] = result['type']
            aidata['value'] = data[key]
            aidata['unit'] = result['unit']
            aidata['code'] = result['code']
            aidatas.append(aidata)

    payload['ai'] = aidatas
        
    pressure ={}
    pressure['value'] = data['pressure']
    pressure['unit'] = sensors_config['pressure']['unit']
    pressure['code'] = sensors_config['pressure']['code']
    payload['pressure'] = pressure

    diff_pressure ={}
    diff_pressure['value'] = data['diff_pressure']
    diff_pressure['unit'] = sensors_config['diff_pressure']['unit']
    diff_pressure['code'] = sensors_config['diff_pressure']['code']
    payload['diff_pressure'] = diff_pressure

    temperature ={}
    temperature['value'] = data['temperature']
    temperature['unit'] = sensors_config['temperature']['unit']
    temperature['code'] = sensors_config['temperature']['code']
    payload['temperature'] = temperature

    voltage ={}
    voltage['value'] = data['voltage']
    voltage['unit'] = sensors_config['voltage']['unit']
    payload['voltage'] = voltage
   
    current ={}
    current['value'] = data['current']
    current['unit'] = sensors_config['current']['unit']
    current['code'] = sensors_config['current']['code']
    payload['current'] = current

    active_power ={}
    active_power['value'] = data['active_power']
    active_power['unit'] = sensors_config['active_power']['unit']
    payload['active_power'] = active_power

    energy ={}
    energy['value'] = data['energy']
    energy['unit'] = sensors_config['energy']['unit']
    payload['energy'] = energy

    msg['payload'] = payload
    msg['gateway_id'] = gateway_id

    return msg

def get_message(data,eui,gateway_id):
    msg = {}
 
    msg['time'] = str(datetime.datetime.now()).replace(' ','T')+'Z'
    msg['eui'] = eui
    
    payload = [1]


    header = 0
    header = header | (data['di4'] << 3)
    header = header | (data['di3'] << 2)
    header = header | (data['di2'] << 1)
    header = header | (data['di1'])

    payload.append(header)

    payload.append(data['ai1'] >> 8)
    payload.append(data['ai1'] & 0x00FF)
    payload.append(data['ai2'] >> 8)
    payload.append(data['ai2'] & 0x00FF)

    payload.append(data['diff_pres'] >> 8)
    payload.append(data['diff_pres'] & 0x00FF)

    payload.append(data['pressure'] >> 8)
    payload.append(data['pressure'] & 0x00FF)

    payload.append(data['temperature'] >> 8)
    payload.append(data['temperature'] & 0x00FF)
    
    payload.append(data['voltage'] >> 8)
    payload.append(data['voltage'] & 0x00FF)

    payload.append((data['current'] & 0xFF000000) >> 24)
    payload.append((data['current'] & 0x00FF0000) >> 16)
    payload.append((data['current'] & 0x0000FF00) >> 8)
    payload.append(data['current'] & 0x000000FF)

    payload.append((data['power'] & 0xFF000000) >> 24)
    payload.append((data['power'] & 0x00FF0000) >> 16)
    payload.append((data['power'] & 0x0000FF00) >> 8)
    payload.append(data['power'] & 0x000000FF)


    payload.append((data['active_power'] & 0xFF000000) >> 24)
    payload.append((data['active_power'] & 0x00FF0000) >> 16)
    payload.append((data['active_power'] & 0x0000FF00) >> 8)
    payload.append(data['active_power'] & 0x000000FF)

    msg['payload'] = payload
    msg['gateway_id'] = gateway_id

    return msg


def get_lora_message(data,eui,gateway_id):
    msg = {}
 
    msg['time'] = str(datetime.datetime.now()).replace(' ','T')+'Z'
    msg['eui'] = eui
    
    payload = [1]


    header = 0
    header = header | (data['di4'] << 7)
    header = header | (data['di4'] << 6)
    header = header | (data['di3'] << 5)
    header = header | (data['di2'] << 4)
    header = header | (data['di4'] << 3)
    header = header | (data['di3'] << 2)
    header = header | (data['di2'] << 1)
    header = header | (data['di1'])

    payload.append(header)

    payload.append(data['ai1'] >> 8)
    payload.append(data['ai1'] & 0x00FF)
    payload.append(data['ai2'] >> 8)
    payload.append(data['ai2'] & 0x00FF)
    payload.append(data['ai3'] >> 8)
    payload.append(data['ai3'] & 0x00FF)
    payload.append(data['ai4'] >> 8)
    payload.append(data['ai4'] & 0x00FF)

    msg['payload'] = payload
    msg['rssi'] = data['rssi']
    msg['apid'] = gateway_id

    return msg

def get_modbus_message(data,eui,gateway_id):
    msg = {}
 
    msg['time'] = str(datetime.datetime.now()).replace(' ','T')+'Z'
    msg['eui'] = eui
    
    payload = [3]

    payload.append(data['energy1'] >> 24)
    payload.append(data['energy1'] >> 16 & 0x00FF)
    payload.append(data['energy1'] >> 8 & 0x00FF )
    payload.append(data['energy1'] & 0x00FF)

    msg['payload'] = payload
    msg['rssi'] = data['rssi']
    msg['apid'] = gateway_id

    return msg

'''
json 설정 파일을 읽어오는 함수
'''
def get_config(file_path):
    with open(file_path,'r') as f:
        config_data = json.load(f)

    return config_data


    '''
        di1 = config_data['di1']
        di2 = config_data['di2']
        di3 = config_data['di3']
        di4 = config_data['di4']
        ai1 = config_data['ai1']
        ai2 = config_data['ai2']
        diff_pres = config_data['diff_pres']
        pressure = config_data['pressure']
        temperature = config_data['temperature']
        voltage = config_data['voltage']
        current = config_data['current']
        power = config_data['power']
        active_power = config_data['active_power']

    return (di1,di2,di3,di4,ai1,ai2,diff_pres,pressure,temperature,voltage,current,power,active_power)
    '''

'''
Main 함수
'''
def main():
    global logger
    logger = logger_init("ITMS-850")

    logger.info("Application is started.........................")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish

    # MQTT 접속 정보는 mqtt.json 파일에서 읽어옵니다.
    mqtt_config = get_config("./mqtt.json")
    logger.info("mqtt.json : loaded")

    server = mqtt_config['server']
    port = mqtt_config['port']
    topic = mqtt_config['topic']
    interval = mqtt_config['interval']
    

    logger.info("server : {}".format(server))
    logger.info("port : {}".format(port))
    logger.info("topic : {}".format(topic))
    logger.info("interval : {}".format(interval))


    # 디바이스 정보는 device.json 파일에서 읽어옵니다.
    device_config = get_config("./device.json")
    logger.info("device.json : loaded")
    eui = device_config['eui']
    gateway_id = device_config['gateway_id']
    mode = device_config['mode']
    
    # 임의의 센서 데이터 생성 정보는 sensors.json 파일에서 읽어옵니다.
    sensors_config = get_config("./sensors.json")
    logger.info("newsensors.json : loaded")

    for key in sensors_config:
        logger.info("{} : {}".format(key,sensors_config[key]))

    # MQTT 브로커에 접속 및 메시지 발행
    client.connect(server,port)
    while(True):
        
        if mode == "old":
            data = generate_sensor_value(sensors_config)
            logger.info("random sensor data is generated : {}".format(data))
            #client.publish(json.dumps(data))
        
            msg = get_message(data,eui,gateway_id)
            logger.info("mqtt message is generated : {}".format(msg))

            client.publish(payload=json.dumps(msg).replace(' ',''),topic=topic)

            time.sleep(interval)
            
        elif mode == "new": 
            data = generate_newsensor_value(sensors_config)
            logger.info("random sensor data is generated : {}".format(data))
            #client.publish(json.dumps(data))
        
            msg = get_new_message(data,eui,gateway_id,sensors_config)
            logger.info("mqtt message is generated : {}".format(msg))

            client.publish(payload=json.dumps(msg).replace(' ',''),topic=topic)

            time.sleep(interval)
            
        elif mode == "lora": 
            data = generate_sensor_value(sensors_config)
            logger.info("random sensor data is generated : {}".format(data))
            #client.publish(json.dumps(data))
        
            msg = get_lora_message(data,eui,gateway_id)
            logger.info("mqtt message is generated : {}".format(msg))

            client.publish(payload=json.dumps(msg).replace(' ',''),topic=topic)

            time.sleep(interval)
            
        elif mode == "modbus": 
            data = generate_sensor_value(sensors_config)
            logger.info("random sensor data is generated : {}".format(data))
            #client.publish(json.dumps(data))
        
            msg = get_modbus_message(data,eui,gateway_id)
            logger.info("mqtt message is generated : {}".format(msg))

            client.publish(payload=json.dumps(msg).replace(' ',''),topic=topic)

            time.sleep(interval)
            

if __name__=="__main__":
    main()
