import zmq
import numpy as np
import cv2
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="ZMQ Compressed Image Receiver")
    parser.add_argument(
        '--save_images', 
        type=bool, 
        default=False, 
        help="Save received images to disk",
    )
    parser.add_argument(
        '--output_folder', 
        type=str, 
        default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'outputs', 'images'), 
        help="Folder to save images if --save_images is True",
    )
    return parser.parse_args()

def main():

    args = parse_args()
    # Create a ZMQ context and socket
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")  # "localhost" is the hostname (resolves to an IP address), and "5555" is the port number
    socket.setsockopt(zmq.SUBSCRIBE, b"")   # Subscribe to all topics

    print("Waiting for images...")

    while True:
        # Receive the multipart message
        parts = socket.recv_multipart()
        if len(parts) != 4:
            print(f"Received unexpected number of parts: {len(parts)}")
            continue

        sec = int.from_bytes(parts[0], byteorder='little', signed=False) if isinstance(parts[0], bytes) else int(parts[0])
        nanosec = int.from_bytes(parts[1], byteorder='little', signed=False) if isinstance(parts[1], bytes) else int(parts[1])
        img_format = parts[2].decode()
        img_data = parts[3]

        print(f"Received image at {sec}.{nanosec}s in format: {img_format}, data length: {len(img_data)} bytes")

        arr = np.frombuffer(img_data, dtype=np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        print(f'converted image shape: {img.shape}')

        # ### Save to file for demonstration
        if args.save_images:
            os.makedirs(args.output_folder, exist_ok=True)
            img_name = f"image_{sec}_{nanosec}.{img_format}"
            with open(os.path.join(args.output_folder, img_name), 'wb') as f:
                f.write(img_data)

        print('\n')


if __name__ == "__main__":
    main()