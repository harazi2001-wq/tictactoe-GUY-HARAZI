#Name:Guy Harazi
#ID:212168421
import numpy as np
import pandas as pd

#-----Q1------
# Q1a
v1 = np.linspace(0, 100, 11, dtype=int)
print("Q1a:", v1)

# Q1b
v2 = np.arange(0, 101, 10)
print("Q1b:", v2)

# Q1c
v3 = v2[:-1].reshape(2, 5)
print("Q1c:\n", v3)

#-----Q2--------

df = pd.read_csv("customerData.csv")
df.columns = df.columns.str.strip()
print("\nQ2 preview:")
print(df.head())

#Q2a
print(df.shape)

#Q2b
print(df.dtypes)

#Q2C
#תשובה: custid הוא רק מזהה,זה תיוג של כל לקוח בקובץ , אבל אינו מתאר דבר בעל משמעות
# כמו גיל ,הכנסה וכו , לכן לא ניתן ללמוד או לחזות מזה משהו

#------Q3-------

q3 = df.iloc[::10, ::2]
print(q3)

#------Q4--------

#Q4a
print(df.shape)
print(type(df.shape))

#Q4b
print(df.size)

#Q4c
#תשובה: כן כי df.shape מחזירה טאפל וdf.shape מחזירה מספר כולל של ערכים במסגרת
# כן ניתן לחשב כך df.size מ- df.shape
#כך
print(df.shape[0] * df.shape[1])

#-----Q5----------

q5 = df[(df["age"] >= 38) & (df["age"] <= 50)]
print(q5)

#------Q6---------

#Q6a
q6a = df[df["age"] > 50].select_dtypes(include=["number"])
print(q6a)

#Q6b
age_idx = df.columns.get_loc("age")
q6b = df.iloc[df.iloc[:, age_idx] > 50, :]
q6b = q6b.select_dtypes(include=["number"])
print(q6b)

#------Q7---------

q7 = df.iloc[:100, [df.columns.get_loc("age")]]
print(q7)
print(type(q7))

#-----Q8---------

print(df.loc[(df["marital_stat"].isin(["Married", "Divorced/Separated"])) & (df["age"] < 18), "custid"])

#------Q9-------

#Q9a
print(df.loc[(df["income"] > 16000) & (df["state_of_res"] == "Washington"), "age"].mean())

#Q9b
print(df.loc[(df["income"] > 16000) & (df["state_of_res"] == "Washington"), "age"].max())
#תשובה:130.4016047

#Q9c
print(df.loc[(df["income"] > 16000) & (df["state_of_res"] == "Washington"), "income"].min())
#תשובה:19200

#Q9d
print(df.loc[(df["income"] > 16000) & (df["state_of_res"] == "Washington")].shape[0])
#תשובה:13

#-------Q10---------
grouped = df.groupby(["gender", "housing_type"]).size()
print(grouped)

# Q10a
print(df.loc[df["gender"] == "F", "housing_type"].mode()[0])
#התשובה:Rented

#Q10b
print(df.loc[df["gender"] == "M", "housing_type"].mode()[0])
#תשובה: Homeowner with mortgage/loan




