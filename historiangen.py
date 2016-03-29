import json, string, random, time, datetime
from kafka import SimpleProducer, KafkaClient


#Config Variables
kafka_broker = "localhost:9092"
kafka_topic = "historian_raw"
num_devices = 30 
events_to_generate = 1000000

#Instantiate Kafka Producer
client = KafkaClient(kafka_broker)
producer = SimpleProducer(client, async=True, batch_send_every_n=1000, batch_send_every_t=10)

#Historian data format
##Format = Tag_Name<String>, Ticks<String> (02/04/2016 12:30:35.00), Value<Double> (50.21), Confidence<Double> (100.00)

#Instantiate devices
devices = []
for device in range(num_devices):
    rand_id = ''
    for i in range(10):
        rand_id += rand_id.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits))
    devices.append(rand_id)

confidence_level = [100.0, 100.0, 100.0, 99.0, 100.0, 100.0, 99.9, 98.0, 99.9, 100.0, 50.0, 100.0, 99.9]

#Device parent definitions - each measurement device (or tag) belongs to some parent entity (IE an oil well)

parent_types = ["Well","Pipe","Rig","Pole"]
parent_letters = ["A","B","C","D","E","F","G"]
measurement_types = ["Temperature","Flow Rate","Casing Pressure","Tubing Pressure"]
target_table_name = "Production Table"
headers = "Tag_Name,Tag_Entity_Id,Tag_Description,Target_Table_Name,Target_Column"

print(headers)

for device in devices:
    tag_name = device
    tag_entity_id = random.SystemRandom().choice(parent_types) + ' ' + random.SystemRandom().choice(parent_letters)
    target_column = random.SystemRandom().choice(measurement_types)
    tag_description = tag_entity_id + ' ' + target_column
    print(str(tag_name) + ',' + str(tag_entity_id) + ',' + str(tag_description) + ',' + str(target_table_name) + ',' + str(target_column))

#Randomly generate until events_to_generate is reached for every device
for events in range(events_to_generate):
    for device in devices:
        tag_name = device
        ticks = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S.%f')[:-4]
        value = random.uniform(0.9,1.0)*random.SystemRandom().randint(50,100)
        confidence = random.uniform(0.9,1.0)*random.choice(confidence_level)
        message = str(tag_name) + ',' + str(ticks) + ',' + str(round(value,2)) + ',' + str(round(confidence,2))
        producer.send_messages(kafka_topic, message)

