import imageGrpc_pb2
import imageGrpc_pb2_grpc

import grpc


def upload_image(stub, image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    response = stub.UploadImage(imageGrpc_pb2.UploadImageRequest(
        image_id="12345",
        image_data=image_data,
    ))
    print("UploadImage Response:", response)

def return_image_data(stub):
    response = stub.ReturnImageData(imageGrpc_pb2.ReturnImageDataRequest(
        id="12345",
        description="Sample description",
        objects=["object1", "object2"],
        text="Sample text",
    ))
    print("ReturnImageData Response:", response)

def run():
    with grpc.insecure_channel("localhost:50050") as channel:
        stub = imageGrpc_pb2_grpc.ImageServiceStub(channel)
        upload_image(stub, "path_to_your_image.jpg")
        return_image_data(stub)

if __name__ == "__main__":
    run()
