#!/usr/bin/env python
# coding: utf-8

# # Chapter 2 – Pandas, NumPy, and Matplotlib  
# ## Part 1: Processing Vaccine Adverse Event Data with pandas
# This notebook focuses on **introducing pandas and DataFrame joins** using VAERS as a motivating example.  
# To simulate real-world analytical challenges such as missing or incomplete data, we intentionally work with **random subsets of the data** and examine how careless joins can introduce subtle but critical errors.
# 
# These concepts are foundational for downstream bioinformatics analyses, including multi-omics integration, clinical data analysis, and large-scale epidemiological studies.
# 
# 




import pandas as pd
import matplotlib.pyplot as plt
vdata = pd.read_csv("C:/Users/razon/Downloads/2021VAERSData/2021VAERSDATA.zip", encoding="iso-8859-1")
vdata.columns
vdata.dtypes
vdata.shape





vdata.iloc[0]
vdata = vdata.set_index("VAERS_ID")



vdata.loc[916600]





vdata.head(3)





vdata.iloc[:3]

vdata.iloc[:5, 2:4]

vdata["AGE_YRS"].max()

vdata.AGE_YRS.max()



vdata["AGE_YRS"].sort_values().plot(use_index=False)

fig, ax = plt.subplots(1, 2, sharey=True, dpi=300)
fig.suptitle("Age of adverse events")
vdata["AGE_YRS"].sort_values().plot(use_index=False, ax=ax[0], xlabel="Obervation", ylabel="Age")
vdata["AGE_YRS"].plot.hist(bins=20, orientation="horizontal")
fig.savefig("adverse.png")
vdata["AGE_YRS"].dropna().apply(lambda x: int(x)).value_counts()





vdata.DIED.value_counts(dropna=False)
vdata["is_dead"] = (vdata.DIED == "Y") 





dead = vdata[vdata.is_dead]
vax = pd.read_csv("C:/Users/razon/Downloads/2021VAERSData/2021VAERSVAX.zip", encoding="iso-8859-1").set_index("VAERS_ID")
vax.groupby("VAX_TYPE").size().sort_values()
vax19 = vax[vax.VAX_TYPE == "COVID19"]
vax19_dead = dead.join(vax19, lsuffix='_dead', rsuffix='_vax')
vax19_dead.index.value_counts()




vax19_dead




baddies = vax19_dead.groupby("VAX_LOT").size().sort_values(ascending=False)
for i, (lot, cnt) in enumerate(baddies.items()):
    print(lot, cnt, len(vax19_dead[vax19_dead.VAX_LOT == lot].groupby("STATE")))
    if i == 10:
        break





vdata = pd.read_csv("vdata_sample.csv.gz")
vax = pd.read_csv("vax_sample.csv.gz")

vdata_with_vax = pd.merge(
    vdata,
    vax,
    on="VAERS_ID",
    how="inner",
    suffixes=('_vdata', '_vax')
)

print(len(vdata), len(vax), len(vdata_with_vax))





lost_vdata = vdata.loc[~vdata.index.isin(vdata_with_vax.index)]
lost_vdata

lost_vax = vax[~vax["VAERS_ID"].isin(vdata_with_vax["VAERS_ID"])]
lost_vax





overlaps = vdata.columns.intersection(vax.columns)
print(overlaps)






