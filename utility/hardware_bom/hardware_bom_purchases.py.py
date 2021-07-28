# Requirements: 
# 1. Entering data spreadsheets to the function in order as referenced.
# 2. Updating priority field on both spreadsheets, ensuring value is equal on both. 

import pandas as pd

# parseCSV will accept the BOM.csv and MS_Quote Excel File and return two seperate Excel/CSV files with winning parts. 
def parse_hardware_bom_(Bom_file, MS_Quote_file): 

    Bom_DF = pd.read_csv(Bom_file)
    MS_Quote_DF = pd.read_excel(MS_Quote_file)
    
    #  Create DF of relevant information.
    Bom_DF = Bom_DF[['Manufacturer Part Number', 'Description', 'Unit Price','Mfg Std Lead Time']]
    MS_Quote_DF = MS_Quote_DF[['Mfr. #', 'Description', 'Order Unit Price','Lead Time in Weeks', 'Priority']] 
    Bom_DF = Bom_DF.rename(columns = {'Manufacturer Part Number':'Mfr. #'}) 

    # Fill Nan values with zeroes for calculation purposes.
    Bom_DF['Mfg Std Lead Time'] = Bom_DF['Mfg Std Lead Time'].fillna(0) 
    MS_Quote_DF['Lead Time in Weeks'] = MS_Quote_DF['Lead Time in Weeks'].fillna(0)

    # Correct issue of having "$" in front of numeric price value.
    MS_Quote_DF["Order Unit Price"] = MS_Quote_DF["Order Unit Price"].replace('[\$]',"",regex=True).astype(float)
    
    # Correct issue where lead times is an integer followed by "Weeks"
    new_values =[]
    for row in (Bom_DF['Mfg Std Lead Time']):
        if type(row) == str:
            new_value = row.replace('Weeks','')
            new_values.append(int(new_value))
        else:
            new_values.append(int(row))
    Bom_DF['Mfg Std Lead Time'] = new_values
    
    # Merges the two files on common column 'Mfr. #'
    result = pd.merge(left=Bom_DF,right=MS_Quote_DF, on='Mfr. #')

    Bom_Winners = [] # list of indices where Bom parts win
    MS_Quote_Winners = [] # list of indices where MS_Quote parts win

    # Creating lists to iterate through each item and compare values for each index
    Bom_prices = result['Unit Price'].fillna(0).tolist()
    MS_prices = result['Order Unit Price'].fillna(0).tolist()
    Bom_lead = result['Mfg Std Lead Time'].tolist()
    MS_lead = result['Lead Time in Weeks'].tolist()
    priority = result['Priority'].tolist()
    
    for i in range(len(result)):
        if priority[i] == 'y': # if part is a priority, lead time comparison is forefront
            if Bom_lead[i] > MS_lead[i]:
                MS_Quote_Winners.append(i)
            elif MS_lead[i] > Bom_lead[i]:
                Bom_Winners.append(i)
            else: # if both lead times are equal, compare price
                if Bom_prices[i]>MS_prices[i]:
                    MS_Quote_Winners.append(i)
                else:
                    Bom_Winners.append(i)
        else:
            if (Bom_lead[i]>15 and MS_lead[i]>15) | (Bom_lead[i]<=15 and MS_lead[i]<=15) | (Bom_lead[i] == MS_lead[i]): 
            # if both lead times >, <, or = 15 weeks or are equal with each other, skip to price comparison
                if Bom_prices[i]>MS_prices[i]:
                    MS_Quote_Winners.append(i)
                elif Bom_prices[i]<MS_prices[i]:
                    Bom_Winners.append(i)
                else: # if equal prices
                    Bom_Winners.append(i)
                    MS_Quote_Winners.append(i)
            elif Bom_lead[i]>15 & MS_lead[i]<=15:  
                MS_Quote_Winners.append(i)
            elif Bom_lead[i]<=15 & MS_lead[i]>15:
                Bom_Winners.append(i)
    
    Bom_Win = result.loc[Bom_Winners]
    MS_Win = result.loc[MS_Quote_Winners]
    Bom_Win=Bom_Win.drop(Bom_Win[['Order Unit Price','Lead Time in Weeks']],1)
    MS_Win = MS_Win.drop(MS_Win[['Unit Price','Mfg Std Lead Time']],1)

    Bom_Win.to_excel('Bom_Parts.xlsx')
    MS_Win.to_excel('MS_Quote_Parts.xlsx')

    print("Wrote selected purchases to Bom_Parts.xlsx and MS_Quote_Parts.xlsx")

if __name__ == "__main__":
    parse_hardware_bom_('Bom.csv', 'MS Quote Request.xls')
