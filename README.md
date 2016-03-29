####Historiangen

###A data generator that emulates the type of data that would come from a historian (or devices that send data to a historian)

###Prereqs
* Python 
* Hadoop cluster w/ Kafka running
* An existing topic in Kafka to publish to 

###Usage
Clone this repo
```
git clone https://github.com/bkvarda/historiangen.git
```
Then change the variables for Kafka Broker and Kafka Topic inside of historiangen.py

Finally, run the generator:
```
python historiangen.py
```

