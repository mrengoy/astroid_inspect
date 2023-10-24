from flatspin.model import PinwheelSpinIceDiamond
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Create a simple Matplotlib plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,10))
#line, = ax.plot(x, y)

asi_size = (5, 5)
model = PinwheelSpinIceDiamond(size=asi_size)
# Function to update the plot
spin_state = np.copy(model.spin)
def update_plot():
    alpha = alpha_item_s.get()
    dis_val = disorder_item_s.get()
    temperature = temperature_item_s.get()
    global model
    model = PinwheelSpinIceDiamond(
        size=asi_size,
        disorder=dis_val,
        temperature=temperature,
        alpha=alpha
    )
    global spin_state
    model.set_spin(spin_state)
    field_strength = field_strength_slider.get()
    field_angle = field_angle_slider.get()
    new_field = np.array([np.cos(field_angle), np.sin(field_angle)])*field_strength
    model.set_h_ext(new_field)
    tot_fields = model.total_fields() # Parallel fields, and perpendicular fields for every magnet
    
    (orange   ,) = np.where((model.spin == 1 ) & (model.angle > 0))
    (green ,) = np.where((model.spin == -1) & (model.angle < 0))
    (blue  ,) = np.where((model.spin == -1) & (model.angle > 0))
    (magenta,) = np.where((model.spin == 1 ) & (model.angle < 0))
    
    orange_mags = tot_fields[orange ]
    green_mags  = tot_fields[green  ]
    blue_mags   = tot_fields[blue   ]
    magenta_mags= tot_fields[magenta]
    ax2.cla()
    ax1.cla()
    model.plot(ax=ax1)
    ax2.scatter(orange_mags[:,0]    , orange_mags[:,1]  , color='orange')
    ax2.scatter(green_mags[:,0]     , green_mags[:,1]   , color='green')
    ax2.scatter(blue_mags[:,0]      , blue_mags[:,1]    , color='blue')
    ax2.scatter(magenta_mags[:,0]   , magenta_mags[:,1] , color='magenta')
    model.plot_astroid(ax=ax2, hc=0.2, angle_range=(np.pi/2, 3*np.pi/2))
    ax2.set_title('Flip astroid')
    ax2.set_xlabel('Total parallel field (H_par)')
    ax2.set_ylabel('Total perpendicular field (H_perp)')
    x = 0
    y = 0
    u = new_field[0]  # X-component of the vector
    v = new_field[1]  # Y-component of the vector
    ax1_shift = asi_size[0]/2
    ax1_scale = 50
    ax1.quiver(x+ax1_shift, y+ax1_shift, u*ax1_scale, v*ax1_scale, angles='xy', scale_units='xy', scale=1, color='blue', label='H_ext')
    ax2.quiver(x, y, u, v, angles='xy', scale_units='xy', scale=1, color='blue', label='H_ext')
    ax2.set_xlim(-0.1, 0.1)
    ax1.legend()
    ax2.legend()
    canvas.draw()
    root.after(100, update_plot)

# Create a Tkinter window
root = tk.Tk()
root.title("Matplotlib Plot with Widgets")

mygrid = tk.Frame(root)
mygrid.pack()
# Create and place interactive widgets
field_strength_label = tk.Label(mygrid, text="Field Strength (T):")
field_strength_label.grid(row=0, column=0)
field_strength_slider = tk.Scale(mygrid, from_=0.0, to=0.10, resolution=0.005, orient="horizontal", length=500)
field_strength_slider.set(0)
field_strength_slider.grid(row=0, column=1)

field_angle_label = tk.Label(mygrid, text="Field Angle (radians):")
field_angle_label.grid(row=1, column=0)
field_angle_slider = tk.Scale(mygrid, from_=0, to=2*np.pi, resolution=0.05, orient="horizontal", length=500)
field_angle_slider.set(1.0)
field_angle_slider.grid(row=1, column=1)

alpha_item = tk.Label(mygrid, text="Alpha")
alpha_item.grid(row=2, column=0)
alpha_item_s = tk.Scale(mygrid, from_=0, to=0.01, resolution=0.0005, orient="horizontal", length=500)
alpha_item_s.set(0.001)
alpha_item_s.grid(row=2, column=1)

disorder_item = tk.Label(mygrid, text="Disorder")
disorder_item.grid(row=3, column=0)
disorder_item_s = tk.Scale(mygrid, from_=0, to=0.1, resolution=0.005, orient="horizontal", length=500)
disorder_item_s.set(0.001)
disorder_item_s.grid(row=3, column=1)

temperature_item = tk.Label(mygrid, text="Temperature (K)")
temperature_item.grid(row=4, column=0)
temperature_item_s = tk.Scale(mygrid, from_=0, to=500, resolution=5, orient="horizontal", length=500)
temperature_item_s.set(0.001)
temperature_item_s.grid(row=4, column=1)

def relax_logic():
    global model
    model.relax()
    global spin_state
    spin_state = np.copy(model.spin)
relax_button= tk.Button(mygrid, text="Relax", command=relax_logic)
relax_button.grid(row=5, column=0)

def randomize_logic():
    global model
    model.randomize()
    global spin_state
    spin_state = np.copy(model.spin)

rand_state_button = tk.Button(mygrid, text="Randomize state", command=randomize_logic)
rand_state_button.grid(row=5, column=1)
update_button = tk.Button(mygrid, text="Exit", command=quit)
update_button.grid(row=5, column=2)

# Embed the Matplotlib plot in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()
update_plot()

# Start the Tkinter event loop
root.mainloop()


