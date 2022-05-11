import os
import tkinter as tk
from configparser import ConfigParser
import logging

from .folders import FolderStructure
from .sources import Source
from .processor import Processor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class Gui:

    def __init__(self, config: ConfigParser, folders: FolderStructure, processor: Processor) -> None:
        self.config = config
        self.folders = folders
        self.processor = processor
        self.source = Source(self.config)

        self.root = tk.Tk() 
        self.root.title("Data Matrix Sorter and Labeler")
        self.root.geometry("1000x600") 

        self.checkbox_input_var = tk.IntVar()
        self.checkbox_paths_var = tk.IntVar()
        self.checkbox_output_var = tk.IntVar()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        frame_top_left = tk.Frame(self.root, bg='cyan', width=250, height=150, pady=3)
        frame_top_center = tk.Frame(self.root, bg='white', width=250, height=150, pady=3)
        frame_top_right = tk.Frame(self.root, bg='cyan', width=500, height=150, pady=3)
        frame_bottom_left = tk.Frame(self.root, bg='lavender', width=250, height=450, pady=3)
        frame_bottom_center = tk.Frame(self.root, bg='gray', width=250, height=450, pady=3)
        frame_bottom_right = tk.Frame(self.root, bg='lavender', width=500, height=450, pady=3)

        frame_top_left.grid(row=0, column=0, sticky='ew')
        frame_top_center.grid(row=0, column=1, sticky='ew')
        frame_top_right.grid(row=0, column=2,  sticky='ew')
        frame_bottom_left.grid(row=1, column=0, sticky='ns')
        frame_bottom_center.grid(row=1, column=1, sticky='ns')
        frame_bottom_right.grid(row=1, column=2, sticky='nsew')

        self.__fill_frame_input(frame_top_left)
        self.__fill_frame_db(frame_top_center)
        self.__fill_frame_scroll_one(frame_bottom_left)
        self.__fill_frame_scroll_two(frame_bottom_center)


    def mainloop(self):
        self.root.mainloop() 

    def __fill_frame_input(self, frame):
        input_frame = tk.LabelFrame(frame, text='Input photos')
            
        checkbox_input = tk.Checkbutton(input_frame, text=f'Input folder [{ self.source.count_input() }]', variable=self.checkbox_input_var)
        if int(self.config['SOURCES']['input_folder']):
            checkbox_input.select()
        checkbox_input.pack(anchor=tk.W, padx=5)

        checkbox_paths = tk.Checkbutton(input_frame, text=f'Paths [{ self.source.count_input() }]', variable=self.checkbox_paths_var)
        if int(self.config['SOURCES']['paths']):
            checkbox_paths.select()
        checkbox_paths.pack(anchor=tk.W, padx=5)

        checkbox_output = tk.Checkbutton(input_frame, text=f'Output folder [{ self.source.count_output(self.folders) }]', variable=self.checkbox_output_var)
        if int(self.config['SOURCES']['output_folder']):
            checkbox_output.select()
        checkbox_output.pack(anchor=tk.W, padx=5)

        button_frame = tk.Frame(
            master=input_frame,
            #relief=tk.RAISED,
            borderwidth=1
        )
        button_frame.pack(fill=tk.Y)

        button_edit_paths = tk.Button(button_frame, text="Edit Paths", command=self.handle_click_edit_paths)
        button_edit_paths.grid(column=0, row=0, padx=5, pady=5)

        button_input_output = tk.Button(button_frame, text="Proceed", command=self.handle_click_input_proceed)
        button_input_output.grid(column=1, row=0, padx=5, pady=5)

        input_frame.pack(side=tk.LEFT)

    def __fill_frame_db(self, frame):
        input_frame = tk.LabelFrame(frame, text='Input reference file')
        input_frame.pack(side=tk.LEFT,  padx=5)

        label_reference = tk.Label(input_frame, text='245 lines, UID for 12 is needed')
        label_reference.pack()

        button_generate_labels = tk.Button(input_frame, text="Generate Labels")
        button_generate_labels.pack()

        button_generate_uids = tk.Button(input_frame, text="Generate UIDs")
        button_generate_uids.pack()

    def __fill_frame_scroll_one(self, frame):
        myscroll = tk.Scrollbar(frame) 
        mylist = tk.Listbox(frame, yscrollcommand = myscroll.set )  
        for line in range(1, 100): 
            mylist.insert(tk.END, "Number " + str(line)) 
        mylist.pack(side = tk.LEFT, fill = tk.BOTH )    
        myscroll.pack(side = tk.RIGHT, fill = tk.Y) 

    def __fill_frame_scroll_two(self, frame):
        myscroll = tk.Scrollbar(frame) 
        mylist = tk.Listbox(frame, yscrollcommand = myscroll.set )  
        for line in range(1, 100): 
            mylist.insert(tk.END, "Number " + str(line)) 
        mylist.pack(side = tk.LEFT, fill = tk.BOTH )    
        myscroll.pack(side = tk.RIGHT, fill = tk.Y) 

    def handle_click_input_proceed(self):
        if self.checkbox_input_var.get():
            logger.debug('Processing input folder')
            self.processor.exec_from_input()
            
        if self.checkbox_paths_var.get():
            logger.debug('Processing paths')
            self.processor.exec_from_paths()

        if self.checkbox_output_var.get():
            logger.debug('Processing output folder')
            self.processor.exec_from_output()

    def handle_click_edit_paths(self):
        paths_file_path = os.path.join(
            os.getcwd(), 
            self.config['PATHS']['paths_file']
        )
        # TODO next line is definitely not cross platform
        os.system('gedit %s' % paths_file_path)



if __name__ == '__main__':
    main()
