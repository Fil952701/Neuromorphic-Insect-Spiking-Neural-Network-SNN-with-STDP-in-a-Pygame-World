# SNN-STDP to simulate a behiavour of an insect who wants to catch food

import pygame
import random
import math
import importlib
import sys
import SNN_insect_brain as sb

importlib.reload(sb)
print("Using UPDATED step_snn!")

# Distance function
def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# Smell around food function
def get_smell_intensity(x, y, food_x, food_y, max_distance=1000):
    d = distance(x, y, food_x, food_y)
    return max(0, 1 - d / max_distance)

# Unified odor‐input function (Opzione B)
def get_odor_inputs(insect_pos, food_pos, max_distance=400):
    ix, iy = insect_pos
    fx, fy = food_pos
    inputs = []
    # per ciascuna delle 8 direzioni
    for dx, dy in directions:
        sx, sy = ix + dx * 10, iy + dy * 10
        # usa la stessa max_distance
        inputs.append(get_smell_intensity(sx, sy, fx, fy, max_distance))
    return inputs

# GUI initialization
pygame.init()
font = pygame.font.SysFont(None, 30)

# Defining insect random environment
WIDTH, HEIGHT = 800, 600
# GUI execution
WHITE = (255, 255, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNN Environment")

# insect, neurons and food features
INSECT_COLOR = (0, 0, 255)
FOOD_COLOR = (0, 255, 0)
INSECT_RADIUS = 10
FOOD_RADIUS = 8
SENSOR_COLOR = (100, 100, 255)
SENSOR_RADIUS = 5

# FPS for clock
clock = pygame.time.Clock()
FPS = 60

# initial position of the insect
insect_x = random.randint(0, WIDTH)
insect_y = random.randint(0, HEIGHT)
# random food position
food_x = random.randint(100, WIDTH - 100)
food_y = random.randint(100, HEIGHT - 100)

# Offset dx, dy for every possible movement (N, NE, E, SE, S, SW, W, NW)
sensor_offsets = [
    (0, -20),   # N
    (14, -14),  # NE
    (20, 0),    # E
    (14, 14),   # SE
    (0, 20),    # S
    (-14, 14),  # SW
    (-20, 0),   # W
    (-14, -14), # NW
]

# Normalized possible directions to take (N, NE, E, SE, S, SW, W, NW)
directions = [
    (0, -1), (1, -1), (1, 0), (1, 1),
    (0, 1), (-1, 1), (-1, 0), (-1, -1)
]
# Labels for every direction
direction_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

# Map to label the vectors
direction_vectors = {
    'N': (0, -20),
    'NE': (14, -14),
    'E': (20, 0),
    'SE': (14, 14),
    'S': (0, 20),
    'SW': (-14, 14),
    'W': (-20, 0),
    'NW': (-14, -14),
    'Random': (0, 0),
    'Idle': (0, 0)
}

# Main loop
print("Program started")
running = True
while running:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
    # smelling stimulations
    odor_inputs = get_odor_inputs((insect_x, insect_y),
                              (food_x, food_y),
                              max_distance=math.hypot(WIDTH, HEIGHT))
    #fired = sb.step_snn([i * 2 for i in odor_inputs], duration=20*b.ms)
    print("Odor inputs:", odor_inputs)
    fired = sb.step_snn(odor_inputs)
    print("Spikes this frame:", fired)
    # Determine direction from SNN based on which sensory neurons emitted spikes
    direction_label = 'Idle'  # default, if none has fired
    speed = 5 # try some values between 5 and 10
    if fired:
        counts = __import__('numpy').bincount(fired, minlength=8) # with this snippet, when the neuron fires, i choose the most spiking neuron among all of them
        most_active = __import__('numpy').argmax(counts)
        dx, dy = directions[most_active]
        direction_label = direction_labels[most_active]
    else:
        # fallback
        dx, dy = random.choice(directions)
        direction_label = 'Random'
    arrow_dx, arrow_dy = dx * speed, dy * speed
    insect_x += arrow_dx
    insect_y += arrow_dy
    # limiting the edges
    insect_x = max(0, min(WIDTH, insect_x))
    insect_y = max(0, min(HEIGHT, insect_y))
    # Odor intensities from 8 directions
    sensor_inputs = []
    sensor_positions = []
    # for every possibile movement get the intensity of the smell
    for dx, dy in sensor_offsets:
        sx, sy = insect_x + dx, insect_y + dy
        intensity = get_smell_intensity(sx, sy, food_x, food_y)
        sensor_inputs.append(intensity)
        sensor_positions.append((sx, sy))
    # food found?
    if distance(insect_x, insect_y, food_x, food_y) < (INSECT_RADIUS + FOOD_RADIUS):
        print("Food found!")
        # eliminate that found food
        food_x = random.randint(100, WIDTH - 100)
        food_y = random.randint(100, HEIGHT - 100)

    # Environment window
    WIN.fill(WHITE)
    pygame.draw.circle(WIN, INSECT_COLOR, (insect_x, insect_y), INSECT_RADIUS)
    # Show the arrow for the direction chosen
    dx, dy = direction_vectors[direction_label]
    arrow_start = (insect_x, insect_y) # the origin point of the insect
    arrow_end = (insect_x + arrow_dx, insect_y + arrow_dy) # the movement of the insect multiplied for the speed of the insect itself
    pygame.draw.line(WIN, (255, 0, 0), arrow_start, arrow_end, 3)  # red frame of the arrow
    pygame.draw.circle(WIN, (255, 0, 0), arrow_end, 4)  # red edge of the arrow
    # Show the food on the screen
    pygame.draw.circle(WIN, FOOD_COLOR, (food_x, food_y), FOOD_RADIUS)
    # Show logs of the direction chosen
    text = font.render(f'Direction: {direction_label}', True, (0, 0, 0))
    WIN.blit(text, (10, 10))    

    # Draw sensors with opacity based on odor intensity
    for (sx, sy), intensity in zip(sensor_positions, sensor_inputs):
        if 0 <= sx < WIDTH and 0 <= sy < HEIGHT:
            # 1) alpha between [0,255]
            alpha = int(255 * intensity)
            # 2) surface double dimension of the radius
            sensor_surf = pygame.Surface((SENSOR_RADIUS*2, SENSOR_RADIUS*2), pygame.SRCALPHA)
            # 3) color rgba
            rgba = (SENSOR_COLOR[0], SENSOR_COLOR[1], SENSOR_COLOR[2], alpha)
            # 4) circle with same coordinates
            pygame.draw.circle(sensor_surf, rgba, (SENSOR_RADIUS, SENSOR_RADIUS), SENSOR_RADIUS)
            # 5) offset correction
            WIN.blit(sensor_surf, (int(sx) - SENSOR_RADIUS, int(sy) - SENSOR_RADIUS))

    pygame.display.update()

pygame.quit()
# Plot SNN metrics
sb.plot_spikes()
sb.plot_weights()
sys.exit()