##############################################################################
## Initialize client
##     - This initializes the gRPC based client to communicate with the
##       Clarifai platform.
##############################################################################
## Import in the Clarifai gRPC based objects needed
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2

import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path.home() / "wa-bot" / ".env"
load_dotenv(dotenv_path=env_path)

## Construct the communications channel and the object stub to call requests on.
# Note: You can also use a secure (encrypted) ClarifaiChannel.get_grpc_channel() however
# it is currently not possible to use it with the latest gRPC version
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)


################################################################################
## Set up Personal Access Token and Access information
##     - This will be used by every Clarifai API call
################################################################################
## Specify the Authorization key.  This should be changed to your Personal Access Token.
## Example: metadata = (('authorization', 'Key 123457612345678'),)
metadata = (("authorization", f'Key {os.getenv("CLARIFAI_API_KEY")}'),)


def get_cake_tags(image_url):
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            # The userDataObject is created in the overview and is required when using a PAT
            model_id="bd367be194cf45149e75f01d59f77ba7",
            # This is optional. Defaults to the latest model version.
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(image=resources_pb2.Image(url=image_url))
                )
            ],
        ),
        metadata=metadata,
    )
    if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_model_outputs_response.status.code)
        raise Exception(
            "Post model outputs failed, status: "
            + post_model_outputs_response.status.description
        )

    # Since we have one input, one output will exist here.
    output = post_model_outputs_response.outputs[0]

    cake_tags = {}

    print("Predicted concepts:")
    for concept in output.data.concepts:
        if concept.value > 0.75:
            cake_tags[concept.name] = 1
            print("%s %.2f" % (concept.name, concept.value))
            return cake_tags
    print(cake_tags)


if __name__ == "__main__":
    tags = get_cake_tags(
        "https://images.unsplash.com/photo-1627834377411-8da5f4f09de8?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=401&q=80"
    )
    if tags:
        print(tags)
    else:
        print("not true!")
