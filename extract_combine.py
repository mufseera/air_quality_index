from plot_aqi import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016,avg_data_2017,avg_data_2018
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv
import sys



    
def met_data(month,year):
    file_html=open("Data/Html_Data/{}/{}.html".format(year,month),"rb")
    plain_text=file_html.read()
    
    temp_d=[]
    final_d=[]
    soup=BeautifulSoup(plain_text,"lxml")
    

    for table in soup.findAll("table",{"class":"medias mensuales numspan"}):
        for tbody in table:
            for tr in tbody:
                a=tr.get_text()
                temp_d.append(a)
    rows=len(temp_d)/15


    for i in range(round(rows)):
        new_temp_d=[]
        for j in range(15):
            new_temp_d.append(temp_d[0])
            temp_d.pop(0)
        final_d.append(new_temp_d)
    length=len(final_d)


    final_d.pop(length-1)
    final_d.pop(0)



    for a in range(len(final_d)):
        final_d[a].pop(6)
        final_d[a].pop(13)
        final_d[a].pop(12)
        final_d[a].pop(11)
        final_d[a].pop(10)
        final_d[a].pop(9)
        final_d[a].pop(0)



    return final_d





def data_combine(year,cs):
    for a in pd.read_csv("Data/Real_Data/real_" +str(year) +".csv",chunksize=cs):
        df=pd.DataFrame(data=a)
        mylist=df.values.tolist()
    return mylist






if __name__=="__main__":
    if not os.path.exists("Data/Real_Data"):
        os.makedirs("Data/Real_Data")
    for year in range(2013,2017):
        final_data=[]
        with open("Data/Real_Data/real_"+str(year)+".csv","w") as csvfile:
            wr=csv.writer(csvfile,dialect="excel")
            wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1,13):
            temp=met_data(month,year)
            final_data=final_data+temp



        pm=getattr(sys.modules[__name__],"avg_data_{}".format(year))()


        for i in range(len(final_data)-1):
            final_data[i].insert(8,pm[i])

        with open("Data/Real_Data/real_" + str(year)+ ".csv","a") as csvfile:
            wr=csv.writer(csvfile,dialect="excel")
            for row in final_data:
                flag=0
                for elem in row:
                    if elem=="" or elem=="-":
                        flag=1
                    if flag!=1:
                        wr.writerow(row)
    



    data_2013=data_combine(2013,700)
    data_2014=data_combine(2014,700)
    data_2015=data_combine(2015,700)
    data_2016=data_combine(2016,700)
    # data_2017=data_combine(2017,700)
    # data_2018=data_combine(2018,700)


    total=data_2013+data_2014+data_2015+data_2016


    with open("Data/Real_Data/Real_Combine.csv","w") as csvfile:
        wr=csv.writer(csvfile,dialect="excel")
        wr.writerow(['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
    df=pd.read_csv("Data/Real_Data/Real_Combine.csv")
    print(df.shape)





















































