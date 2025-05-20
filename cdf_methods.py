from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Function to calculate deviation of arrival time of buses at a given stop
def specificTimeDeviation(stopName, line, time, direction):
    cond1 = line["HoldeplassFraNavn"] == stopName
    cond2 = line["Retning"] == direction
    cond3 = line["AvgangstidPlanlagt"].str.contains(time)
    combinedCond = cond1 & cond2 & cond3
    appliedConstraint = line[combinedCond]
    deviations = []
    for row in appliedConstraint.iterrows():
        planned = row[1]["AvgangstidPlanlagt"]
        actual = row[1]["AvgangstidFaktisk"]
        try:
            deviation = (datetime.strptime(actual, "%Y-%m-%d %H:%M:%S") - datetime.strptime(planned, "%Y-%m-%d %H:%M:%S")).total_seconds() /60
        except:
            continue
        deviations.append(float(deviation))
    print(deviations)
    return deviations


# Function to compute and plot the CDF with polynomial regression
# data is a list of deviations
# label is a string describing the plot (e.g. stop name and line number)
def plot_cdf(data, label, colormap):
    # Sort the data
    sorted_data = np.sort(data)
    
    # Calculate the cumulative probabilities
    prob = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    
    # Color map for the stops
    # gets the color for the stop or black if the stop is not in the colormap
    color = colormap.get(label, "black")

    # Plot the CDF in steps using post modifier
    # sorted_data is the x-axis and prob is the y-axis
    plt.plot(sorted_data, prob, label=label, color=color, drawstyle='steps-post')


# Function to compute deviations for all stops on a line
# lines is a list of dataframes, each dataframe contains the data for a bus line
def compute_deviations(lines):

    deviation_dict = {} # Dictionary to store each line with a list of all stops and their deviations

    # For each line, create a set of the stops and their direction and sequence
    for line in lines:
        stops_dir = set()
        deviation_dict[line.iloc[0, 0]] = []
        for row in line.iterrows():
            stops_dir.add((row[1]["HoldeplassFraNavn"], row[1]["Retning"], row[1]["SekvensHoldeplassFra"]))
        
        for (stop, direction, sequence) in stops_dir:
            deviations = []
            cond1 = line["HoldeplassFraNavn"] == stop
            cond2 = line["Retning"] == direction
            cond3 = line["SekvensHoldeplassFra"] == sequence # This ensures that irregular routes stays separate from the regular routes. ex. 16E from Birkelundstoppen
            combinedCond = cond1 & cond2 & cond3
            appliedConstraint = line[combinedCond]
            for row in appliedConstraint.iterrows():
                plan = row[1]["AvgangstidPlanlagt"]
                faktisk = row[1]["AvgangstidFaktisk"]
                try:
                    avvik = (datetime.strptime(faktisk, "%Y-%m-%d %H:%M:%S") - datetime.strptime(plan, "%Y-%m-%d %H:%M:%S")).total_seconds() /60
                except:
                    continue
                deviations.append(float(avvik))
        
            deviation_dict[line.iloc[0, 0]].append((stop, direction, sequence, deviations))
        
    print(deviation_dict)
    return deviation_dict


def map_colors_to_stops(line, dir):
    # Create a dictionary to map each stop to a color
    stops_dir = set()
    line= line[line["Retning"] == dir]
    if line.shape[0] == 0: return {}

    for row in line.iterrows():
        stops_dir.add((row[1]["HoldeplassFraNavn"], row[1]["Retning"], row[1]["SekvensHoldeplassFra"]))
        
    
    #line = line.drop_duplicates(subset="HoldeplassFraNavn").reset_index(drop=True)
    #num_colors = max(line.shape[0], line.iloc[-1]["SekvensHoldeplassFra"])
    num_colors = len(stops_dir)
    colors = [plt.cm.rainbow(i / num_colors) for i in range(num_colors)][::-1]
    stop_color = {}
    # Maps colors for both directions. Red is first stop -> violet is last stop
    # for stop, dir, seq in stops_dir:
    #     key = f'{row["HoldeplassFraNavn"]} seq {row["SekvensHoldeplassFra"]}'
    #     val = colors[row["SekvensHoldeplassFra"]-1]
    #     stop_color[key] = val
    for stop, dir, seq in stops_dir:
        key = f'{stop} seq {seq}'
        val = colors[seq-1]
        stop_color[key] = val
    
    return stop_color

# Takes in the deviation dic
def create_colormaps(allLines):
    color_maps = {}
    for line in allLines:
        dir1 = f'1{line.iloc[0, 0]}'
        dir2 = f'2{line.iloc[0, 0]}'
        color_maps[dir1] = map_colors_to_stops(line, dir=1)
        color_maps[dir2] = map_colors_to_stops(line, dir=2)

    return color_maps

