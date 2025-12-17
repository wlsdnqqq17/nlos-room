import numpy as np

# mixamo -> smpl 매핑
# Mixamo: 0=Hips, 1-3=Spine, 4=Neck, 5=Head
#         7=LeftShoulder, 8=LeftArm, 9=LeftForeArm, 10=LeftHand
#         31=RightShoulder, 32=RightArm, 33=RightForeArm, 34=RightHand
#         55=LeftUpLeg, 56=LeftLeg, 57=LeftFoot, 58=LeftToeBase
#         60=RightUpLeg, 61=RightLeg, 62=RightFoot, 63=RightToeBase
# SMPL: 0=pelvis, 1=L_hip, 2=R_hip, 3=spine1, 4=L_knee, 5=R_knee, 6=spine2,
#       7=L_ankle, 8=R_ankle, 9=spine3, 10=L_foot, 11=R_foot, 12=neck,
#       13=L_collar, 14=R_collar, 15=head, 16=L_shoulder, 17=R_shoulder,
#       18=L_elbow, 19=R_elbow, 20=L_wrist, 21=R_wrist, 22=L_hand, 23=R_hand
d = {
    0: 0, 1: 3, 2: 6, 3: 9, 4: 12, 5: 15,
    6: -1, 7: 13, 8: 16, 9: 18, 10: 20,  # Left arm: LeftShoulder->L_collar, etc.
    11: -1, 12: -1, 13: -1, 14: -1, 15: -1,
    16: -1, 17: -1, 18: -1, 19: -1, 20: -1,
    21: -1, 22: -1, 23: -1, 24: -1, 25: -1,
    26: -1, 27: -1, 28: -1, 29: -1, 30: -1,
    31: 14, 32: 17, 33: 19, 34: 21, 35: -1,  # Right arm: RightShoulder->R_collar, etc.
    36: -1, 37: -1, 38: -1, 39: -1, 40: -1,
    41: -1, 42: -1, 43: -1, 44: -1, 45: -1,
    46: -1, 47: -1, 48: -1, 49: -1, 50: -1,
    51: -1, 52: -1, 53: -1, 54: -1,
    55: 1, 56: 4, 57: 7, 58: 10, 59: -1,  # Left leg: LeftUpLeg->L_hip, etc.
    60: 2, 61: 5, 62: 8, 63: 11, 64: -1,  # Right leg: RightUpLeg->R_hip, etc.
}

# Load Mixamo rotation (T, J, 3, 3)
mixamo_rot = np.load("mixamo_rotation_matrix.npy")
T, J, _, _ = mixamo_rot.shape

# Initialize SMPL rotation (T, 24, 3, 3) as identity
smpl_rot = np.tile(np.eye(3)[None, None, :, :], (T, 24, 1, 1))

# Fill mapped joints
for mixamo_idx, smpl_idx in d.items():
    if smpl_idx == -1:
        continue
    if mixamo_idx >= J:
        continue  # 안전 장치
    smpl_rot[:, smpl_idx] = mixamo_rot[:, mixamo_idx]

# Save
np.save("smpl_rotation_matrix.npy", smpl_rot)

print("Done! Saved smpl_rotation_matrix.npy")

