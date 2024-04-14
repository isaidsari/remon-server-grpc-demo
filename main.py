import grpc

import os
if not os.path.exists("remon_proto_pb2.py"):
    import subprocess
    import requests
    req = requests.get("https://raw.githubusercontent.com/adnanjpg/remon-server/grpc/proto/notification.proto")
    with open("remon_proto.proto", "w") as f:
        f.write(req.text)
    subprocess.run(["python", "-m", "grpc_tools.protoc", "-I.", "--python_out=.", "--grpc_python_out=.", "remon_proto.proto"])
    print("proto file downloaded, please run the script again")
    exit()
else:
    import remon_proto_pb2
    import remon_proto_pb2_grpc

# python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. remon_proto.proto

def main():
    # Connect to the gRPC server
    channel = grpc.insecure_channel('localhost:50051')

    # Create a stub for the NotificationService
    stub = remon_proto_pb2_grpc.NotificationServiceStub(channel)

    # Create a notification request
    request = remon_proto_pb2.NotificationRequest(
        title="Test Notification",
        body="This is a test notification sent from python app",
        token="example_token"
    )

    # Send the notification request to the server
    response = stub.SendNotification(request)

    # Print the response message
    print("Response from server:", response.message)


    # create log request
    log_request = remon_proto_pb2.LogRequest(
        level= "FATAL",
        message="This is a test log message sent from python app",
        target="example_target"
    )

    # Send the log request to the server
    log_response = stub.Log(log_request)

    # Print the response message
    print("Response from server:", log_response.message)

if __name__ == '__main__':
    main()
