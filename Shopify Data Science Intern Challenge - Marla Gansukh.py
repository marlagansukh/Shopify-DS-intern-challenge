#!/usr/bin/env python
# coding: utf-8

# # SHOPIFY DATA SCIENCE INTERN CHALLENGE/FALL 2022 

# Analyst: Marla Gansukh 
# > Purpose of the analysis
# - Defining the AOV(Average Order Value) for merchants of the Shopify. 
# - Finding errors that can have an impact for the purity of our analysis
# - Finding the appropriate solution to deal with errors

# Since there were no explanations for the data, I have considered order_amount column as the price of the order.

# In[2]:


#importing necessary libraries for the analysis
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
sneakers = pd.read_csv(r"C:\Users\marla\Downloads\2019 Winter Data Science Intern Challenge Data Set - Sheet1.csv")
#making irrelevant columns an index column so it doesn't have an impact for the analysis
sneakers.set_index(["order_id","shop_id","user_id"], inplace=True)
#displaying the data and datatypes we will be working with and checking for any null values
sneakers.info()


# In[3]:


#displaying a boxplot graph to check for outliers in the order amount
sns.boxplot(x=sneakers['order_amount'])
plt.show()


# In[4]:


#displaying plot graph to observe the distribution of the order amount and we can see that the data is left-skewed
sns.displot(sneakers, x="order_amount", kind="kde", fill=True)
plt.show()


# In[5]:


#finding the statistical values that are necessary for our further analysis and observe potential outliers
sneakers[["order_amount"]].describe()


# In[6]:


#finding the 25th percent of the order_amount so we can find IQR
sneakers["order_amount"].quantile(0.25)


# In[7]:


#finding the 75th percent of the order_amount
sneakers["order_amount"].quantile(0.75)


# In[8]:


#finding the IQR
Q1=sneakers['order_amount'].quantile(0.25)
Q3=sneakers['order_amount'].quantile(0.75)
IQR=Q3-Q1
print(IQR)


# In[9]:


#we need to set the limit for the analysis so we can eliminate outliers that are not between that limit
#the calculation shows us that the lower limit is a negative number
#since the lower limit cannot be a negative number I have taken the value of 0 and carried on with my analysis
lower_limit = Q1-1.5*IQR
upper_limit = Q3+1.5*IQR
lower_lim = 0
print(lower_limit)
print(upper_limit)
print(lower_lim)


# In[10]:


#counting the values that are between the limit that we have set to eliminate the outliers
#141 values have been eliminated from the total 5000 values 
outliers_low = (sneakers["order_amount"]<lower_lim)
outliers_upper = (sneakers["order_amount"]>upper_limit)
len(sneakers["order_amount"])-(len(sneakers["order_amount"][outliers_low])+len(sneakers["order_amount"][outliers_upper]))


# In[11]:


#displaying outliers that have been eliminated
sneakers['order_amount'][(outliers_low | outliers_upper)]


# In[12]:


#dataframe after dropping the outliers
sneakers['order_amount'][~(outliers_low | outliers_upper)]


# In[13]:


sneakers = sneakers[~(outliers_low | outliers_upper)]


# In[14]:


sneakers


# In[15]:


#after handling the outliers we can see that the box plot looks so much better than before 
#the dots outside the boxplot graph are outliers that have been eliminated previously 
sns.boxplot(x=sneakers["order_amount"])
plt.show()


# In[16]:


#in the distribution graph we can see that after handling the outliers it looks more normally distributed
sns.displot(sneakers, x='order_amount', kind="kde", fill=True)
plt.show()


# In[25]:


#finding the revenue in order to calculate AOV
sneakers["revenue"]=sneakers["order_amount"]*sneakers["total_items"]
print(sneakers)


# In[26]:


#finding the AOV 
sneakers["AOV"] = sneakers["revenue"]/sneakers["total_items"]
print(sneakers)


# In[31]:


#grouping our final result by the shop_id and user_id so that it is more easier to analyze the final result. 
group = sneakers.groupby(["shop_id","user_id"])
group.first()


# <b> Conclusion: I am convinced that the reason behind the abnormal AOV is because the outliers have not been eliminated before diving into the analysis and it affected the whole dataset. With the proper outlier handling technique, the AOV can be calculated accurately. In the analysis above, I have used only the method that I am familiar with and tried my best to visualize the output and made the dataset as organized as I could with the help of pandas library. I have documented every single step I did so it is more easier for non-technical professionals to understand.  <b> 
