import pympi.Elan as elan
import json
import graphing
import os

class AnnotationProcessor:
    def __init__(self, eaf_path='./P62.eaf', metadata_path='null'):
        # Load EAF file and metadata file
        self.eaf_file = elan.Eaf(eaf_path)
        if metadata_path != "null":
            with open(metadata_path, 'r') as file:
                self.metadata = json.load(file)

        self.id = str(eaf_path).replace("./","").replace(".eaf","")
        self.annotations = self.get_annotations()
        self.list_intersection = self.get_intersection()
        self.list_movement = self.get_head_movement()

        #overlapping data with annotations
        self.filtered_results_headmovment = self.process_positions() 
      
        # data for graphing
      
        self.dataIntersection, self.dataHeadMovement = self.perpareData()
        self.action_count = {}
        self.count_driver_actions()
        
    def get_annotations(self):
        annotations = {}
        for tier_id in self.eaf_file.get_tier_names():
            annotations[tier_id] = self.eaf_file.get_annotation_data_for_tier(tier_id)
        return annotations

    def print_dict_keys(self, input_dict):
        if not isinstance(input_dict, dict):
            print("Provided input is not a dictionary.")
            return
        
        if not input_dict:
            print("The dictionary is empty.")
            return
        
        for key in input_dict.keys():
            print(key)

    def get_intersection(self):
        list_intersection = []
        positions = self.annotations["Position(Ego_car)"]
        for cross in positions:
            if "intersection" in str(cross):
                list_intersection.append(cross)
        return list_intersection

    def get_head_movement(self):
        return self.annotations["Head_Movement"]

    def getCountIntersection(self):
        return len(self.filtered_results)
    
    def process_positions(self):
        all_filtered_positions = {}
        for car_pos in self.list_intersection:
            filtered_positions = self.filter_car_positions(car_pos, self.list_movement)
            all_filtered_positions[str(car_pos)] = filtered_positions
        return all_filtered_positions

    def filter_car_positions(self, car_pos, head_movement):
        filtered_positions = []
        car_start_time, car_end_time = car_pos[0], car_pos[1]
        for pos in head_movement:
            h_start_time, h_end_time = pos[0], pos[1]
            head = pos[2]

            # Check if there is any overlap.
            if h_end_time < car_start_time or h_start_time > car_end_time:
                # No overlap
                continue
            
            # Adjust start and end times to ensure they are within the car position range.
            adjusted_start_time = max(h_start_time, car_start_time)
            adjusted_end_time = min(h_end_time, car_end_time)
            
            # Append the adjusted time range if it constitutes a valid interval.
            if adjusted_start_time <= adjusted_end_time:
                filtered_positions.append((adjusted_start_time, adjusted_end_time,head))

        return filtered_positions


    def get_recording_info(self):
        # Returns structured metadata about the recording
        return {
            "Recording Name": self.metadata['recording_name'],
            "Recording Software": f"{self.metadata['recording_software_name']} {self.metadata['recording_software_version']}",
            "Duration (s)": self.metadata['duration_s'],
            "Recording UUID": self.metadata['recording_uuid'],
            "System Info": self.metadata['system_info']
        }


    def perpareData(self):
        dataIntersection = []
        dataHeadMovment = []
        car_id = str(self.id)
        result_headMv = (self.filtered_results_headmovment)
        #print(result_headMv)
        list_cross = (self.list_intersection)

        for inter in list_cross:
            start_time = inter[0]
            end_time = inter[1]
            dataIntersection.append({'Car': car_id, 'Start Time (ms)': start_time, 'End Time (ms)': end_time})
            interHeadMv = (result_headMv[str(inter)])
            for i in interHeadMv:
                start_time,end_time,hd_mv = i[0], i[1],i[2]
                dataHeadMovment.append({'Driver,': car_id, 'Start Time (ms)': start_time, 'End Time (ms)': end_time, 'Head Mv' : hd_mv})
        return dataIntersection, dataHeadMovment
    

    def count_driver_actions(self):
        # Define a dictionary to store counts of each action
        action_counts = {
            'turn_left': 0,
            'turn_right': 0,
            'straight': 0,
            'slight_right': 0,
            'slight_left': 0
        }

        # Loop through each event in the list
        for event in self.dataHeadMovement:
            # Check the 'Head Mv' field and increment the corresponding count
            if event['Head Mv'] in action_counts:
                action_counts[event['Head Mv']] += 1
        self.action_count = action_counts
        return action_counts




import os

def find_all_eaf_files(folder_path):

    eaf_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".eaf"):
            eaf_files.append(os.path.join(folder_path, filename))
    return eaf_files



"""
path = "./dataset/"

paths = find_all_eaf_files(path)
list_object = []
print(paths)
for path_i in paths:

    a = AnnotationProcessor(path_i)
    list_object.append(a)
    print(a.action_count)

"""
# Usage
#processor = AnnotationProcessor()

#graphing.plot_average_turn_time([processor])
#graphing.plot_turn_percentage([processor])