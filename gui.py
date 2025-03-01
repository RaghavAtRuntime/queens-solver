import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from image_processor import ImageProcessor
from solver import Solver

class QueensSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Queens Solver with Dynamic Board Detection")

        # Variables
        self.image_path = None
        self.board = []
        self.n = 0
        self.regions = {}
        self.current_region_id = 0

        # GUI Components
        self.label = tk.Label(root, text="Upload a screenshot of the game board:")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.solve_button = tk.Button(root, text="Solve", command=self.solve_board)
        self.solve_button.pack(pady=10)

    def upload_image(self):
        """Allows the user to upload an image of the game board."""
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", ".png .jpg .jpeg")])
        if not self.image_path:
            return

        # Load and display the image
        image = Image.open(self.image_path)
        image.thumbnail((400, 400))
        self.tk_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # Process the image to detect the board and regions
        self.process_image(self.image_path)

    def process_image(self, image_path):
        """Processes the image to detect the board and regions."""
        processor = ImageProcessor()
        self.board, self.n, self.regions = processor.process_image(image_path)

        print(f"Detected Board Size: {self.n}x{self.n}")
        print("Detected Board:")
        for row in self.board:
            print(row)

    def solve_board(self):
        """Solves the board using the backtracking solver."""
        if not self.regions:
            messagebox.showwarning("Warning", "No regions detected. Please upload a valid image.")
            return

        solver = Solver()
        solution = solver.solve(self.board, self.regions)

        if solution:
            # Display the solution on the canvas
            self.display_solution(solution)
            messagebox.showinfo("Solution Found", "The board has been solved!")
        else:
            messagebox.showinfo("No Solution", "No solution found.")

    def display_solution(self, solution):
        """Displays the solution on the canvas."""
        cell_size = 400 // self.n
        for r, c in solution:
            x1 = c * cell_size
            y1 = r * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black")
            self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="X", font=("Arial", 16), fill="red")
