from nicegui import ui
from DataHandler import EAFFileHandler as E
import numpy as np
import matplotlib.pyplot as plt

class Gui:
    def __init__(self) -> None:
        self.fhandler = E()

        self.names_only = self.fhandler.names_only
        self.typgraph = ""

        self.continents = [
            'Average Time',
            'Turn Count',
            'Precentage of Turns',
            'Average turn count',
        ]

        self.FIGURE_ON = False
        self.gui_layout_draw()

    def updategraph(self):
        if hasattr(self, 'matplotlib_element'):
            self.matplotlib_element.delete()
        if hasattr(self, 'row_element'):
            self.row_element.delete()

        # Create a new object element
        self.matplotlib_element = ui.matplotlib(figsize=(10, 5))
        self.row_element = ui.row()

        with self.matplotlib_element.figure as fig:
            print(self.valueselection.value)
            match self.valueselection.value:
                case "Average Time":
                    self.fhandler.plot_average_turn_time(fig)
                    
                case "Turn Count":
                    self.fhandler.plot_driver_head_movements(fig)
                case "Precentage of Turns":
                    self.fhandler.plot_turn_percentage(fig)
                case "Average turn count":
                    list = self.fhandler.plot_average_turn_count(fig)
                    for i in list:
                        with self.row_element:
                            text = (i," : ",list[i])
                            ui.label(text)
                case "plot radar chart":
                    self.fhandler.plot_radar_chart(fig)
                case "":
                    pass

    def updateSelection(self):
        print(self.fileselection.value)
        self.fhandler.analyze(self.fileselection.value)
    
    def gui_layout_draw(self):

        with ui.expansion('Select Data!', icon='work').classes('w-full'):
                self.fileselection = ui.select(
                self.names_only, 
                multiple=True, 
                value=self.names_only[:len(self.names_only)],
                label='with chips',
                ).classes('w-64').props('use-chips')
                
        with ui.card().classes('fixed-center'):
            ui.button("Load Data", on_click=self.updateSelection)

            self.valueselection = ui.select(
            self.continents, 
            multiple=False, 
            label='Select type of graph',
            ).classes('w-64').props('use-chips')

            ui.button("Graph", on_click=self.updategraph)

        ui.run()

            
     

gui = Gui()
