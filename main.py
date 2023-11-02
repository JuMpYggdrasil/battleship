import tkinter as tk

# Define the size of the Battleship grid
grid_size = 10

# Create an empty grid to represent the known information
# 0 represents an unknown square, 1 represents a hit, and -1 represents a miss
grid = [[0] * grid_size for _ in range(grid_size)]

# Define the number of remaining ships and their sizes
remaining_ships = {
    "Aircraft Carrier(5)": 5,
    "Battleship(4)": 4,
    "Cruiser(3)": 3,
    "Submarine(3)": 3,
    "Destroyer(2)": 2,
    "boat-1(1)": 1,
    "boat-2(2)": 2,
    "boat-3(3)": 3,
    "boat-4(4)": 4,
}

# Create the Tkinter application
app = tk.Tk()
app.title("Battleship Probability Calculator")

# Create a frame for the checkboxes
checkbox_frame = tk.Frame(app)
checkbox_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Create a frame for the grid
grid_frame = tk.Frame(app)
grid_frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a list of IntVar variables to store checkbox states
checkbox_vars = {ship: tk.IntVar() for ship in remaining_ships}

# Function to calculate the probability in each position
def calculate_probability():
    probabilities = [[0.0] * grid_size for _ in range(grid_size)]

    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == 0:
                for ship, size in remaining_ships.items():
                    if checkbox_vars[ship].get() == 1:  # Only calculate for selected ships
                        for direction in [(1, 0), (0, 1)]:
                            prob = 1.0
                            for i in range(size):
                                r, c = row + i * direction[0], col + i * direction[1]
                                if not (0 <= r < grid_size and 0 <= c < grid_size) or grid[r][c] == -1:
                                    prob = 0.0
                                    break

                            for i in range(size):
                                r, c = row + i * direction[0], col + i * direction[1]
                                if 0 <= r < grid_size and 0 <= c < grid_size:
                                    probabilities[r][c] += prob

    return probabilities

# Function to handle mouse click events
def on_grid_click(row, col):
    if grid[row][col] == 0:
        grid[row][col] = -1  # Mark as missed
        probabilities = calculate_probability()  # Recalculate probabilities
        display_grid(probabilities)  # Display updated grid with probabilities

# Function to display the grid with probability values and red background for missed squares
def display_grid(probabilities):
    for widget in grid_frame.winfo_children():
        widget.destroy()  # Clear the grid_frame
    
    for row in range(grid_size):
        for col in range(grid_size):
            prob = probabilities[row][col]
            if grid[row][col] == -1:
                label = tk.Label(grid_frame, text=f'{prob:.2f}', width=6, height=1, relief=tk.RAISED, bg='red')
            else:
                label = tk.Label(grid_frame, text=f'{prob:.2f}', width=6, height=1, relief=tk.RAISED)
            label.grid(row=row, column=col)
            label.bind("<Button-1>", lambda event, r=row, c=col: on_grid_click(r, c))

# Function to update the displayed grid when checkboxes are updated
def update_grid():
    probabilities = calculate_probability()  # Recalculate probabilities
    display_grid(probabilities)  # Display updated grid with probabilities

# Create and display the initial grid
initial_probabilities = calculate_probability()
display_grid(initial_probabilities)

# Create Checkbutton widgets for ship selection
for ship in remaining_ships:
    checkbox = tk.Checkbutton(checkbox_frame, text=ship, variable=checkbox_vars[ship], command=update_grid)
    checkbox.pack(anchor=tk.W)

# Start the Tkinter main loop
app.mainloop()
