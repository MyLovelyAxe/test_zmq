import zmq
import pickle

""" This socket is used to receive 3D reconstruction result messages.

The message is an numpy.array which consists of the following content:

- number of each partition
    shape: (3), i.e. [Num_Points, Num_Colors, Num_Cameras]
- point cloud position
    shape: (N, 3), i.e. (Num_Points, XYZ)
- point cloud colors
    shape: (N, 3), i.e. (Num_Colors, RGB)
- camera poses
    shape: (M*4, 3), i.e. the extrinsics of M cameras concatenated vertically
    each extrinsics E is a 4x3 matrix:
        - E[0, :]: translation vector (3,), i.e. (X, Y, Z)
        - E[1:4, :]: rotation matrix (3, 3)
"""

reconst_context = zmq.Context()
reconst_socket = reconst_context.socket(zmq.SUB)
reconst_socket.connect("tcp://127.0.0.1:5555")
reconst_socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

print("Waiting for messages...")
while True:

    msg = reconst_socket.recv()
    array = pickle.loads(msg)
    ### numbers of each partition
    num_points, num_colors, num_cameras = array[0].astype(int)
    print(f"Received 3D reconstruction message: num_points={num_points}, num_colors={num_colors}, num_cameras={num_cameras}")
    ### point cloud position
    point_cloud_positions = array[1:num_points + 1]
    print(f"Point cloud positions shape: {point_cloud_positions.shape}")
    ### point cloud colors
    point_cloud_colors = array[num_points + 1:num_points + num_colors + 1]
    print(f"Point cloud colors shape: {point_cloud_colors.shape}")
    ### camera poses
    camera_poses = array[num_points + num_colors + 1:]
    assert len(camera_poses) == num_cameras * 4, f"Wrong camera poses, i.e. len(camera_poses)={len(camera_poses)}, num_camerasx4={num_cameras}x4={num_cameras * 4}"
    cameras = dict()
    for i in range(num_cameras):
        camera_pose = camera_poses[i * 4:(i + 1) * 4]
        translation = camera_pose[0].reshape(1,3)
        rotation = camera_pose[1:4] # 3x3 rotation matrix
        print(f"Camera {i}: Translation={translation}, Rotation={rotation}")
        cameras[i] = dict(
            translation=translation,
            rotation=rotation,
        )

