import grpc


class GrpcClient:
    def __init__(self, service_url: str, auth_token: str):
        self.service_url = service_url
        self.auth_token = auth_token
        self.metadata = (("authorization", f"Bearer {self.auth_token}"),)

    def _create_channel(self):
        return grpc.insecure_channel(self.service_url)

    def _execute_grpc_call(self, stub_method, request):
        try:
            return stub_method(request, metadata=self.metadata)
        except grpc.RpcError as e:
            print(f"Error: {e}")
            return None 