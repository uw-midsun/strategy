import pandas as pd

df = pd.read_csv("Bom_.csv") #CSV file must be named BOM_.csv for function to perform. 

partNumber = input("Enter Manufacturer Part Number: ")

def parseFunction(partNumber):
    for index, row in df.iterrows(): # parses through each manufacturer value to scan for matching input value.
        if partNumber== row["Manufacturer Part Number"]:
            print ("The extended price is: " + row["Extended Price"] + "\n" + "The Mfg Std Lead Time is: " + row["Mfg Std Lead Time"])
        else:
            print("Manufacturer part number not found.")
            return
parseFunction(partNumber)