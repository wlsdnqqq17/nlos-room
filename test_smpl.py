import numpy as np
import smplx
import torch
import trimesh

# Load rotation matrices (320 frames, 24 joints, 3x3 rotation matrix)
rotation_matrices = np.load("smpl_rotation_matrix.npy")
print(f"Loaded rotation matrices: {rotation_matrices.shape}")

# Select frame to visualize (0-319)
frame_idx = 100  # Try different frames to see the animation
frame_rotations = rotation_matrices[frame_idx]  # (24, 3, 3)

# Global orientation (root joint 0) and body pose (joints 1-23)
global_orient = torch.tensor(frame_rotations[0:1], dtype=torch.float32).unsqueeze(
    0
)  # (1, 1, 3, 3)
body_pose = torch.tensor(frame_rotations[1:], dtype=torch.float32).unsqueeze(
    0
)  # (1, 23, 3, 3)

try:
    model = smplx.create(model_path="models", model_type="smpl", gender="male")
except Exception as e:
    print(f"Error creating model: {e}")
    exit()

betas = torch.zeros([1, 10], dtype=torch.float32)

# pose2rot=False: input is already rotation matrices, not axis-angle
output = model(
    betas=betas, global_orient=global_orient, body_pose=body_pose, pose2rot=False
)
vertices = output.vertices.detach().cpu().numpy().squeeze()
faces = model.faces
mesh = trimesh.Trimesh(vertices, faces)
output_filename = "result.obj"
mesh.export(output_filename)
print(f"Frame {frame_idx} exported to '{output_filename}'")
mesh.show()
