# Requirements: 
# - Files must be in CSV formats. 
# - Two CSV's must be entered into the function, with the first csv containing a "Digi-Key Part Number" column value and a "Mfg Std Lead Time" value. The second CSV should contain a "Mouser Part Number" column value and a "Lead Time in Weeks" value. 
# - The third parameter is either the Digi-Key Part Number or the Mouser Part Number. The part number is to be entered as a string, as with the other CSV names. 


import pandas as pd

def parseCSV(csv1, csv2, partNumber):

    df1 = pd.read_csv(csv1)
    df2 = pd.read_csv(csv2)

    try:
        value = df1.loc[df1['Digi-Key Part Number'] == partNumber, "Mfg Std Lead Time"].values[0]
        print(f"The lead time in weeks is: {value}.")
    except:
        print(f"Did not find part number in {csv1}.")

    try:
        value2 = df2.loc[df2['Mouser Part Number'] == partNumber, "Lead Time in Weeks"].values[0]
        print(f"The lead time in weeks is: {value2}.")
    except:
        print(f"Did not find part number in {csv2}.")

# Testing - Assuming names for the CSV files and selecting random part number from BomSample_.csv 
parseCSV('BomSample_.csv','MidnightSun-Jan28-QuoteRequest.csv','490-4789-1-ND')
