from gymnasium import register

register(
    id="HumanoidWalk-v0",
    entry_point="sai_mujoco.humanoid_walk:HumanoidWalkEnv",
)

register(
    id="HumanoidObstacle-v0",
    entry_point="sai_mujoco.humanoid_obstacle:HumanoidObstacleEnv",
)

register(
    id="InvertedPendulumWheel-v0",
    entry_point="sai_mujoco.inverted_pendulum_wheel:InvertedPendulumWheelEnv",
)

register(
    id="RoboticArm-v0",
    entry_point="sai_mujoco.robotic_arm:RoboticArmEnv",
)
