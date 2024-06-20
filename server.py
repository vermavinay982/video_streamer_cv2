import cv2
import socket
import pickle
import struct
import time 

# file_path = r"flower_test.mp4"   
file_path = 0 # if using camera for streaming

global video_capture
video_capture = None

def init_video():
    global video_capture
    # Initialize video capture from the default camera
    video_capture = cv2.VideoCapture(file_path)

init_video()

# Create a socket server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_address = ('127.0.0.1', 8000)

    server_socket.bind(server_address)  
    server_socket.listen(10)
    print(f"Server Started at: {server_address}")

    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f"[*] Accepted connection from {client_address}")

    while True:
        # Read a frame from the camera
        ret, frame = video_capture.read()

        if not ret:
            print("Frame Damaged, Restarting")
            time.sleep(2)
            init_video()
            continue

        # Serialize the frame to bytes
        serialized_frame = pickle.dumps(frame)

        # Pack the data size and frame data
        message_size = struct.pack("L", len(serialized_frame))
        client_socket.sendall(message_size + serialized_frame)

        # Display the frame on the server-side (optional)
        cv2.imshow('Server Video', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    video_capture.release()
    cv2.destroyAllWindows()
    server_socket.close()
