from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from PIL import Image as pil
import numpy as np
import os
import time
import pickle
import re

class SmartStitch(Tk):
    def __init__(self, *args, **kwargs):
        # Initalizes a tk window with the give parameters of the constructor.
        Tk.__init__(self, *args, **kwargs)

        # Global Variables
        self.input_folder = StringVar()
        self.output_folder = StringVar()
        self.split_height = StringVar(value="5000")
        self.senstivity = StringVar(value="90")
        self.status = StringVar(value="Idle")
        self.output_type = StringVar(value=".jpg")
        self.progress = ""
        self.actionbutton = ""
        self.batchButton = ""
        self.batch = False
        self.start = 0

        # Componant Setup
        self.SetupWindow()
        self.SetupBrowseFrame().grid(row=0, column=0, padx=(15), pady=(15), sticky="new")
        self.SetupSettingsFrame().grid(row=1, column=0, padx=(15), pady=(0,15), sticky="new")
        self.SetupStatusFrame().grid(row=2, column=0, padx=(15), pady=(0,15), sticky="new")
        self.SetupActionFrame().grid(row=3, column=0, padx=(15), pady=(0,15), sticky="new")
        self.LoadPrevSettings()

    def geticon(self, relative_path):    
        if not hasattr(sys, "frozen"):
            relative_path = os.path.join(os.path.dirname(__file__), relative_path)
        else:
            relative_path = os.path.join(sys.prefix, relative_path)
        return relative_path

        # return os.path.join(base_path, relative_path)
    def SetupWindow(self):
        # Sets up Title and Logo
        self.title('SmartStitch by MechTechnology [1.4]')
        self.iconbitmap(default=self.geticon("SmartStitchLogo.ico"))

        # Sets Window Size, centers it on Launch and Prevents Resize.
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (self.winfo_screenwidth()/2) - (window_height/2) - 120
        y = (self.winfo_screenheight()/2) - (window_width/2) - 40
        self.geometry('+%d+%d' % (x, y))
        self.columnconfigure(0, weight=1)
        self.resizable(False, False)

    def LoadPrevSettings(self):
        # loads the setting on start up (creates if it does not exist)
        settings_pickle = "settings.pickle"
        if not os.path.exists(settings_pickle):
            self.SaveCurrentSettings()
        else:
            with open(settings_pickle, "rb") as settings_handle:
                settings = pickle.load(settings_handle)
                self.split_height.set(settings[0])
                self.senstivity.set(settings[1])
                self.output_type.set(settings[2])

    def SaveCurrentSettings(self, *args):
        # Saves the settings
        settings = []
        settings.append(self.split_height.get())
        settings.append(self.senstivity.get())
        settings.append(self.output_type.get())

        settings_pickle = "settings.pickle"
        with open(settings_pickle, 'wb') as settings_handle:
            pickle.dump(settings, settings_handle)

    def SetupBrowseFrame(self):
        # Browse Button and Input and Output Field
        browse_frame = Frame(self)
        browse_label = ttk.Label(browse_frame, text = 'Input Path')
        browse_field = ttk.Entry(browse_frame, textvariable=self.input_folder)
        browse_field.bind("<Any-KeyRelease>", self.UpdateOutputFolder)
        browse_button = ttk.Button(browse_frame, text = 'Browse', command=self.BrowseToCommand)
        self.batchButton = ttk.Button(browse_frame, text = 'Batch', command=self.BatchToCommand)
        style = ttk.Style()
        style.configure("BW.TButton", foreground="green", background="green")
        output_label = ttk.Label(browse_frame, text = 'Output Path')
        output_field = ttk.Entry(browse_frame, textvariable=self.output_folder)
        browse_label.grid(row = 0,column = 0, sticky="new")
        browse_field.grid(row = 1, column = 0, pady=(2,0), sticky="new")
        browse_button.grid(row = 1,column = 1, padx=(15, 0), sticky="ne")
        self.batchButton.grid(row = 1,column = 1, pady=(30, 0), padx=(15, 0), sticky="ne")
        output_label.grid(row = 2, column = 0, sticky="new")
        output_field.grid(row = 3, column = 0, columnspan=2, pady=(2,0), sticky="new")
        browse_frame.columnconfigure(0, weight=1)
        return browse_frame

    def BatchToCommand(self):
        if(self.batch):
            self.batch = False
            self.batchButton['style'] = ""
        else:
            self.batch = True
            self.batchButton['style'] = "BW.TButton"
        
        self.batchButton.update()

    def BrowseToCommand(self):
        # Allow user to select a directory and updates input_folder and output_folder
        foldername = filedialog.askdirectory()
        self.input_folder.set(foldername)
        self.output_folder.set(foldername + " [Stitched]")

    def UpdateOutputFolder(self, *args):
        foldername = self.input_folder.get()
        self.output_folder.set(foldername + " [Stitched]")

    def SetupSettingsFrame(self):
        # Browse Split Field and Senstivity Fields
        settings_frame = Frame(self)
        split_label = ttk.Label(settings_frame, text = 'Rough Panel Height (In Pixels):')
        split_field = ttk.Entry(settings_frame, textvariable=self.split_height, validate='all')
        split_field.bind("<Any-KeyRelease>", self.SaveCurrentSettings)
        split_field['validatecommand'] = (split_field.register(self.AllowNumOnly),'%P','%d','%s')
        senstivity_label = ttk.Label(settings_frame, text = 'Bubble Detection Senstivity (0-100%):')
        senstivity_field = ttk.Entry(settings_frame, textvariable=self.senstivity, validate='all')
        senstivity_field.bind("<Any-KeyRelease>", self.SaveCurrentSettings)
        senstivity_field['validatecommand'] = (senstivity_field.register(self.AllowPercentOnly),'%P','%d','%s')
        type_label = ttk.Label(settings_frame, text = 'Output Images Type:')
        type_dropdown = ttk.Combobox(settings_frame, textvariable=self.output_type, values=('.jpg', '.png', '.webp', '.bmp', '.tiff', '.tga'))
        type_dropdown.bind("<<ComboboxSelected>>", self.SaveCurrentSettings)
        split_label.grid(row=0, column=0, sticky="new")
        split_field.grid(row=1, column=0, pady=(2,0), sticky="new")
        senstivity_label.grid(row = 0, column = 1, padx=(15, 0), sticky="new")
        senstivity_field.grid(row = 1, column = 1, padx=(15, 0), pady=(2,0), sticky="new")
        type_label.grid(row = 2, column = 0, columnspan=2, pady=(5,0), sticky="new")
        type_dropdown.grid(row = 3, column = 0, columnspan=2, pady=(2,0), sticky="new")
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        return settings_frame
    
    def AllowNumOnly(self,P,d,s):
        #If the Keyboard is trying to insert value
        if d == '1': 
            if not (P.isdigit()):
                return False
        return True
    
    def AllowPercentOnly(self,P,d,s):
        #If the Keyboard is trying to insert value
        if d == '1': 
            if not (P.isdigit() and len(s) < 3 and int(P)<=100):
                return False
        return True
    
    def SetupStatusFrame(self):
        status_frame = Frame(self)
        status_label = ttk.Label(status_frame, text = 'Status:')
        status_field = ttk.Entry(status_frame, textvariable=self.status)
        status_field.config(state=DISABLED)
        status_label.grid(row = 0,column = 0, sticky="new")
        status_field.grid(row = 1, column = 0, pady=(2,0), sticky="new")
        status_frame.columnconfigure(0, weight=1)
        return status_frame

    def SetupActionFrame(self):
        action_frame = Frame(self)
        self.progress = ttk.Progressbar(action_frame)
        self.actionbutton = ttk.Button(action_frame, text = 'Start Process', command=self.RunStitchProcess)
        self.progress.grid(row = 0, column = 0, columnspan = 2, pady=(2,0), sticky="new")
        self.actionbutton.grid(row = 0, column = 2, padx=(15, 0), sticky="new")
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)
        action_frame.columnconfigure(2, weight=1)
        return action_frame

    def LoadImages(self, folderInput):
        # Loads all image files in a given folder into a list of pillow image objects
        images = []
        if (folderInput == ""):
            return images
        folder = os.path.abspath(str(folderInput))
        files = os.listdir(folder)
        files.sort(key=lambda f: int(re.sub('\D', '', f)))
        for imgFile in files:
            if imgFile.endswith(('.png', '.webp', '.jpg', '.jpeg', '.bmp', '.tiff', '.tga')):
                imgPath = os.path.join(folder, imgFile)
                image = pil.open(imgPath)
                images.append(image)
        return images
    def Loadfolders(self):
        # Loads all image files in a given folder into a list of pillow image objects
        folders = []
        if (self.input_folder.get() == ""):
            return folders
        folder_path = os.path.abspath(str(self.input_folder.get()))
        for subdir, dirs, files in os.walk(folder_path):
            for folder in dirs:
                if not folder.endswith(('[Stitched]')):
                    path = os.path.join(folder_path, folder)
                    folders.append(path)
        return folders

    def CombineVertically(self, images):
        # All this does is combine all the files into a single image in the memory.
        widths, heights = zip(*(image.size for image in images))
        new_image_width = min(widths)
        new_image_height = sum(heights)
        new_image = pil.new('RGB', (new_image_width, new_image_height))

        combine_offset = 0
        for image in images:
            widthDifferce = 1/image.size[0]*new_image_width
            if (widthDifferce != 1):
                newNewImage = pil.new('RGB', (new_image_width, round(new_image_height+(image.size[1]*(widthDifferce-1)))))
                newNewImage.paste(new_image, (0, 0)) #x1 etc. still need to fill in
                image = image.resize((round(image.size[0]*widthDifferce), round(image.size[1]*widthDifferce)))
                new_image = newNewImage
                new_image_height = new_image.size[1]
            new_image.paste(image, (0, combine_offset))
            combine_offset += image.size[1]
        return new_image


    def SmartAdjust(self, combined_pixels, split_height, split_offset, senstivity):
        # Where the smart magic happens, compares pixels of each row, to decide if it's okay to cut there
        AdjustSensitivity = int(255 * (1-(senstivity/100)))
        adjust_in_progress = True
        new_split_height = split_height
        countdown = True
        while (adjust_in_progress):
            adjust_in_progress = False
            split_row = split_offset + new_split_height
            pixel_row = combined_pixels[split_row]
            prev_pixel = pixel_row[0]
            for x in range(1, len(pixel_row)):
                current_pixel = pixel_row[x]
                diff_pixel = int(current_pixel - prev_pixel)
                if (diff_pixel > AdjustSensitivity):
                    if (countdown):
                        new_split_height -= 1
                    else:
                        new_split_height += 1
                    adjust_in_progress = True
                    break
                current_pixel = prev_pixel
            if (new_split_height < 0.5*split_height):
                new_split_height = split_height
                countdown = False
                adjust_in_progress = True
        return new_split_height

    def SplitVertical(self, combined_img):
        # Splits the gaint combined img into small images passed on desired height.
        split_height = int(self.split_height.get())
        senstivity = int(self.senstivity.get())
        max_width = combined_img.size[0]
        max_height = combined_img.size[1]
        combined_pixels = np.array(combined_img.convert('L'))
        images = []

        # The spliting starts here (calls another function to decide where to slice)
        split_offset = 0
        while((split_offset + split_height) < max_height):
            new_split_height = self.SmartAdjust(combined_pixels, split_height, split_offset, senstivity)
            split_image = pil.new('RGB', (max_width, new_split_height))
            split_image.paste(combined_img,(0,-split_offset))
            split_offset += new_split_height
            images.append(split_image)
        # Final image (What ever is remaining in the combined img, will be smaller than the rest for sure)
        split_image = pil.new('RGB', (max_width, max_height-split_offset))
        split_image.paste(combined_img,(0,-split_offset))
        images.append(split_image)
        return images

    def SaveData(self, data, folder):
        # Saves the given images/date in the output folder!
        if (self.batch):
            new_folder = str(self.input_folder.get())
            fileprefix = re.findall(r"([\d]{1,5}(\.\d){0,1})",os.path.basename(os.path.normpath(folder)))[0][0]
            print(fileprefix);
        else:
            new_folder = str(self.output_folder.get())
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        imageIndex = 1
        outputformat = self.output_type.get()
        for image in data:
            if (self.batch):
                image.save(new_folder + '/' + fileprefix+"-"+str(f'{imageIndex:02}') + outputformat, quality=100)
            else:
                image.save(new_folder + '/'+str(f'{imageIndex:02}') + outputformat, quality=100)
            imageIndex += 1
            progress_value = 40 + (60 * imageIndex/len(data))
            self.progress['value'] = progress_value
            Tk.update_idletasks(self)
        return

    def RunStitchProcess(self):
        # Fires the process sequence from the GUI
        self.actionbutton['state'] = "disabled"
        self.actionbutton.update()
        if(self.split_height.get() == "" or self.split_height.get() =="0"):
            self.status.set("Idle - Split height value was not set!")
            self.actionbutton['state'] = "normal"
            return
        if(self.senstivity.get() == "" or self.senstivity.get() == "0"):
            self.status.set("Idle - Senstivity value was not set!")
            self.actionbutton['state'] = "normal"
            return
        self.start = time.time()
        if (self.batch):
            self.status.set("Working - Loading Folders!")
            self.progress['value'] = 0
            folders = self.Loadfolders()
            for folder in folders:
                self.StitchOne(folder)
        else:
            self.status.set("Working - Loading Image Files!")
            self.progress['value'] = 0 
            self.StitchOne(self.input_folder.get())

    def StitchOne(self, folder):
        Tk.update_idletasks(self)
        images = self.LoadImages(folder)
        if len(images) == 0:
            self.status.set("Idle - No Image Files Found!")
            self.actionbutton['state'] = "normal"
            return
        self.status.set("Working - Combining Image Files!")
        self.progress['value'] = 10
        Tk.update_idletasks(self)
        combined_image = self.CombineVertically(images)
        self.status.set("Working - Slicing Combined Image into Finalized Images!")
        self.progress['value'] = 20
        Tk.update_idletasks(self)
        final_images = self.SplitVertical(combined_image)
        self.status.set("Working - Saving Finalized Images!")
        self.progress['value'] = 40
        Tk.update_idletasks(self)
        self.SaveData(final_images, folder)
        end = time.time()
        delta = end - self.start
        self.status.set("Idle - Files successfully stitched in " +  str(f'{delta:.2}') + "sec!")
        self.progress['value'] = 100
        self.actionbutton['state'] = "normal"
    

SmartStitch().mainloop()