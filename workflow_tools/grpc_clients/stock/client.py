import os
import random
from typing import List

import grpc
import requests
from workflow_tools.grpc_clients.stock.proto import stock_pb2, stock_pb2_grpc


class StockClient:
    def __init__(self, service_url, auth_token):
        self.service_url = service_url
        self.auth_token = auth_token
        self.metadata = (("authorization", f"Bearer {self.auth_token}"),)

    def get_stock(self, item_ids: List[int]):
        try:
            channel = grpc.insecure_channel(self.service_url)
            stub = stock_pb2_grpc.StockServiceStub(channel)
            request = stock_pb2.GetStockRequest(item_ids=item_ids)
            response = stub.GetStock(request, metadata=self.metadata)
            return response
        except grpc.RpcError as e:
            print(f"RPC failed: {e}")


def parse_stock_response(response):
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