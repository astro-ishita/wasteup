import pandas as pd
import numpy as np
import random  
from datetime import datetime, timedelta

#settings 
factory_name = "Factory A"
num_days = 30
machines = ["Injection Moulder 1", 
            "Injection Moulder 2", 
            "Blow Moulder",
            "Extrusion Line",
            "Thermoformer"]

waste_types = ['Sprue/Runner', 'Purge material', 'Off-spec parts',
               'Edge trim', 'Colour change waste']
shifts = ['Morning (06:00-14:00)',
          'Afternoon (14:00-22:00)',
          'Night (22:00-06:00)']

# Generate data
np.random.seed(42)  # Makes results repeatable
rows = []
start_date = datetime(2025, 1, 1)

for day in range(num_days):
    date = start_date + timedelta(days=day)
    for shift in shifts:
        for machine in machines:
            # Normal waste: between 1 and 8 kg per shift
            waste_kg = round(np.random.uniform(1.0, 8.0), 2)
            waste_type = random.choice(waste_types)

            #randomly create an anomaly with a 10% chance
            anomaly = np.random.rand() < 0.1
            if anomaly:
                waste_kg *= np.random.uniform(1.5, 3.0)  # Increase waste by 50-200%
                waste_type = "Anomalous Waste"

            rows.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Shift": shift,
                "Machine": machine,
                "Waste Type": waste_type,
                "Waste (kg)": waste_kg,
                "anomaly": anomaly,
                "factory": factory_name
            })

#save to csv
df = pd.DataFrame(rows)
df.to_csv("factory_waste_data.csv", index=False)
print(f"Generates {len(df)} rows of waste data.")
print(f"Total waste simulated: {df['Waste (kg)'].sum():.1f} kg")
print(f"Anomalies detected: {df['anomaly'].sum()}")
print("File saved as 'factory_waste_data.csv'")