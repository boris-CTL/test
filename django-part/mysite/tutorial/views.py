from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import json 
import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../build/service/")
sys.path.insert(0, BUILD_DIR)
import fib_pb2_grpc
import fib_pb2
import grpc
import log_pb2
import log_pb2_grpc
import paho.mqtt.client as mqtt


class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={'echo': 'hello world'}, status=200)


class FibAndGetJasonView(APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(host="localhost", port=1883) #docker listen to port 1883.


                      
    def get(self, request):
	    with grpc.insecure_channel("localhost:8088") as channel:
	        stub = log_pb2_grpc.LogAndSaveJasonStub(channel)
	        request = log_pb2.LogRequest()
	        response = stub.request_hist(request).value[:]
	        return Response(data={'history': response}, status=200)



class FibAndPostJasonView(APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(host="localhost", port=1883) #docker listen to port 1883.

    def post(self, request):
        requested_fib_order = request.data.get('order')
        with grpc.insecure_channel("localhost:8080") as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)
            request = fib_pb2.FibRequest()
            request.order = requested_fib_order
            response = stub.Compute(request)
            TempDictionary = {'order': requested_fib_order, 'value': response.value}
            #payload = json.dumps(TempDictionary)
            self.client.publish(topic='log', payload=json.dumps(TempDictionary))
            return Response(data=TempDictionary, status=200)
