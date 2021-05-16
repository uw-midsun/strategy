import pandas as pd

def main():
    parseCSV()

if __name__=='__main__':
    main()

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

