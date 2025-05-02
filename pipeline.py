import subprocess
from ete3 import Tree
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image
import sys
import os


# Function to handle file paths in PyInstaller for icon and background pic
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


# Variables
aligned_file = "aligned_sequences.fasta"
tree_file = "phylogenetic_tree.nw"


# Midpoint rooting with ete3
def midpoint_root(tree):
    tree.set_outgroup(tree.get_midpoint_outgroup())
    return tree


# Button for user to select FASTA files
def select_fasta_files():
    root = tk.Tk()
    root.withdraw()
    fasta_files = filedialog.askopenfilenames(
        title="Select FASTA files",
        filetypes=[("FASTA files", "*.fasta *.fa")]
    )
    return list(fasta_files)


# Combines FASTA files into one
def combine_fasta_files(fasta_files):
    with open("combined_sequences.fasta", "w") as outfile:
        for file in fasta_files:
            with open(file) as infile:
                outfile.write(infile.read())


# Aligns the sequences
def align_sequences():
    clustal_command = [
        "clustalo",
        "-i", "combined_sequences.fasta",
        "-o", "aligned_sequences.fasta",
        "--force",
        "--full",
        "--iterations=3"
    ]
    try:
        subprocess.run(clustal_command, check=True)
        print("Alignment complete. Results saved to aligned_sequences.fasta")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Clustal Omega alignment failed: {e}")


# Shows user the tree
def display_tree(canvas_frame):
    fasttree_command = [
        "fasttree.exe",
        "-wag",
        aligned_file
    ]
    try:
        # Run FastTree to generate the tree
        result = subprocess.run(fasttree_command, capture_output=True, text=True, check=True)
        with open(tree_file, 'w') as tree_output:
            tree_output.write(result.stdout)
        print(f"Phylogenetic tree saved to {tree_file}.")
        tree = Tree(tree_file, quoted_node_names=True, format=0)
        tree = midpoint_root(tree)
        tree.resolve_polytomy()
        tree.write(outfile=tree_file)
        tree.render("tree_image.png", w=800, units="px")
        img = Image.open("tree_image.png")
        tree_width, tree_height = img.size
        app.geometry(f"{tree_width}x{tree_height + 150}")
        fig, ax = plt.subplots(figsize=(8, 6))
        img = plt.imread("tree_image.png")
        ax.imshow(img)
        ax.axis("off")
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        return tree
    except subprocess.CalledProcessError as e:
        error_message = e.stderr if e.stderr else "Unknown error"
        raise RuntimeError(f"Error generating tree: {error_message}")
    except Exception as e:
        raise RuntimeError(f"Error in tree processing: {str(e)}")


# Was still running in processes after closing. This completely terminates it
def on_closing():
    plt.close("all")
    app.destroy()
    sys.exit()


def run_pipeline():
    selected_files = select_fasta_files()
    if selected_files:
        try:
            combine_fasta_files(selected_files)
            align_sequences()
            tree = display_tree(tree_frame)
            print(tree)
            messagebox.showinfo("Success", "Pipeline completed successfully")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showwarning("No files", "Please select FASTA files to continue.")


# Program aesthetics
app = ttk.Window(themename="cosmo")
app.title("Mike's Phylogenetic Tree Generator")
app.geometry("500x500")
app.iconbitmap(resource_path("icon.ico"))  # Set the window icon
bg_image = tk.PhotoImage(file=resource_path("Tree Background pic resized.png"))
bg_label = tk.Label(app, image=bg_image)
bg_label.place(relx=0.5, rely=0.6, anchor="center", relwidth=0.7, relheight=0.7)
main_frame = ttk.Frame(app)
main_frame.place(relx=0, rely=0)
ttk.Label(app, text="Let's make a tree, shall we?!", font=("Arial", 20, "bold"), anchor="center").pack(pady=10)
tree_frame = ttk.Frame(main_frame, style="Transparent.TFrame")
app.style.configure("Transparent.TFrame", background="#00000000")
tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
run_button = ttk.Button(app, text="Select FASTA Files and Run", command=run_pipeline)
run_button.pack(pady=20)
footer_label = ttk.Label(app, text="Created by Michael Weingart, Job Hunter", font=("Verdana", 8, "italic"),
                         anchor="center")
footer_label.pack(side="bottom", pady=5)

# For closing function
app.protocol("WM_DELETE_WINDOW", on_closing)

app.mainloop()
