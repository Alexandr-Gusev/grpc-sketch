cmake_minimum_required(VERSION 3.13)

project(example NONE)

find_package(Python REQUIRED COMPONENTS Interpreter)

set(proto "${CMAKE_CURRENT_SOURCE_DIR}/StoreAPI.proto")

get_filename_component(proto_path ${proto} PATH)
get_filename_component(proto_name ${proto} NAME_WE)

set(client_dir "${CMAKE_CURRENT_SOURCE_DIR}/client")
set(server_dir "${CMAKE_CURRENT_SOURCE_DIR}/server")

set(client_backend_dir "${client_dir}/backend")
set(server_backend_dir "${server_dir}/backend")

set(protoc_out
    "${client_backend_dir}/${proto_name}_pb2.py"
    "${client_backend_dir}/${proto_name}_pb2_grpc.py"
)
add_custom_command(
    OUTPUT  ${protoc_out}
    COMMAND "${Python_EXECUTABLE}"
            -m
            grpc_tools.protoc
            "--proto_path=backend=${proto_path}"
            "--python_out=${client_dir}"
            "--grpc_python_out=${client_dir}"
            "${proto}"
    DEPENDS "${proto}"
)
add_custom_target(${PROJECT_NAME}-client
    ALL
    DEPENDS ${protoc_out}
)

set(server_copy_out
    "${server_backend_dir}/${proto_name}_pb2.py"
    "${server_backend_dir}/${proto_name}_pb2_grpc.py"
)
add_custom_command(
    OUTPUT  ${server_copy_out}
    COMMAND ${CMAKE_COMMAND} -E copy "${client_backend_dir}/${proto_name}_pb2.py" ${server_backend_dir}
    COMMAND ${CMAKE_COMMAND} -E copy "${client_backend_dir}/${proto_name}_pb2_grpc.py" ${server_backend_dir}
    DEPENDS ${PROJECT_NAME}-client
)
add_custom_target(${PROJECT_NAME}-server
    ALL
    DEPENDS ${server_copy_out}
)

set(crt_out
    "${server_dir}/localhost.key"
    "${server_dir}/localhost.crt"
    "${client_dir}/localhost.crt"
)
add_custom_command(
    OUTPUT  ${crt_out}
    COMMAND openssl req -x509 -nodes -newkey rsa:2048 -sha256 -days 10000 -keyout "${server_dir}/localhost.key" -out "${server_dir}/localhost.crt" -subj /CN=localhost
    COMMAND ${CMAKE_COMMAND} -E copy "${server_dir}/localhost.crt" ${client_dir}
)
add_custom_target(${PROJECT_NAME}-crt
    ALL
    DEPENDS ${crt_out}
)
