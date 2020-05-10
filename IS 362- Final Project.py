#!/usr/bin/env python
# coding: utf-8

# # IS 362- Final Project

# ### NYC Open Parking And Camera Violations

# ### {Presented by: Khairul Chowdhury}
# 

# ### CSV Source online downloaded from:
#     1)Parking Violations Issued - Fiscal Year 2020-2018 https://catalog.data.gov/dataset/parking-violations-issued-fiscal-year-2018
#     2)DOF Parking Violation Codes February 7, 2020 https://data.cityofnewyork.us/Transportation/DOF-Parking-Violation-Codes/ncbg-6agr

# In[6]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('pylab', 'inline')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[7]:


data = pd.read_csv('Parking_Violations_Issued_-_Fiscal_Year_2018.csv', 
                   dtype={'Summon Number': np.int64, 
                          'Plate ID': object, 
                         'Registration State': object, 
                         'Plate Type': object, 
                         'Issue Date': object, 
                         'Violation Code': np.int64, 
                         'Vehicle Body Type': object, 
                         'Vehicle Make': object, 
                         'Issuing Agency': object, 
                         'Street Code1': np.int64, 
                         'Street Code2': np.int64, 
                         'Street Code3': np.int64, 
                         'Vehicle Expiration Date': np.int64, 
                         'Violation Loation': np.float64, 
                         'Violation Precinct': np.int64, 
                         'Issuer Precinct': np.int64,
                         'Issuer Code': np.int64, 
                         'Issuer Command': object, 
                         'Issuer Squad': object, 
                         'Violation Time': object, 
                         'Time First Observed': object, 
                         'Violaion County': object, 
                         'Violation In Front Of Or Opposite': object, 
                         'House Number': object, 
                         'Street Name': object, 
                         'Intersecting Street': object, 
                         'Date First Observed': np.int64, 
                         'Law Section': np.int64, 
                         'Sub Division': object, 
                         'Violation Legal Code': object,
                         'Days Parking In Effect': object, 
                         'From Hours In Effect': object, 
                         'To Hours In Effect': object, 
                         'Vehicle Color': object, 
                         'Unregistered Vehicle?': np.float64, 
                         'Vehicle Year': np.int64, 
                         'Meter Number': object, 
                         'Feet From Curb': np.int64,
                         'Violation Post Code': object, 
                         'Violation Description': object, 
                         'No Standig or Stopping Violation': np.float64, 
                         'Hydrant Violation': np.float64, 
                         'Double Parking Violation': np.float64}, low_memory=False)


# In[8]:


data.dtypes


# # Converting 'Issue date' to datetime datatype

# In[9]:


data['Issue Date'] = pd.to_datetime(data['Issue Date'], errors='coerce')


# In[10]:


data.dtypes.head(5)


# ### Cleaning data for Null values 

# In[11]:


data.isnull().sum()


# In[12]:


clear_data = data.fillna(0) # Filling null values
clear_data.isnull().sum() # Checking if any null remains


# In[13]:



clear_data.head(10) # reading data


# In[14]:


clear_data.shape  # Total rows and columns


# ### Total Number for Violation by County

# In[15]:


v_count = clear_data.groupby('Violation County')['Violation Code'].count().sort_values(ascending=False)
v_count.plot()
plt.suptitle('# of Violation by County')
plt.xlabel('County')
plt.ylabel('# of Violation')

v_count


# #### Sorting Violation only for County = BX

# In[16]:


# Bronx = clear_data['Violation County']== 'BX'
q_county = clear_data[['Violation County', 'Violation Code']] # Selecting only two columns
q_only = q_county[q_county['Violation County'] == 'BX']
q_only.sort_values(by='Violation Code').head(10).sort_values(by='Violation Code', ascending=False)


# ### Importing another CSV with Violation fine and codes

# In[17]:


column = ['Violation Code','Definition', 'Manhattan 96th St. & below', 'All Other Areas'] # setting column names
v_code = pd.read_csv('DOF_Parking_Violation_Codes_1.csv', names=column, header=None ) # imporint CSV
code = v_code.iloc[1:] # selecting column from 2nd row 
code.shape


# In[18]:


code


# In[19]:


code.dtypes


# Since, all 4 columns are object, we need to change column 'Violation Code', 'Manhattan 96th St. & below' & 'All Other Areas' to numeric datatype. In order to do that we need to clean few rows first since, it contains strings as well. We can check row 81, 74, 24 etc.

# In[20]:


row = code.loc[code['Violation Code']=='37-38']
code = code.append([row]*1, ignore_index=True) # copying row and apppend
code.shape


# In[21]:


code.loc[code['Violation Code']=='37-38'] # printing just to confirm


# In[29]:


code.loc[[23],'Violation Code'] = '37' # changing values '37-38' to 37
code.loc[[84],'Violation Code'] = '38' # changing values '37-38' to 38


# In[30]:


code.loc[[23, 84]]


# In[31]:


# converting datatype of 'Violation Code' column to numeric
code['Violation Code'] = pd.to_numeric(code['Violation Code'], errors='coerce')


# In[32]:


code.dtypes


# In[33]:


code.loc[[73, 80]]


# In[34]:


# Change values in row 73, 80
code.loc[[73], 'Manhattan 96th St. & below'] = '100'
code.loc[[73], 'All Other Areas'] = '200'
code.loc[[80], 'Manhattan 96th St. & below'] = '265'
code.loc[[80], 'All Other Areas'] = '265'


# In[35]:


code.loc[[73, 80]]


# In[36]:


code.head(10)


# In[37]:


# since colun, 'Manhattan 96th St. & below' & 'All other Areas' has $ sign, we need to remove $
code = code[code.columns[:]].replace('[\$,]', '', regex=True)


# In[38]:


code.fillna(0) # Changing null values to 0


# In[39]:


code.loc[[77], 'Manhattan 96th St. & below'] = '60'
code.loc[[77], 'All Other Areas'] = '60'
code.loc[[81], 'Manhattan 96th St. & below'] = '50'
code.loc[[81], 'All Other Areas'] = '50'
code.loc[[82], 'Manhattan 96th St. & below'] = '115'
code.loc[[82], 'All Other Areas'] = '115'


# In[40]:


code.loc[[77, 81, 82]]


# In[41]:



code.isnull().sum()


# In[42]:


code.loc[[78], 'All Other Areas'] = '115'


# In[43]:



code.isnull().sum()


# In[44]:


code.dtypes


# In[45]:


code['Manhattan 96th St. & below'] = pd.to_numeric(code['Manhattan 96th St. & below'], errors='coerce')
code['All Other Areas'] = pd.to_numeric(code['All Other Areas'], errors='coerce')


# In[46]:


code.dtypes


# In[47]:


code.head()


# ## Merging two data based on 'Violation Code

# In[48]:


merge = pd.merge(q_only, code, on='Violation Code')
merge.head(5)


# In[49]:


merge.shape


# ### Revenue generated based on violation in Bronx only

# In[50]:


merge[['Violation Code', 'All Other Areas']].agg({'All Other Areas': np.sum})


# ### Merging violation fine with clean data

# In[51]:


new_merge = pd.merge(clear_data, code, on='Violation Code')
new_merge.head(3)


# In[52]:


Selected_data = new_merge[['Violation Code', 
                          'Issuing Agency', 
                          'Issue Date',
                           'Violation County', 
                          'All Other Areas']]
Selected_data['# of Violation'] = Selected_data['All Other Areas']
Selected_data['Revenue'] = Selected_data['All Other Areas']

Selected_data.head()
top100_selected = Selected_data.head(100).sort_values(by='# of Violation', ascending=False)
Selected_data.head()


# #### Top Violation Code grouped by County and Total Number

# In[53]:


violation_group = Selected_data.groupby(['Violation Code', 'Violation County']).count().sort_values(by='# of Violation', ascending=False)
top10 = violation_group[['# of Violation']].head(10)
top10.plot.bar()
top10


# In[54]:


sns.lmplot('Violation Code', '# of Violation', data= Selected_data, fit_reg=False)


# Revenue Generated in County by Violation Code

# In[55]:


a_data = Selected_data.groupby(['Violation Code', 'Violation County']). agg({'Revenue': np.sum})
top10_data = a_data.sort_values(by='Revenue', ascending=False).head(10)
top10_data.plot.bar()
plt.suptitle('Top 10 Violation Code & County')
plt.ylabel('Revenue')
top10_data


# #### Top 10 Violation Code and Revenue generated

# In[57]:


a_data = Selected_data.groupby(['Violation Code']). agg({'Revenue': np.sum})
top10_data = a_data.sort_values(by='Revenue', ascending=False).head(10)
top10_data.plot.bar(color='R')
plt.suptitle('Top 10 Violation Code')
plt.xlabel('Violation Code')
plt.ylabel('Revenue')
top10_data


# #### Total generate Revenue by County

# In[59]:



Revenue = Selected_data.groupby(['Violation County']).agg({'Revenue': np.sum})
Revenue_sorted = Revenue.sort_values(by='Revenue', ascending=False)
Revenue_sorted.plot.area(color='B')
plt.suptitle('Revenue Generate by County')
plt.xlabel('County')
plt.ylabel('Revenue')
Revenue_sorted


# In[60]:


Rev = Revenue['Revenue'].sort_values(ascending=False)
County = ['NY', 'K', 'Q', 'BX', 'BK', 'QN', 'R', 'MN', '0', 'ST']
series = pd.Series(Rev, index=County, name='seriers')
series.plot.pie(figsize=(6,6))
plt.suptitle('Revenue Generate by County')
Rev


# #### Analyzing total number for violation, and revenue sum by County

# In[61]:


Analysis = new_merge[['Violation County', 'Violation Code', 'All Other Areas']]
chart = Analysis.groupby('Violation County')['All Other Areas'].agg(['count', 'sum', 'mean']).sort_values(by='sum', ascending=False)
chart.plot.line()
chart


# In[63]:


sns.lmplot(x='count', y='sum',data=chart, size=4)


# In[ ]:




