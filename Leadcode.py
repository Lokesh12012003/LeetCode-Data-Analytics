
import pandas as pd

df=pd.read_excel(r"C:\Users\SARATHY RAMESH\Downloads\(102) Lead Filters.xlsx",header=1)

print(df.head(10))

#  rename to column one 
df=df.rename(columns={"#" : "Lead_ID"} )

# #  Safe sorting
df = df.sort_values(by="Lead_ID", ascending=True).reset_index(drop=True)


#                                 #   column 2

# # Step A: Text-a (String) maathrom
df['Name'] = df['Name'].astype(str)

# Step B: Tamil characters irundha 'Unknown Name'
df.loc[df['Name'].str.contains(r'[\u0B80-\u0BFF]', regex=True), 'Name'] = 'Unknown Name'

# Step C: English Letters & Space THAVIRA mitha ellathaiyum (Numbers, Symbols, Junk) thookrom
df['Name'] = df['Name'].str.replace(r'[^a-zA-Z\s]', ' ', regex=True)

# Step D: Extra spaces thooki Proper Capitalization (Title Case) panrom
df['Name'] = df['Name'].str.split().str.join(' ').str.title()

# Step E: Single letter or Empty-a irundha 'Unknown Name'
df.loc[df['Name'].str.len() <= 1, 'Name'] = 'Unknown Name'

# # Output check
# print(df[['Name']].head(10))


#                                # column 3


# # # 1 Blank values & Symbols/Numbers irundha 'Chennai' nu fill pandrom
df['City'] = df['City'].fillna('Chennai').astype(str)
df['City'] = df['City'].str.replace(r'.*[^a-zA-Z\s].*', 'Chennai', regex=True)

# 2 Capitalize and remove extra space
df['City'] = df['City'].str.strip().str.title()

# Result Output
# print(df[['City']].head(6))

#                             #   column 4
                        

# # 1. Blank Values & Non-English Characters (Tamil/Numbers/Symbols) -> 'Tamil Nadu'
df['State'] = df['State'].fillna('Tamil Nadu').astype(str)
df['State'] = df['State'].str.replace(
    r'.*[^a-zA-Z\s].*', 'Tamil Nadu', regex=True
)

# 2. Extra Spaces Clear Panni Capital-a Maathrom
df['State'] = df['State'].str.strip().str.title()

# Result Check
# print(df[['State']].head(15))

                            # column 5

# 1.empty values fill india
df["Country"] = df["Country"].fillna("india")

# 2. Clean spaces & First letter Capital
df['Country'] = df['Country'].str.strip().str.title()

print(df['Country'])


                            # column 6


#  drop the column
print(df.drop(columns=["Zip Code"],inplace=True))

                           # column 7




# 1. Column Name Rename Pandrom ('Lead Value' -> 'Lead_Value')
df = df.rename(columns={'Lead value': 'Lead_Value'})

# 3. Currency Symbols ($, ₹), Commas & Spaces Clear Pandrom
df['Lead_Value'] = (
    df['Lead_Value'].astype(str).str.replace(r'[₹$,\s]', '', regex=True)
)

# 4. Pure Numbers-a Maathi, Blank Values-ku 0 Fill Pandrom
df['Lead_Value'] = (
    pd.to_numeric(df['Lead_Value'], errors='coerce').fillna(0).astype(int)
)

# Output Check
# print(df[['Lead_Value']].head(15))



                                    # column 8  

# 1. Column Name Rename Pandrom ('Status' -> 'Status')
df = df.rename(columns={'Status': 'Status'})

# 2. Blank / Tamil Text / Symbols irundha -> 'Pending' nu fill pandrom
df['Status'] = df['Status'].fillna('Pending').astype(str)
df['Status'] = df['Status'].str.replace(
    r'.*[^a-zA-Z\s].*', 'Pending', regex=True
)

# 3. Extra spaces clear panni Capitalized First Letter-a maathrom
df['Status'] = df['Status'].str.strip().str.title()
df['Status'] = df['Status'].replace('', 'Pending')

# # Output Check
# print(df[['Status']].head(15))

                                     # column 9
         


# 1. just empt value irundha replace pannum 
df['Source'] = df['Source'].fillna('Organic / Direct').astype(str)

# 2. Extra spaces clear panni Capitalized First Letter-a maathrom
df['Source'] = df['Source'].str.strip().str.title()


# # Output Check
# print(df[['Source']].head(50))

                                     # column 10


# 1.rename to column 
df = df.rename(columns={ "Created Date": "Created_Date"})

# 2. utc=True use panni Timezone error-a bypass pandrom
df['Created_Date'] = pd.to_datetime(
    df['Created_Date'], errors='coerce', dayfirst=True, utc=True
)

# 3. Valid dates-a direct-a 'YYYY-MM-DD' String-a maathidrom
df['Created_Date'] = df['Created_Date'].dt.strftime('%Y-%m-%d')

# 4. Missing / Invalid values-ku Today's Date-a string-a fill pandrom
today_str = pd.Timestamp.now().strftime('%Y-%m-%d')
df['Created_Date'] = df['Created_Date'].fillna(today_str)

# Output Check
# print(df[['Created_Date']].head(15))




                              # column 11 




# # 1. Rename Column
df = df.rename(columns={'Last Contact': 'Last_Contact'})

# 2 Convert to Datetime (Handles text, Tamil characters & timezones)
df['Last_Contact'] = pd.to_datetime(
    df['Last_Contact'], errors='coerce', dayfirst=True, utc=True
)

# 3. Future dates-a fix pandrom
today_utc = pd.Timestamp.now(tz='UTC')
df.loc[df['Last_Contact'] > today_utc, 'Last_Contact'] = pd.NaT

# 4. Format YYYY-MM-DD & Blanks/Text-ku 'Not Contacted' fill pandrom
df['Last_Contact'] = (
    df['Last_Contact'].dt.strftime('%Y-%m-%d').fillna('Not Contacted')
)

# # Check Output
# print(df[['Last_Contact']].head(15))


                          # column 12


# 1. Clean spaces & make standard Title Case
df['Public'] = df['Public'].astype(str).str.strip().str.title()

# 2. Fix all blanks, N/A & invalid text to 'Unknown'
df['Public'] = df['Public'].replace(
    ['Nan', 'None', '', 'Null', 'N/A'], 'Unknown'
)

                          # column 13


# 1. Strip extra spaces & Standardize Name Format (Title Case)
df['Assigned'] = df['Assigned'].astype(str).str.strip().str.title()

# 2. Fix blanks, N/A, numbers & missing entries to 'Unassigned'
df['Assigned'] = df['Assigned'].replace(
    ['Nan', 'None', '', 'Null', 'N/A', '0', 'Pending'], 'Unassigned'
)
                         

                              # column 14                              

# 1. Strip extra spaces & Standardize Format (Title Case)
df['Tags'] = df['Tags'].astype(str).str.strip().str.title()

# 2. Fix dynamic typos & variations (e.g., 'Followup' / 'Follow-Up' -> 'Follow Up')
df['Tags'] = df['Tags'].replace(
    {'Followup': 'Follow Up', 'Follow-Up': 'Follow Up', 'Colld Lead': 'Cold Lead'}
)

# 3. Fix blanks, N/A, NaN & invalid placeholders to 'No Tag'
df['Tags'] = df['Tags'].replace(
    ['Nan', 'None', '', 'Null', 'N/A', '0', '---', 'Nil'], 'No Tag'
)


# print(df['Tags'].head(50))


df.to_csv('Cleaned_codedata.csv', index=False)
# df.to_excel('Cleaned_codedata.xlsx', index=False)

