#%%
# Imports and setup
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Read and clean data set

    # Notes: Read entire data set. Store each bus line separatly.  Split on date (driftsdato) also?

    # Columns in data set:
    # Rute; Rutenavn; DriftsDato; Ukedag; SekvensHoldeplassFra; HoldeplassFraNsrID; HoldeplassFraNavn; AvgangstidPlanlagt; AvgangstidFaktisk; AvgangstimeFaktisk; SekvensHoldeplassTil; HoldeplassTilNsrID; HoldeplassTilNavn; AnkomstHoldeplassTilPlanlagt; AnkomstHoldeplassTilFaktisk; TidSidenForrigeHoldeplassFaktiskSek; TidPåHoldeplassFaktiskSe; Retning; KjøretidPlanlagtSek; KjøretidFaktiskSek; Telle_Status; Time_Status; TurID;
df = pd.read_csv("/Users/erikingebrigtsen/Documents/UIB/Master/Skyss_OneDrive_1_19.11.2024/20241113_48_Bergen_Sentrum_uke_2024_45.csv", sep="\t", encoding="iso-8859-1", dtype={'Rute': str,  'Rutenavn': str,  'DriftsDato': str,  'Ukedag': str, 'SekvensHoldeplassFra': int, 'HoldeplassFraNsrID': str,  'HoldeplassFraNavn': str,  'AvgangstidPlanlagt': str, 'AvgangstidFaktisk': str, 'AvgangstimeFaktisk': pd.Int32Dtype(), 'SekvensHoldeplassTil': int, 'HoldeplassTilNsrID': str, 'HoldeplassTilNavn': str, 'AnkomstHoldeplassTilPlanlagt': str, 'AnkomstHoldeplassTilFaktisk': str, 'TidSidenForrigeHoldeplassFaktiskSek': int, 'TidPåHoldeplassFaktiskSek': int, 'Retning': int, 'KjøretidPlanlagtSek': int, 'KjøretidFaktiskSek': int, 'Telle_Status': int, 'Time_Status':  pd.Int32Dtype(), 'TurID': int})
print(df)

#%%

# Create subsets of data set. split on bus lines
bus6 = df[df["Rute"] == "6"]        # 6 Birkelundstoppen-Lyngbø
bus10 = df[df["Rute"] == "10"]      # 10 Wergeland/Søndre Skogveien - Mulen
bus11 = df[df["Rute"] == "11"]      # 11 Nordnes - Starefossen
bus12 = df[df["Rute"] == "12"]      # 12 Lønnborglien - Montana
bus13 = df[df["Rute"] == "13"]      # 13 Bergen sentrum - Solheimsviken
bus14 = df[df["Rute"] == "14"]      # 14 Bergen busstasjon - Bønes o/Fjøsanger
bus15 = df[df["Rute"] == "15"]      # 15 Bergen sentrum - Bønes
bus16E = df[df["Rute"] == "16E"]    # 16E Nesttun - Helldalsåsen - Øyjorden
bus18 = df[df["Rute"] == "18"]      # 18 Barlieveien - Formanns vei
bus20 = df[df["Rute"] == "20"]      # 20 Storavatnet - Haukeland sjukehus
bus24 = df[df["Rute"] == "24"]      # 24 Olsvikskjenet - Loddefjord terminal - Oasen
bus40 = df[df["Rute"] == "40"]      # 40 Storavatnet terminal - Olsvik - Bergen busstasjon
bus41 = df[df["Rute"] == "41"]      # 41 Hetlevikåsen - Loddefjord terminal
bus42 = df[df["Rute"] == "42"]      # 42 Alvøen - Loddefjord terminal
bus43 = df[df["Rute"] == "43"]      # 43 Tyssøy/Bjorøy - Loddefjord terminal
bus44 = df[df["Rute"] == "44"]      # 44 Gravdal - Nipedalen
bus45 = df[df["Rute"] == "45"]      # 45 Loddefjord - Skålevik - Brøstaneset - Loddefjord
bus46 = df[df["Rute"] == "46"]      # 46 Løvstakkskiftet - Oasen
bus48 = df[df["Rute"] == "48"]      # 48 Oasen - Løtveit
bus49 = df[df["Rute"] == "49"]      # 49 Skoleturer Bergen Sentrum
bus81 = df[df["Rute"] == "81"]      # 81 Nattlandsfjellet - Mannsverk
bus82 = df[df["Rute"] == "82"]      # 82 Grønnestølen - Wergeland

#%%
# Function to calculate deviation of arrival time of buses at a given stop
def calculateDeviations(stopName, line, time, to_from, arrive_depart, direction):
    # Calculate the deviations of the buses arriving at the given stop.
    # stopName: Name of the stop
    # line: Line number
    # time: planned time of arrival or departure
    # to_from: "HoldeplassTilNavn" if the bus is arriving at the stop, "HoldeplassFraNavn" if the bus is departing from the stop.
    # arrive_depart: "AnkomstHoldeplassTilPlanlagt" if the bus is arriving at the stop, "AvgangstidPlanlagt" if the bus is departing from the stop.
    # direction: 1 if the bus is going in the direction following its route name, 2 if the bus going in the opposite direction.
    # Returns a list of deviations of the buses arriving at the given stop.
    cond1 = line[to_from] == stopName
    cond2 = line["Retning"] == direction
    cond3 = line[arrive_depart].str.contains(time)
    combinedCond = cond1 & cond2 & cond3
    appliedConstraint = line[combinedCond]
    deviations = []
    for row in appliedConstraint.iterrows():
        plan = row[1][arrive_depart]
        arrive_depart_rt = arrive_depart.replace("Planlagt", "Faktisk")
        faktisk = row[1][arrive_depart_rt]
        try:
            avvik = (datetime.strptime(faktisk, "%d.%m.%Y %H:%M") - datetime.strptime(plan, "%d.%m.%Y %H:%M")).total_seconds() /60
        except:
            continue
        #print("Planlagt:",plan,"Faktisk:", faktisk,"Avvik:", avvik)
        deviations.append(float(avvik))
    print(deviations)
    return deviations

#%%
# Function to compute and plot the CDF with polynomial regression
def plot_cdf(data, label):
    # Sort the data
    sorted_data = np.sort(data)
    
    # Calculate the cumulative probabilities
    y = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
     
    # Plot the CDF
    plt.step(sorted_data, y, where='post', label=f'{label} CDF')

#%%
# Plot CDF with polynomial regression for each list
florida_nattlandsfjellet = [
    [("Florida", bus12, "16:18|16:28|16:38", "HoldeplassFraNavn", "AvgangstidPlanlagt", 1), ("Haukeland sjukehus nord", bus12, "16:24|16:34|16:44", "HoldeplassTilNavn", "AnkomstHoldeplassTilPlanlagt", 1), ("Haukeland sjukehus nord", bus16E, "16:33|16:41|16:51", "HoldeplassFraNavn", "AvgangstidPlanlagt", 2), ("Mannsverk", bus16E, "16:39|16:47|16:57", "HoldeplassTilNavn", "AnkomstHoldeplassTilPlanlagt", 2), ("Mannsverk", bus81, "16:29|16:49|17:09", "HoldeplassFraNavn", "AvgangstidPlanlagt", 1), ("Nattlandsfjellet", bus81, "16:35|16:55|17:15", "HoldeplassTilNavn", "AnkomstHoldeplassTilPlanlagt", 1)], 
    [("Florida", bus12, "16:38|16:48|17:08", "HoldeplassFraNavn", "AvgangstidPlanlagt", 1), ("Haukeland sjukehus nord", bus12, "16:44|16:54|17:14", "HoldeplassTilNavn", "AnkomstHoldeplassTilPlanlagt", 1), ("Haukeland sjukehus nord", bus6, "16:49|16:59|17:09", "HoldeplassFraNavn", "AvgangstidPlanlagt", 2), ("Mannsverk", bus6, "17:00|17:06|17:16", "HoldeplassTilNavn", "AnkomstHoldeplassTilPlanlagt", 2), ("Mannsverk", bus81, "16:49|17:09|17:29", "HoldeplassFraNavn", "AvgangstidPlanlagt", 1), ("Nattlandsfjellet", bus81, "16:55|17:15|17:35", "HoldeplassTilNavn", "AnkomstHoldeplassTilPlanlagt", 1)], 
    [("Florida", bus12, "16:28|16:38|16:48", "HoldeplassFraNavn", "AvgangstidPlanlagt", 1), ("Mannsverk garasje", bus12, "16:53|17:03|17:13", "HoldeplassTilNavn", "AnkomstHoldeplassTilPlanlagt", 1), ("Mannsverk", bus81, "16:49|17:09|17:29", "HoldeplassFraNavn", "AvgangstidPlanlagt", 1), ("Nattlandsfjellet", bus81, "16:55|17:15|17:35", "HoldeplassTilNavn", "AnkomstHoldeplassTilPlanlagt", 1)]
    ]

for route in florida_nattlandsfjellet:
    for stop in route:
        dev = calculateDeviations(stop[0], stop[1], stop[2], stop[3], stop[4], stop[5])

        
        plot_cdf(dev, label=(stop[0] + stop[1].iloc[0, 0]))

        # Add labels and legend
        plt.xlabel('Deviations in minutes from planned time')
        plt.ylabel('Cumulative Probability')
        plt.title('Cumulative Distribution Function (CDF)')
        plt.legend()
        plt.grid(True)
        plt.show()


#%%
# Function to compute deviations for all stops on a line

# for x in line
    # add stop name, direction to set
    # for y in set    
        # get time, direction from stopname in df
        # get all rows = stop name and direction
        # calculate deviation

allBusLines = [bus6, bus10, bus11, bus12, bus13, bus14, bus15, bus16E, bus18, bus20, bus24, bus40, bus41, bus42, bus43, bus44, bus45, bus46, bus48, bus49, bus81, bus82]

def compute_deviations(lines):

    deviation_dict = {}

    for line in lines:
        stops_dir = set()
        deviation_dict[line.iloc[0, 0]] = []
        for row in line.iterrows():
            stops_dir.add((row[1]["HoldeplassFraNavn"], row[1]["Retning"]))
        
        for (stop, direction) in stops_dir:
            deviations = []
            cond1 = line["HoldeplassFraNavn"] == stop
            cond2 = line["Retning"] == direction
            combinedCond = cond1 & cond2
            appliedConstraint = line[combinedCond]
            for row in appliedConstraint.iterrows():
                plan = row[1]["AvgangstidPlanlagt"]
                faktisk = row[1]["AvgangstidFaktisk"]
                try:
                    avvik = (datetime.strptime(faktisk, "%d.%m.%Y %H:%M") - datetime.strptime(plan, "%d.%m.%Y %H:%M")).total_seconds() /60
                except:
                    continue
                deviations.append(float(avvik))
        
            deviation_dict[line.iloc[0, 0]].append((stop, direction, deviations))
        
    print(deviation_dict)
    return deviation_dict

deviation_dict = compute_deviations(allBusLines)

#%%
# Function to compute and plot CDFs for whole line

line_deviations = {}
for x in deviation_dict:
    # Sort the deviation dict by direction
    # res = sorted(deviation_dict[x], key=lambda x: x[1])
    # print(res)
    line_deviations[x] = []
    for (stop, direction, deviations) in deviation_dict[x]:
        if direction == 1:
            line_deviations[x] += deviations
            plot_cdf(deviations, label=str(stop) + " retning " + str(direction))
    plt.yticks(np.arange(0, 1.1, 0.05))
    plt.xticks(np.arange(-10, 20, 2))
    plt.xlim(right=20)
    plt.xlabel('Deviations in minutes from planned time')
    plt.ylabel('Cumulative Probability')
    plt.title(f'Line {x} Direction 1 - Cumulative Distribution Function (CDF)')
    # plt.legend()
    plt.grid(True)
    plt.show()
            
    print(line_deviations)
    

# for (line, dev) in line_deviations.items():
#     plot_cdf(dev, label=line)
#     plt.yticks(np.arange(0, 1.1, 0.05))
#     plt.xticks(np.arange(-10, 20, 2))
#     plt.xlim(right=20)
#     plt.xlabel('Deviations in minutes from planned time')
#     plt.ylabel('Cumulative Probability')
#     plt.title('Cumulative Distribution Function (CDF)')
#     plt.legend()
#     plt.grid(True)
#     plt.show()



# %%
for (stop, direction, deviations) in deviation_dict["6"]:
    if direction == 1:
        plot_cdf(deviations, label=f'6 - {stop} retning {direction}')
plt.yticks(np.arange(0, 1.1, 0.05))
plt.xticks(np.arange(-10, 20, 2))
plt.xlim(right=20)
plt.xlabel('Deviations in minutes from planned time')
plt.ylabel('Cumulative Probability')
plt.title('Cumulative Distribution Function (CDF)')
plt.legend()
plt.grid(True)
plt.show()
# %%
for (stop, direction, deviations) in deviation_dict["10"]:
    plot_cdf(deviations, label=f'10 - {stop} retning {direction}')
    plt.yticks(np.arange(0, 1.1, 0.05))
    plt.xticks(np.arange(-10, 20, 2))
    plt.xlim(right=20)
    plt.xlabel('Deviations in minutes from planned time')
    plt.ylabel('Cumulative Probability')
    plt.title('Cumulative Distribution Function (CDF)')
    plt.legend()
    plt.grid(True)
    plt.show()
    plt.savefig(f'CDF_10_{stop}_retning_{direction}.png')
# %%

 