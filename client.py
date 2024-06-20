import cv2
import socket
import pickle
import struct

server_address = ('127.0.0.1', 8000)


# Create a socket client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as video_client_socket:
    video_client_socket.connect(server_address)  
    received_data = b""
    payload_size = struct.calcsize("L")

    while True:
        # Receive and assemble the data until the payload size is reached
        while len(received_data) < payload_size:
            received_data += video_client_socket.recv(4096)

        # Extract the packed message size
        packed_msg_size = received_data[:payload_size]
        received_data = received_data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Receive and assemble the frame data until the complete frame is received
        while len(received_data) < msg_size:
            received_data += video_client_socket.recv(4096)

        # Extract the frame data
        frame_data = received_data[:msg_size]
        received_data = received_data[msg_size:]

        # Deserialize the received frame
        received_frame = pickle.loads(frame_data)

        # Display the received frame
        cv2.imshow('Client Video', received_frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cv2.destroyAllWindows()
    video_client_socket.close()