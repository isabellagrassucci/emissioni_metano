# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 18:56:21 2024

@author: chiar
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

#Lettura file dati mergiati ch4-bufale e robot, selezionando solo colonne che ci servono per questo momento.

mandria_path = 'C:/Users/chiar/Dropbox/Prove_MOOLOGGER/Troscia_frisone/Dati_gen_feb_2024/plot_mung_v3_no_neg/ch4_cutted_v3.csv'
mandria = pd.read_csv(mandria_path)

mandria['ID_cow'] = mandria['ID_Cow'].apply(lambda x: int(x))
mandria['Milking_number'] = mandria['Milking_number'].apply(lambda x: int(x))

animals = list(set(mandria['ID_Cow']))
mungiture = list(set(mandria['Milking_number']))


mandria.drop(columns=['timestamp','CH4_det','Entry_time',
                      'Milking_duration','Exit_time','ID_cow',
                      'milking_duration_seconds','progressive_seconds'], inplace=True)


# Group by 'Milking_number' and calculate the mean of 'Methane'
average_methane_per_milking = mandria.groupby('Milking_number').mean().reset_index()

#METANO MEDIO EMESSO PER MUNGITURA
mean_ch4_per_milking = average_methane_per_milking['CH4'].mean()

# Group by 'Animal_ID' and count the unique 'Milking_number'
milking_count_per_animal = mandria.groupby('ID_Cow')['Milking_number'].nunique().reset_index()

# Step 2: Group by 'Animal_ID' to calculate the average and standard deviation of the means
mean_and_std = average_methane_per_milking.groupby('ID_Cow').agg({
    'CH4': ['mean', 'std'],
    'Milk_Yield': 'mean'}).reset_index()

# Flatten the MultiIndex columns resulting from the aggregation
mean_and_std.columns = ['ID_Cow', 'CH4_mean', 'CH4_std', 'avg_milk_yield']


# Salva il DataFrame combinato in un nuovo file CSV.
output_file = 'C:/Users/chiar/Dropbox/Prove_MOOLOGGER/Troscia_frisone/Dati_gen_feb_2024/plot_mung_v3_no_neg/mean_ch4_per_animal.xlsx'
mean_and_std.to_excel(output_file, index=False)


output_file_2 = 'C:/Users/chiar/Dropbox/Prove_MOOLOGGER/Troscia_frisone/Dati_gen_feb_2024/plot_mung_v3_no_neg/mean_ch4_per_milking.xlsx'
average_methane_per_milking.to_excel(output_file_2, index=False)
print("File CSV combinato creato con successo.")



