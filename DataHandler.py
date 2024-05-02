import os
from Data import AnnotationProcessor as AP
import matplotlib.pyplot as plt
import graphing as G

class EAFFileHandler:
    def __init__(self, directory="./dataset/"):
        self.directory = directory
        
        self.eaf_files = self.find_eaf_files()
        self.selectedFiles = []
        self.objectLoaded: AP = []
        
        self.names_only = self.getFilenames()
    
    def find_eaf_files(self):
        eaf_files = []
        # Walk through the directory
        for root, dirs, files in os.walk(self.directory):
            # Check each file to see if it ends with .eaf
            for file in files:
                if file.endswith('.eaf'):
                    # Create a dictionary for the file
                    file_info = {
                        'path': os.path.join(root, file),
                        'name': file
                    }
                    # Append the dictionary to the list
                    eaf_files.append(file_info)
        return eaf_files
    
    def getFilenames(self):
        # Retrieve names only from the list of eaf_files
        return [file['name'] for file in self.eaf_files]

    # Will load the data paths from the name and call data library
    def load_selected_data(self, listSelectname):
        selected_files = []
        for file_info in self.eaf_files:
            if file_info['name'] in listSelectname:
                selected_files.append(file_info['path'])
        return selected_files

    def analyze(self, fileselection):
        self.objectLoaded = []
        self.selectedFiles = self.load_selected_data(fileselection)
        for selected in self.selectedFiles:
            self.objectLoaded.append(AP(selected))
        print("joe")

    # Graphing --------------------------------------------
    def plot_driver_head_movements(self,plt):
        return G.plot_driver_head_movements(self.objectLoaded,plt)
    
    def plot_average_turn_time(self,plt):
        return G.plot_average_turn_time(self.objectLoaded,plt)
    
    def plot_turn_percentage(self,plt):
        return G.plot_turn_percentage(self.objectLoaded,plt)

    def plot_average_turn_count(self,plt):
        return G.plot_average_turn_count(self.objectLoaded,plt)
    
    def plot_radar_chart(self,plt):
        return G.plot_radar_chart(self.objectLoaded,plt)