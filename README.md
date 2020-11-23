## gRPC Service for Projects

Questo progetto implementaun servizio gRPC per la gestione dei worskspaces:

1. A riga di commando, eseguire il commando:

    ```shell script
    python ./server.py 
    ```
2. Compilando il Docker file:

    ```shell script
    docker build -t datasets-services:latest .
    docker run -d -p 50051:50051 -n datasets-services datasets-services:latest
    ```
   
3. Generare gRPC code

    ```shell script
     python -m grpc_tools.protoc -I./protobuffers --python_out=./protobuffers --grpc_python_out=./protobuffers ./protobuffers/service.proto
    ```