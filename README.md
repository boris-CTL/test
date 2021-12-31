# IOT HW for NMLab, 2021-fall, b06703027.

## How to run


- First, clone the project
```bash
git clone ***
```
- Change current directory
```bash
cd 
```
- Install project dependencies and make sure the environment is well-built.
```bash
# Install protobuf compiler
sudo apt-get install protobuf-compiler

# Install buildtools
sudo apt-get install build-essential make

# Install grpc packages
pip3 install -r requirements.txt
```
- Run the eclipse mosquitto docker container
```bash
cd mosquitto-part
docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
cd ..
```
- Compile protobuf schema to python wrapper by doing the following instructions:
```bash
cd django-part 
make
cd ../gRPC-part
make
cd ../mosquitto-part
make
```
- Start the REST server. First, open another new terminal:
```bash
cd django-part
cd mysite
python3 manage.py migrate
python3 manage.py runserver
```
- Start the server that calculates the Fibonacci number. Open yet another new terminal:
```bash
cd gRPC-part
python3 fib_server.py
```
- Start the loggin server. Open yet another new terminal:
```bash
cd mosquitto-part
python3 logging_server.py
```
- POST method to sent Fibonacci-order-request to servers.
```bash
curl -X POST -H "Content-Type: application/json" http://localhost:8000/rest/fibonacci/ -d "{\"order\": #Number}"
```

 - GET method to get the history of our requests from servers.
```bash
curl http://localhost:8000/rest/logs
```