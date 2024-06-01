from pynput import mouse
import time
import matplotlib.pyplot as plt
from screeninfo import get_monitors
import numpy as np
from matplotlib import colors
import subprocess
import os

monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

coordinates = []
clicks = []


def on_move(x, y):
    coordinates.append((x, y))


def on_click(x, y, button, pressed):
    if pressed:
        clicks.append((x, y))


with mouse.Listener(on_move=on_move, on_click=on_click) as listener:
    time.sleep(10)
    listener.stop()

output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

mouse_coordinates_path = os.path.join(output_dir, "mouse_coordinates.txt")
with open(mouse_coordinates_path, "w") as file:
    for x, y in coordinates:
        file.write(f"{x}, {y}\n")
    for x, y in clicks:
        file.write(f"{x}, {y} CLICK\n")

num_points = 1000
indices = np.linspace(0, len(coordinates) - 1, num_points, dtype=int)
x_coords_sampled = [coordinates[i][0] for i in indices]
y_coords_sampled = [coordinates[i][1] for i in indices]

color_map = plt.get_cmap('viridis')
norm = colors.Normalize(vmin=0, vmax=len(coordinates))
color_samples = [color_map(norm(i)) for i in range(len(coordinates))]

if coordinates:
    plt.figure(figsize=(screen_width / 100, screen_height / 100), dpi=100)
    plt.scatter(x_coords_sampled, screen_height - np.array(y_coords_sampled), c=np.arange(num_points), cmap='viridis',
                label='Mouse Movement')
    plt.plot(x_coords_sampled, screen_height - np.array(y_coords_sampled), color='blue')

for i, click_coord in enumerate(clicks):
    plt.scatter(click_coord[0], screen_height - click_coord[1], color='red')
    plt.text(click_coord[0] + 10, screen_height - click_coord[1] + 10, str(i + 1), fontsize=8, color='black')

plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.title('Mouse Movement and Clicks')
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar(label='Time')

mouse_movement_path = os.path.join(output_dir, "mouse_movement.png")
plt.savefig(mouse_movement_path)
plt.close()

batch_file_path = os.path.join(os.path.dirname(__file__), "subprocess.bat")
subprocess.run(batch_file_path, shell=True)
