# this imports the code from files and modules
import gradio as gr
import utilities as u
import os
import ctypes


# This is a fix for the way that python doesn't release system memory back to the OS and it was leading to locking up the system
libc = ctypes.cdll.LoadLibrary("libc.so.6")
M_MMAP_THRESHOLD = -3

# Set malloc mmap threshold.
libc.mallopt(M_MMAP_THRESHOLD, 2**20)

# Declare accessible directories
base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where the script is located
print(f"Base Directory :",base_dir)
list_of_static_dir = [os.path.join(base_dir, "output"), 
                    os.path.join(base_dir, "dependencies"),
                    os.path.join(base_dir, "galleries")] 
gr.set_static_paths(paths=list_of_static_dir)

# Build gradio app
# Storing everything inside the Blocks to be accessible to the app

with gr.Blocks() as demo:
    # Functions and State Variables
    state_name = gr.State()

    def general_function():
        return 
    with gr.Tab("Name of Tab"):
        image_path_list= u.absolute_path("./folder_with_images")
        
        gr.HTML(""" <div id="inner"> <header>
                <h1>Title of Tool</h1>
               
                </div>""")
        
        md_instructions_header = """## How It Works:
        \n This tool does things. \n
        ** If you are new, expore the tabs above, look at some examples ** """
        gr.Markdown(md_instructions_header)
        
    with gr.Tab("Name of Tab"):
        image_path_list= u.absolute_path("./folder_with_images")
        
        gr.HTML(""" <div id="inner"> <header>
                <h1>Title of Tool</h1>
               
                </div>""")
        
        md_instructions_header = """## How It Works:
        \n This tool does things. \n
        ** If you are new, expore the tabs above, look at some examples ** """
        gr.Markdown(md_instructions_header)
        
    if __name__ == "__main__":
        demo.launch(allowed_paths=list_of_static_dir)  

