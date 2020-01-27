# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 15:36:20 2019

@author: Neelam
"""


import numpy as np
from flask import Flask, request, jsonify, render_template,send_file
import pickle
import pandas as pd
import numpy as np
import io
import json
import seaborn as sns
app = Flask(__name__) #Initialize the flask App

#model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return jsonify("hi")

@app.route('/predict',methods=['POST','GET'])
def order():
    data=pd.read_csv(r'C:\Users\Neelam\Desktop\Codes\nyco.csv')
    #order = request.get_json()
    order=json.loads(request.data)
    orderno=order['data']
    #orderno=int(orderno)
    
    new = data.loc[data['Order_ID'] == int(orderno)]

        
    profit=[]
    cp=[]
    
    for index,row in new.iterrows():
        pro=row['SP']-row['CP']
        pro=pro*row['quantity']
        cp2=row['CP']*row['quantity']
        cp.append(cp2)
        
        profit.append(pro)
    
    
    
    totcp=sum(cp)
    totalpro=sum(profit)
    
    profitpercentz=(totalpro/totcp)*100
    print(profitpercentz)
    new['ProfitPercent']="a"
    
    if profitpercentz>40:
        print("\nGood to go, free shipping !")
        return (jsonify("Free shipping !"))
    else:
        print("\nextra shipping fee required, total profit percent is :" + str(profitpercent) )
        below40 = pd.DataFrame()
        above40= pd.DataFrame()
        for index,row in new.iterrows():
            pro=row['SP']-row['CP']
            pro=pro*row['quantity']
            cp=row['CP']*row['quantity']
            profitpercent2=(pro/cp)*100
            new['ProfitPercent'][index] = profitpercent2
            
            if profitpercent2<40:
                below40=below40.append(row)
            else:
                above40=above40.append(row)
    print(new)
    
    #ax = new.plot.bar(x='Product_ID', y='ProfitPercent',label=profitpercent ,rot=0)
    ax = sns.barplot(x='Product_ID', y='ProfitPercent',label=profitpercentz ,data=new)
    ax=ax.axhline(40, ls='--')
    bytes_image=io.BytesIO()
    ax.figure.savefig(bytes_image,format='png')
    ax.get_figure().clf()
    bytes_image.seek(0)
    bytesobj=bytes_image
    
    
    
    
    
    return send_file(bytesobj,attachment_filename='plot.png',mimetype='image/png')

@app.route('/recommendation',methods=['POST','GET'])
def recc():
    #data=pd.read_csv(r'C:\Users\Neelam\Desktop\Codes\nyco.csv')
    pd.options.mode.chained_assignment = None
    
    data=pd.read_csv(r'C:\Users\Neelam\Desktop\Codes\nyco.csv')
    order=json.loads(request.data)
    orderno=order['data']
    
    new = data.loc[data['Order_ID'] == int(orderno)]
    
    
    profit=[]
    cp=[]
    
    for index,row in new.iterrows():
        pro=row['SP']-row['CP']
        pro=pro*row['quantity']
        cp2=row['CP']*row['quantity']
        cp.append(cp2)
        
        profit.append(pro)
    
    
    
    totcp=sum(cp)
    totalpro=sum(profit)
    
    profitpercent=(totalpro/totcp)*100
    new['ProfitPercent']="a"
    
    if profitpercent>40:
        print("\nGood to go, free shipping !")
        return jsonify("FREE SHIPPING")
    else:
        print("\nextra shipping fee required, total profit percent is :" + str(profitpercent) )
        below40 = pd.DataFrame()
        above40= pd.DataFrame()
        for index,row in new.iterrows():
            pro=row['SP']-row['CP']
            pro=pro*row['quantity']
            cp=row['CP']*row['quantity']
            profitpercent2=(pro/cp)*100
            new['ProfitPercent'][index] = profitpercent2
            
            if profitpercent2<40:
                below40=below40.append(row)
            else:
                above40=above40.append(row)
    
        below40pid=list(below40['Product_ID'])
      
        try:
            above40pid=list(above40['Product_ID'])
      
            print("\nremove these items for 0 shipping")
            print(below40pid)
           
            allstuff=below40pid+above40pid
        
            import itertools
        
            allcomb=[]
            for L in range(0, len(allstuff)+1):
                    for subset in itertools.combinations(allstuff, L):
                            
                            allcomb.append(subset)
                 
                        
            main=[] 
            comblast=[]
            pp=[]
            for i in allcomb:
                 if set(i) >= set(above40pid):          
                     
                     main.append(i)                   
                                                            
           
            for i in main:
                a=list(i)
                b=[int(m) for m in a]
                profit=[]
                cp=[]
                #print(b)
                for z in b:
               
                    j=new.loc[new['Product_ID'] == z]
                    pro=j['SP']-j['CP']
                    pro=pro*j['quantity']
                    cp2=j['CP']*j['quantity']
                    cp2=int(cp2)
                    pro=int(pro)
                    cp.append(cp2)
                    profit.append(pro)
                totcp=sum(cp)
                totcp=int(totcp)
                totalpro=sum(profit)
                totalpro=int(totalpro)
                profitpercent=(totalpro/totcp)*100
                profitpercent=int(profitpercent)
               
                
                if profitpercent>40:
                        print("\n This combination is greater that 40%")
                        print(profitpercent)
                        #print("\n")
                        print(a)
                        comblast.append(i)
                        new1=new[new['Product_ID'].isin(a)]
                        print(new1)
                        pp.append(profitpercent)
                        ax = new1.plot.bar(x='Product_ID', y='ProfitPercent', label=profitpercent,rot=0)                    
                else:
                        print("\nthis combination is less that 40")
                        print(profitpercent)
                        print(a)
    
                    
                  
            #ax = new.plot.bar(x='Product_ID', y='ProfitPercent',label=profitpercent ,rot=0)
    
    
        except:
            print("add more items for free shipping or pay $6.99 shipping charge")
            return jsonify("add more items for free shipping or pay $6.99 shipping charge")
        comblast=str(comblast)
        pp=str(pp)
        return jsonify("combinations > 40%",comblast,"profit percent",pp)
     


if __name__ == "__main__":
    app.run(debug=False)