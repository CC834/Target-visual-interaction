#import matplotlib.pyplot as plt
import numpy as np


def plot_radar_chart(data_objects,plt):
    
    # Initialize dictionary to store aggregated turn counts
    turn_counts = {}
    
    # Process each object to count turns
    for obj in data_objects:
        for record in obj.dataHeadMovement:
            turn = record['Head Mv']
            if turn in turn_counts:
                turn_counts[turn].append(1)  # Increment turn count for this type
            else:
                turn_counts[turn] = [1]  # Initialize list with first count
    
    # Calculate the average count for each turn type
    average_counts = {turn: sum(counts) / len(data_objects) for turn, counts in turn_counts.items()}
    labels = list(average_counts.keys())
    stats = list(average_counts.values())
    
    # Number of variables we're plotting.
    num_vars = len(labels)
    
    # Compute angle each bar is centered on:
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # The plot is made in a circular (not polygon) manner:
    stats += stats[:1]
    angles += angles[:1]
    
    #fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax = plt.gca()
    ax.fill(angles, stats, color='red', alpha=0.25)
    ax.plot(angles, stats, color='red', linewidth=2)  # Draw the outline of our data
    ax.set_yticklabels([])
    
    # Labels for each point
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    
    plt.plot()

def plot_average_turn_count(data_objects,plt):
    
    # Initialize dictionary to store aggregated turn counts
    turn_counts = {}
    
    # Process each object to count turns
    for obj in data_objects:
        for record in obj.dataHeadMovement:
            turn = record['Head Mv']
            if turn in turn_counts:
                turn_counts[turn].append(1)  # Increment turn count for this type
            else:
                turn_counts[turn] = [1]  # Initialize list with first count

    turn_max_min = {}
    for turn in turn_counts:
        turn_max_min[turn] = len(turn_counts[turn])

    # Calculate the average count for each turn type
    average_counts = {turn: sum(counts) / len(data_objects) for turn, counts in turn_counts.items()}
    turns = list(average_counts.keys())
    counts = [average_counts[turn] for turn in turns]
    
    # Plotting
    ax = plt.gca()
    ax.bar(turns, counts, color='green')
    
    ax.set_xlabel('Type of Turn')
    ax.set_ylabel('Average Turn Count per Object')
    ax.set_title('Average Turn Count for Each Type of Turn')
    
    #plt.plot()
    return turn_max_min


def plot_driver_head_movements(data_objects,plt):
    
    # Initialize dictionary to store aggregated turn data
    turn_data = {}
    
    # Process each object and aggregate data
    for obj in data_objects:
        obj_id = obj.id  # Retrieve the id of the object
        actions = obj.action_count  # Retrieve the turning data
        
        # Initialize or update counts for each turn type for this object
        for turn, count in actions.items():
            if turn not in turn_data:
                turn_data[turn] = {}
            turn_data[turn][obj_id] = count
    
    # Create lists for plotting
    turns = list(turn_data.keys())
    object_ids = [obj.id for obj in data_objects]
    indexes = range(len(turns))
    bar_width = 0.1
    
    # Setup plot
    ax = plt.gca()
    for idx, obj in enumerate(data_objects):
        # Generate positions offset by the bar width * index of the object
        positions = [i + idx * bar_width for i in indexes]
        counts = [turn_data[turn].get(obj.id, 0) for turn in turns]
        ax.bar(positions, counts, bar_width, label=f'ID {obj.id}')

    # Adjust x-ticks and x-tick labels
    ax.set_xlabel('Types of Turns')
    ax.set_ylabel('Amount of Turns')
    ax.set_title('Turns by Object ID')
    ax.set_xticks([i + (len(data_objects) * bar_width) / 2 - bar_width / 2 for i in indexes])
    ax.set_xticklabels(turns)
    ax.legend(title="Object ID", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    ax.plot()


def plot_average_turn_time(data_objects,plt):
    
    # Initialize dictionary to store aggregated turn times
    turn_times = {}
    
    # Process each object to calculate average turn times
    for obj in data_objects:
        for record in obj.dataHeadMovement:
            turn = record['Head Mv']
            start_time = record['Start Time (ms)']
            end_time = record['End Time (ms)']
            duration = end_time - start_time
            
            if turn in turn_times:
                turn_times[turn].append(duration)
            else:
                turn_times[turn] = [duration]
    
    # Calculate the average time for each turn
    average_times = {turn: sum(times) / len(times) for turn, times in turn_times.items()}
    turns = list(average_times.keys())
    times = [average_times[turn] for turn in turns]
    
    # Plotting
    ax = plt.gca()
    ax.bar(turns, times, color='blue')
    
    ax.set_xlabel('Type of Turn')
    ax.set_ylabel('Average Time (ms)')
    ax.set_title('Average Time for Each Type of Turn')
    
    ax.plot()


def plot_turn_percentage(data_objects,plt):

    # Initialize dictionary to count turns by type
    turn_counts = {}
    total_turns = 0
    
    # Process each object to count turns
    for obj in data_objects:
        for record in obj.dataHeadMovement:
            turn = record['Head Mv']
            if turn in turn_counts:
                turn_counts[turn] += 1
            else:
                turn_counts[turn] = 1
            total_turns += 1
    
    # Calculate the percentage for each turn
    turn_percentages = {turn: (count / total_turns) * 100 for turn, count in turn_counts.items()}
    labels = list(turn_percentages.keys())
    sizes = list(turn_percentages.values())
    
    # Plotting
    ax = plt.gca()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    ax.plot()
