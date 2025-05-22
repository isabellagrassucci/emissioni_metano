# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:00:26 2024

@author: chiar
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
       
from scipy.signal import find_peaks


mandria_path = 'C:/Users/chiar/Dropbox/Prove_MOOLOGGER/g_day/dati_troscia_gen_feb/ch4_cleaned_bg20.csv'
mandria = pd.read_csv(mandria_path)
matrix=[]
peaks=[]

mungiture = list(set(mandria['Milking_number']))
#print(len(animals))
#print(len(mungiture))

for mungitura in mungiture:  

    milking_ch4 = mandria[mandria['Milking_number'] == mungitura]
    milking_ch4 = milking_ch4.reset_index(drop=True)
    
    ch4=milking_ch4['CH4']
    
    cow = milking_ch4.iloc[0,0]
    
    #Wait 20 sec before the detection of the next peak
    time_interval=35
    
    # Find peaks
    peaks, properties = find_peaks(ch4, height=600,distance=time_interval)
    
    # Count the number of peaks
    num_peaks = len(peaks)
    
    
    # Save the count to a new column in the DataFrame
    milking_ch4['num_peaks'] = num_peaks
    '''
    # Plot the data
    plt.plot(ch4, label='Data')

    # Plot the detected peaks
    plt.plot(peaks, ch4[peaks], "x", label='Detected Peaks')

    # Optionally, mark the heights of the peaks
    plt.vlines(x=peaks, ymin=min(ch4), ymax=ch4[peaks], colors="y", linestyles="dashed")

    # Add labels and title
    plt.title("Detected Peaks per milking" + "-" + str(cow))
    plt.xlabel("time")
    plt.ylabel("ppm")
    plt.legend()
    
    directory = "C:/Users/chiar/Dropbox/Prove_MOOLOGGER/g_day/dati_troscia_gen_feb/plot_peaks_35sec_600height/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = directory + str(mungitura) + ".png"
    
    plt.savefig(file_path, format="png", dpi=250)
    
    plt.show()
    
   '''
            
    matrix.append(milking_ch4)
      
# Concatenate all DataFrames in the list into a single DataFrame
combined_df = pd.concat(matrix, ignore_index=True)

mean_ch4_1= combined_df['CH4'].mean()

filter_peaks=combined_df[combined_df['num_peaks']>= 2]

mean_ch4_2= filter_peaks['CH4'].mean()


filter_peaks.drop(columns=['Entry_time',
                      'Milking_duration','Exit_time'], inplace=True)

# Salva il DataFrame combinato in un nuovo file CSV.
output_file = 'C:/Users/chiar/Dropbox/Prove_MOOLOGGER/g_day/dati_troscia_gen_feb/ch4_peaks_filtered_bg20.csv'
filter_peaks.to_csv(output_file, index=False)

  
   