import math

MAX_ANGLE = 100

for i in range(MAX_ANGLE * 2 // 5 + 1):
    angle_deg = -MAX_ANGLE + i * 5
    angle_rad = math.radians(angle_deg)
    sin_val = int(round(math.sin(angle_rad) * 1000))
    cos_val = int(round(math.cos(angle_rad) * 1000))
    print(f"        let sinTable[{i}] = {sin_val}; let cosTable[{i}] = {cos_val}; // {angle_deg}°")
