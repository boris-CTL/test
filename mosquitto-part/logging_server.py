import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt
import threading

history = []

class subb():
    def __init__(self):
        self.client = mqtt.Client()

        
    def go_execute(self):
        self.client.on_message = self.on_message
        self.client.connect(host="localhost", port=1883) #ince we use docker to listen to port number 1883.
        self.client.subscribe('log', 0)
        try:
            self.client.loop_forever()
        except KeyboardInterrupt as e:
            pass


    def on_message(self, client, obj, msg):
        print(f"The result is :{msg.payload} and it'll be autosaved.")
        history.append(msg.payload)


    

class LogAndSaveJasonServicer(log_pb2_grpc.LogAndSaveJasonServicer):

    def __init__(self):
        pass

        
        
    def request_hist(self, request, context):
        response = log_pb2.LogResponse()
        for cached_hist in history:
            response.value.append(cached_hist)
        return response
        
        
      


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8088, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LogAndSaveJasonServicer()
    log_pb2_grpc.add_LogAndSaveJasonServicer_to_server(servicer, server)
    sub = subb()

    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"gRPC server runs at {args['ip']}:{args['port']}")
        sub.go_execute()
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
