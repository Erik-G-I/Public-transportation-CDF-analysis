#%%
# Load and preprocess the data

from datetime import datetime
from matplotlib import pyplot as plt
from cdf_methods import plot_cdf, compute_deviations, map_colors_to_stops, create_colormaps
import numpy as np
import pandas as pd

# Read and clean data set

    # Notes: Read entire data set. Store each bus line separatly.  Split on date (driftsdato) also?

    # Columns in data set:
    # Rute; Rutenavn; DriftsDato; Ukedag; SekvensHoldeplassFra; HoldeplassFraNsrID; HoldeplassFraNavn; AvgangstidPlanlagt; AvgangstidFaktisk; AvgangstimeFaktisk; SekvensHoldeplassTil; HoldeplassTilNsrID; HoldeplassTilNavn; AnkomstHoldeplassTilPlanlagt; AnkomstHoldeplassTilFaktisk; TidSidenForrigeHoldeplassFaktiskSek; TidPåHoldeplassFaktiskSe; Retning; KjøretidPlanlagtSek; KjøretidFaktiskSek; Telle_Status; Time_Status; TurID;

    # Use only the columns neded for the analysis
usecols = ['Rute', 'Rutenavn', 'DriftsDato', 'Ukedag', 'SekvensHoldeplassFra', 'HoldeplassFraNavn', 'AvgangstidPlanlagt', 'AvgangstidFaktisk', 'SekvensHoldeplassTil', 'HoldeplassTilNavn', 'AnkomstHoldeplassTilPlanlagt', 'AnkomstHoldeplassTilFaktisk', 'Retning', 'TurID']

    # Optimize memory usage by specifying data types for each column
dtypes = {'Rute': str,  'Rutenavn': str,  'DriftsDato': str,  'Ukedag': str, 'SekvensHoldeplassFra': pd.Int8Dtype(), 'HoldeplassFraNavn': str,  'AvgangstidPlanlagt': str, 'AvgangstidFaktisk': str, 'SekvensHoldeplassTil': pd.Int8Dtype(), 'HoldeplassTilNavn': str, 'AnkomstHoldeplassTilPlanlagt': str, 'AnkomstHoldeplassTilFaktisk': str, 'Retning': pd.Int8Dtype(), 'TurID': pd.Int32Dtype()}
df = pd.read_csv("/Users/erikingebrigtsen/Documents/UIB/Master/20241113_48_Bergen_Sentrum_uke_2024_45.csv", sep=";", encoding="utf-8", usecols=usecols, dtype=dtypes)
df2 = pd.read_csv("/Users/erikingebrigtsen/Documents/UIB/Master/20250505_BS_202411-202505.csv", sep=";", encoding="utf-8", usecols=usecols, dtype=dtypes)
print(df2.head())

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

bus3df2 = df2[df2["Rute"] == "3"]
bus12df2 = df2[df2["Rute"] == "12"]
bus14df2 = df2[df2["Rute"] == "14"]
bus16Edf2 = df2[df2["Rute"] == "16E"]
bus19df2 = df2[df2["Rute"] == "19"]
bus20df2 = df2[df2["Rute"] == "20"]
bus22df2 = df2[df2["Rute"] == "22"]
bus23df2 = df2[df2["Rute"] == "23"]
bus23Edf2 = df2[df2["Rute"] == "23E"]
bus26df2 = df2[df2["Rute"] == "26"]
bus27df2 = df2[df2["Rute"] == "27"]
bus30df2 = df2[df2["Rute"] == "30"]
bus36df2 = df2[df2["Rute"] == "36"]
bus37df2 = df2[df2["Rute"] == "37"]
bus39df2 = df2[df2["Rute"] == "39"]
bus300df2 = df2[df2["Rute"] == "300"]
bus300Edf2 = df2[df2["Rute"] == "300E"]
bus310df2 = df2[df2["Rute"] == "310"]
bus313df2 = df2[df2["Rute"] == "313"]

## Found one line with <NA> value for direction on bus 39
bus39df2 = bus39df2.dropna(subset=["Retning"])

#%%
# Put all bus lines together in a list
# REMOVED LINE 49 - SKOLERUTER
allBusLinesOLD = [bus6, bus10, bus11, bus12, bus13, bus14, bus15, bus16E, bus18, bus20, bus24, bus40, bus41, bus42, bus43, bus44, bus45, bus46, bus48, bus81, bus82]
allBusLines =  [bus19df2, bus20df2, bus22df2, bus23df2, bus23Edf2, bus26df2, bus27df2, bus30df2, bus36df2, bus37df2, bus39df2, bus300df2, bus300Edf2, bus310df2, bus313df2]
#[bus3df2, bus12df2, bus14df2, bus16Edf2,

#%%
# Compute deviations for all stops on all bus lines
deviation_dict = compute_deviations(allBusLines)
# print(deviation_dict["12"])

# Create color maps for each line
colormaps = create_colormaps(allBusLines)

print(colormaps)

#%%
# Plot CDF for all lines in one direction (Different colors for each stop)

line_deviations = {}
for x in deviation_dict:
    line_deviations[x] = []
    for (stop, direction, sequence, deviations) in deviation_dict[x]:
        if direction == 1:
            line_deviations[x] += deviations
            colorKey = str(direction) + x
            label = f'{stop} seq {sequence}'
            plot_cdf(deviations, label=label , colormap=colormaps[colorKey])
    plt.yticks(np.arange(0, 1.1, 0.05))
    plt.xticks(np.arange(-10, 20, 2))
    plt.xlim(left=-10)
    plt.xlim(right=20)
    plt.xlabel('Deviations in minutes from planned time')
    plt.ylabel('Cumulative Probability')
    plt.title(f'Line {x} Direction 1')
    plt.grid(True)
    # plt.legend()
    y = f'0{x}' if len(x) <2 else x
    plt.savefig(f'/Users/erikingebrigtsen/Documents/UIB/Master/CDF_{y}_retning_1.png')
    plt.show()
        
    print(line_deviations)

#%%
# Plot CDF for all lines in one direction (all stops combined)

line_deviations = {}
for x in deviation_dict:
    # Sort the deviation dict by direction
    # res = sorted(deviation_dict[x], key=lambda x: x[1])
    # print(res)
    line_deviations[x] = []
    for (stop, direction, sequence, deviations) in deviation_dict[x]:
        if direction == 1:
            line_deviations[x] += deviations
    plot_cdf(line_deviations[x], label=f"Line {x}" + " retning 1")
    plt.yticks(np.arange(0, 1.1, 0.05))
    plt.xticks(np.arange(-10, 20, 2))
    plt.xlim(left = -10)
    plt.xlim(right=20)
    plt.xlabel('Deviations in minutes from planned time')
    plt.ylabel('Cumulative Probability')
    plt.title(f'Line {x} Direction 1 - Cumulative Distribution Function (CDF)')
    plt.legend()
    plt.grid(True)
    plt.show()
            
    print(line_deviations)

# %%
# For every line, plot CDF for all stops in both directions. 
# Individual plots for each stop and direction.
for x in deviation_dict:
    for (stop, direction, sequence, deviations) in deviation_dict[x]:
        colorKey = str(direction) + x
        label = f'{stop} seq {sequence}'
        plot_cdf(deviations, label=label, colormap=colormaps[colorKey])
        plt.yticks(np.arange(0, 1.1, 0.05))
        plt.xticks(np.arange(-10, 20, 2))
        plt.xlim(right=20)
        plt.xlabel('Deviations in minutes from planned time')
        plt.ylabel('Cumulative Probability')
        plt.title(f'Line{x} - {stop} seq {sequence}, direction{direction}')
        plt.legend()
        plt.grid(True)
        y = "06" if x == "6" else x
        z = "0" + str(sequence) if sequence < 10 else sequence
        plt.savefig(f"/Users/erikingebrigtsen/Documents/UIB/Master/CDFplots/Line12/Individual_stops_v3/CDF_{y}_dir{direction}_seq{z}_{stop}.png")
        plt.show()

# %%
for (stop, direction, sequence, deviations) in deviation_dict["16E"]:
    colorKey = str(direction)+"16E"
    label = f'{stop} seq {sequence}'
    plot_cdf(deviations, label=label, colormap=colormaps[colorKey])
    plt.yticks(np.arange(0, 1.1, 0.05))
    plt.xticks(np.arange(-10, 20, 2))
    plt.xlim(right=20)
    plt.xlabel('Deviations in minutes from planned time')
    plt.ylabel('Cumulative Probability')
    plt.title(f'Line 16E - {stop} seq {sequence}, direction {direction}')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'CDF_16E_seq{sequence}_dir{direction}_{stop}.png')
    plt.show()
# %%
