import sys
import math


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


def calc_target_position(x, y, next_checkpoint_x, next_checkpoint_y, radius):
    angle_to_checkpoint = angle(x, y, next_checkpoint_x, next_checkpoint_y)

    target_x = next_checkpoint_x + radius * math.cos(angle_to_checkpoint)
    target_y = next_checkpoint_y + radius * math.sin(angle_to_checkpoint)

    return target_x, target_y


def adjust_target_position(target_x, target_y, speed, speed_direction):
    adjust_factor = 2250 * speed / max_speed
    dx = speed_direction[0]
    dy = speed_direction[1]
    adjusted_x = target_x - dx * adjust_factor
    adjusted_y = target_y - dy * adjust_factor
    return adjusted_x, adjusted_y



def calc_speed(speed_x, speed_y):
    return math.sqrt(speed_x ** 2 + speed_y ** 2)


def calc_speed_direction(vx, vy):
    norm = math.sqrt(vx ** 2 + vy ** 2)
    return vx / norm, vy / norm


def is_new_checkpoint(next_checkpoint_x, next_checkpoint_y, map_memory):
    for checkpoint in map_memory:
        if distance(next_checkpoint_x, next_checkpoint_y, checkpoint[0], checkpoint[1]) < 100:
            return False
    return True


def go_next_checkpoint(map_memory, next_cp_id):
    if next_cp_id == checkpoint_count - 1:
        return map_memory[0]
    else:
        return map_memory[next_cp_id + 1]

def calculate_distance_threshold(speed):
    return speed * 4.5


# game loop
map_memory = []
laps = int(input())
checkpoint_count = int(input())
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    map_memory.append((checkpoint_x, checkpoint_y))

boost_available = True
first_action = True
first_turn = True
checkpoint_radius = 600
enemy_radius = 400
previous_x = 0
previous_y = 0
speed = 0
speed_direction = 0, 0
max_speed = 961
while True:
    pod_data = []
    for i in range(2):
        # x: x position of your pod
        # y: y position of your pod
        # vx: x speed of your pod
        # vy: y speed of your pod
        # angle: angle of your pod
        # next_check_point_id: next check point id of your pod
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]
        pod_data.append((x, y, vx, vy, angle, next_check_point_id))
    
    opponent_positions = []
    for i in range(2):
        # x_2: x position of the opponent's pod
        # y_2: y position of the opponent's pod
        # vx_2: x speed of the opponent's pod
        # vy_2: y speed of the opponent's pod
        # angle_2: angle of the opponent's pod
        # next_check_point_id_2: next check point id of the opponent's pod
        x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2 = [int(j) for j in input().split()]
        opponent_positions.append((x_2, y_2, vx_2, vy_2, angle_2, next_check_point_id_2))

    for i in range(2):
        x, y, vx, vy, next_checkpoint_angle, next_check_point_id = pod_data[i]
        speed = calc_speed(vx, vy)
        speed_direction = calc_speed_direction(vx, vy)
        threshold = calculate_distance_threshold(speed)
        next_checkpoint_dist = distance(x, y, next_checkpoint_x, next_checkpoint_y)
        if next_checkpoint_dist < threshold:
            next_checkpoint_x, next_checkpoint_y = go_next_checkpoint(map_memory, next_check_point_id)
            print(f"NEXT CHECKPOINT: {next_checkpoint_x}, {next_checkpoint_y}", file=sys.stderr)

        target_x, target_y = calc_target_position(x, y, next_checkpoint_x, next_checkpoint_y, checkpoint_radius)
        target_x, target_y = adjust_target_position(target_x, target_y, speed, speed_direction)
        target_distance = distance(x, y, target_x, target_y)

        if abs(next_checkpoint_angle) < 2 and target_distance > 6000 and boost_available:
            boost = "BOOST"
            boost_available = False
        elif abs(next_checkpoint_angle) < 20:
            boost = "100"
        elif abs(next_checkpoint_angle) < 45:
            boost = "95"
        elif abs(next_checkpoint_angle) < 90:
            boost = "100"
        elif abs(next_checkpoint_angle) < 135:
            boost = "40"
        else:
            boost = "0"

        # Print all details in a readable way
        print(f"Position: {x}, {y}", file=sys.stderr)
        print(f"Speed: {speed}, Speed direction: {speed_direction}", file=sys.stderr)
        print(f"Threshold: {threshold}", file=sys.stderr)
        print(f"next_checkpoint_x: {next_checkpoint_x}, next_checkpoint_y: {next_checkpoint_y}", file=sys.stderr)
        print(f"map_memory: {map_memory}", file=sys.stderr)
        print(f"next_checkpoint_distance: {next_checkpoint_dist}, target_distance: {target_distance}", file=sys.stderr)
        print(f"boost: {boost}", file=sys.stderr)
        print(f"Angle: {next_checkpoint_angle}", file=sys.stderr)

        print(f"{int(target_x)} {int(target_y)} {boost}")
