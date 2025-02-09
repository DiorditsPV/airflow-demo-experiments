.PHONY: gen clean

gen:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. stock.proto

clean:
	rm -f stock_pb2.py stock_pb2_grpc.py 