# SteamDatabase

brew install rabbitmq
brew services start rabbitmq



pip3 install git+https://github.com/YashSinha1996/redis-simple-cache.git

brew install kafka
brew install zookeeper
zkServer start
kafka-server-start /usr/local/etc/kafka/server.properties
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test


kafka-console-producer --broker-list localhost:9092 --topic test
>HELLO Kafka

kafka-console-consumer --bootstrap-server localhost:9092 --topic test --from-beginning
HELLO Kafka
