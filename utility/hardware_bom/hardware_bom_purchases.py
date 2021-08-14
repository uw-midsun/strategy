# Requirements: 
# 1. Entering data spreadsheets to the function in order as referenced.
# 2. Updating priority field on both spreadsheets, ensuring value is equal on both. 

import pandas as pd
bom_winners = pd.DataFrame()
ms_quote_winners = pd.DataFrame()

# parse_hardware_bom will accept the BOM.csv and MS_Quote Excel File and return two seperate Excel/CSV files with winning parts. 
def parse_hardware_bom(bom_file, ms_quote_file): 
    global bom_winners, ms_quote_winners

    bom_df = pd.read_csv(bom_file)
    ms_quote_df = pd.read_excel(ms_quote_file)
    
    #  Create DF of relevant information.
    bom_df = bom_df[['Manufacturer Part Number', 'Description', 'Unit Price', 'Mfg Std Lead Time']]
    ms_quote_df = ms_quote_df[['Mfr. #', 'Description', 'Order Unit Price', 'Lead Time in Weeks', 'Priority']] 
    bom_df = bom_df.rename(columns = {'Manufacturer Part Number':'Mfr. #'}) 

    # Fill Nan values with zeroes for calculation purposes.
    bom_df['Mfg Std Lead Time'] = bom_df['Mfg Std Lead Time'].fillna(0) 
    ms_quote_df['Lead Time in Weeks'] = ms_quote_df['Lead Time in Weeks'].fillna(0)

    # Correct issue of having "$" in front of numeric price value.
    ms_quote_df['Order Unit Price'] = ms_quote_df['Order Unit Price'].replace('[\$]', '', regex = True).astype(float)
    
    # Correct issue where lead times is an integer followed by "Weeks"
    bom_df['Mfg Std Lead Time'] = bom_df['Mfg Std Lead Time'].map(
        lambda row: int(row.replace('Weeks', '')) if type(row) == str else int(row)
    )
    
    # Merges the two files on common column 'Mfr. #'
    result = pd.merge(left = bom_df, right = ms_quote_df, on = 'Mfr. #')

    for _, row in result.iterrows():
        if row['Priority'] == 'y': #
            select_on_time(row)     
        elif row['Priority'] == 'n':
            if (row['Mfg Std Lead Time'] > 15 and row['Lead Time in Weeks'] > 15) or \
                (row['Mfg Std Lead Time'] <= 15 and row['Lead Time in Weeks'] <= 15) or \
                (row['Mfg Std Lead Time'] == row['Lead Time in Weeks']):
                
                select_on_price(row)
            elif row['Mfg Std Lead Time'] < row['Lead Time in Weeks']:
                bom_winners = bom_winners.append(row)
            elif row['Mfg Std Lead Time'] > row['Lead Time in Weeks']:
                ms_quote_winners = ms_quote_winners.append(row)

    bom_winners = bom_winners.drop(bom_winners[['Order Unit Price','Lead Time in Weeks']], 1)
    ms_quote_winners = ms_quote_winners.drop(ms_quote_winners[['Unit Price','Mfg Std Lead Time']], 1)

    bom_winners.to_excel('Bom_Parts.xlsx')
    ms_quote_winners.to_excel('MS_Quote_Parts.xlsx')

    print("Wrote selected purchases to Bom_Parts.xlsx and MS_Quote_Parts.xlsx")

def select_on_time(row):
    global bom_winners, ms_quote_winners
    if row['Mfg Std Lead Time'] < row['Lead Time in Weeks']:
        bom_winners = bom_winners.append(row)
    elif row['Mfg Std Lead Time'] > row['Lead Time in Weeks']:
        ms_quote_winners = ms_quote_winners.append(row)
    elif row['Mfg Std Lead Time'] == row['Lead Time in Weeks']:
        select_on_price(row)
    
def select_on_price(row):
    global bom_winners, ms_quote_winners
    if row['Unit Price'] < row['Order Unit Price']:
        bom_winners = bom_winners.append(row)
    elif row['Unit Price'] > row['Order Unit Price']:
        ms_quote_winners = ms_quote_winners.append(row)
    else:
        ms_quote_winners = ms_quote_winners.append(row)
        bom_winners = bom_winners.append(row)
        
if __name__ == "__main__":
    parse_hardware_bom('Bom.csv', 'MS Quote Request.xls')
