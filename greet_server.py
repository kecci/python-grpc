from concurrent import futures
import time

import grpc
import greeter_pb2
import greeter_pb2_grpc

# add the following import statement to use server reflection
from grpc_reflection.v1alpha import reflection

class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return super().SayHello(request, context)
    def ParrotSaysHello(self, request, context):
        return super().ParrotSaysHello(request, context)
    def ChattyClientSaysHello(self, request_iterator, context):
        return super().ChattyClientSaysHello(request_iterator, context)
    def InteractingHello(self, request_iterator, context):
        return super().InteractingHello(request_iterator, context)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    
     # the reflection service will be aware of "Greeter" and "ServerReflection" services.
    SERVICE_NAMES = (
        greeter_pb2.DESCRIPTOR.services_by_name['Greeter'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port("[::1]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()