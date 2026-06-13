import pandas as pd
import matplotlib.pyplot as plt
from .mongodb import collection

def generate_graphs():
    data = list(collection.find())
    df = pd.DataFrame(data)

    # -------------------------------
    # 1. OCCUPANCY RATE (BAR)
    # -------------------------------
    df['Occupancy_Rate'] = (df['Occupied_Beds'] / df['Total_Beds']).round(2)

    top10 = df.sort_values('Occupancy_Rate', ascending=False)\
              .drop_duplicates(subset=['Occupancy_Rate'])\
              .head(10)

    plt.figure(figsize=(8,5))
    plt.bar(top10['Hospital_Name'], top10['Occupancy_Rate'])
    plt.xticks(rotation=45)
    plt.title("Top Hospitals by Occupancy Rate")
    plt.tight_layout()
    plt.savefig("app/static/bar.png")
    plt.close()

    # -------------------------------
    # 2. PIE CHART
    # -------------------------------
    region = df['Region_Type'].value_counts()

    plt.figure(figsize=(6,6))
    plt.pie(region.values, labels=region.index, autopct='%1.1f%%')
    plt.title("Urban vs Rural Distribution")
    plt.savefig("app/static/pie.png", bbox_inches='tight')
    plt.close()

    # -------------------------------
    # 3. LINE CHART (PATIENT INFLOW)
    # -------------------------------
    # sort for proper line visualization
    line_data = df.sort_values('Hospital_ID').head(20)

    plt.figure(figsize=(8,5))
    plt.plot(line_data['Hospital_Name'], line_data['Daily_Patient_Inflow'])
    plt.xticks(rotation=45)
    plt.title("Patient Inflow Trend Across Hospitals")
    plt.xlabel("Hospital")
    plt.ylabel("Daily Patient Inflow")
    plt.tight_layout()
    plt.savefig("app/static/scatter.png")  # same filename
    plt.close()

    # -------------------------------
    # 4. HISTOGRAM (EMERGENCY CASES)
    # -------------------------------
    plt.figure(figsize=(8,5))
    plt.hist(df['Emergency_Cases'], bins=20)
    plt.title("Distribution of Emergency Cases")
    plt.xlabel("Emergency Cases")
    plt.ylabel("Number of Hospitals")
    plt.tight_layout()
    plt.savefig("app/static/gap.png")
    plt.close()

    # -------------------------------
    # INSIGHTS
    # -------------------------------
    overcrowded = (df['Occupancy_Rate'] > 0.85).sum()
    underutilized = (df['Occupancy_Rate'] < 0.4).sum()

    urban_avg = df[df['Region_Type'] == 'Urban']['Daily_Patient_Inflow'].mean()
    rural_avg = df[df['Region_Type'] == 'Rural']['Daily_Patient_Inflow'].mean()

    insights = {
        "bar": f"{overcrowded} hospitals are overcrowded while {underutilized} are underutilized.",
        
        "pie": f"Urban hospitals handle an average of {urban_avg:.0f} patients daily, compared to {rural_avg:.0f} in rural areas.",
        
        "scatter": "This line chart shows variation of patient inflow across hospitals, highlighting differences in demand.",
        
        "gap": "This histogram shows how emergency cases are distributed, identifying hospitals with high emergency load."
    }

    return insights