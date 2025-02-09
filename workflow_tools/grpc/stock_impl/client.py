import os
from typing import List

from workflow_tools.grpc.stock_impl.proto import stock_pb2, stock_pb2_grpc
from workflow_tools.grpc.client.grpc_client import GrpcClient


class StockClient(GrpcClient):
    def get_stock(self, item_ids: List[int]):
        stub = stock_pb2_grpc.StockServiceStub(self._create_channel())
        request = stock_pb2.GetStockRequest(item_ids=item_ids)
        return self._execute_grpc_call(stub.GetStock, request) 

def parse_stock_response(response):
    if not response:
        return
    for item in response.items:
        yield {
            "item_id": item.item_id,
            "warehouse_id": item.warehouse_id,
            "quantity": item.quantity,
            "updated_at": item.updated_at.ToDatetime(),
        } 

def main():
    service_url = "stock-service:50051"
    auth_token = os.environ["AUTH_TOKEN"]

    client = StockClient(service_url, auth_token)
    response = client.get_stock([1, 2, 3])

    for stock_item in parse_stock_response(response):
        print(stock_item)


if __name__ == "__main__":
    main()