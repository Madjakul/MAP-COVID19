from elasticsearch import helpers, Elasticsearch
import csv
import pandas as pd
from googletrans import Translator
import sys,os

def ExtractCSVHopkins(pathname):
    df=pd.read_csv(dataPath,sep=',',dtype={'Province/State':str,'Country/Region':str})
    
    df=df.melt(id_vars=['Province/State','Country/Region','Lat','Long'],var_name="Date")
    df=df[['Date','Province/State','Country/Region','Lat','Long','value']]
    df=df.drop(columns=['Lat','Long'])
    df['value']=pd.to_numeric(df['value'])

    #Gestion des Province/State + NaN
    df=df.fillna('nc')
    cr=list(df['Country/Region'])
    cr=list(dict.fromkeys(cr))
    crNC=list(df.loc[df['Province/State']!='nc','Country/Region'])
    crNC=list(dict.fromkeys(crNC))

    date=list(df['Date'])
    date=list(dict.fromkeys(date))

    for c in cr: 
        for d in date: 
            somme=df.loc[(df['Country/Region']==c) &(df['Date']==d),'value'].sum()
            indices=list(df.loc[(df['Country/Region']==c) &(df['Date']==d),'value'].index)

            df.loc[:,'value'].iloc[indices]=somme

    df=df.drop(columns=['Province/State'])
    df=df.drop_duplicates()
    #df.to_csv(pathname+'/result.csv')
    documents=df.to_dict(orient='records')
    return documents

def ExtractINED(pathname):
    dfI=pd.read_excel(pathname,sheet_name="df_COVID_20AUG",usecols="F:AB")
    dfI=dfI.drop_duplicates()
    #dtype={'Continent':str,'Sous_Continent':str,'Pays_Ou_Entités':str,'Superficie_(En_Milliers_De_Km2)':np.float64,'Superficie_(En_Km2)':np.float64,'Population_Mi-2019_(En_Millions)':np.float64,'Population_Mi-2019':np.float64,'Taux_De_Natalite_(Pour_1_000_Habitants)':int,'Taux_De_Mortalite_(Pour_1_000_Habitants)':int,'Projection_De_La_Population_En_2050_(En_Millions)':np.float64,'Projection_De_La_Population_En_2050':np.float64,'Taux_De_Mortalite_Infantile_(Pour_1_000_Naissances)':np.float64,'Indice_Synthetique_De_Fecondite_(Enfants_Par_Femme)':np.float64,'Proportion_De_Moins_De_15_Ans_(En_%)':np.float64}
    cols=list(dfI.columns)
    cols=[cols[2]] + cols[0:2]+cols[3:]
    dfI=dfI[cols]
    dfI=dfI.reset_index()
    dfI=dfI.drop(columns=['index'])
    print(dfI.head(5))
    dicI=dfI.to_dict(orient='records')
    pays=list(dfI['Pays_Ou_Entites'])
    countries=[]
    t=Translator()
    for p in pays:
        trad=t.translate(p,src='fr',dest='en').text
        countries.append(trad)
    return dicI

def ExtractUSHopkins(pathname):
    df=pd.read_csv(pathname,sep=",")
    col=list(df.columns)
    firstDate=col.index('1/22/20')
    psI=col.index('Province_State')
    delCol=col[:psI]+col[psI+1:firstDate]
    print(delCol)
    df=df.drop(columns=delCol)
    df=df.melt(id_vars=['Province_State'],var_name="Date")
    df['value']=pd.to_numeric(df['value'])
    states=list(df['Province_State'])
    states=list(dict.fromkeys(states))
    date=list(df['Date'])
    date=list(dict.fromkeys(date))
    dic=[]
    for d in date:
        somme=df.loc[df['Date']==d,'value'].sum()
        dic.append(('United States',d,somme))
    dfUS=pd.DataFrame(dic,columns=['Country/Region','Date','value'])
    print(dfUS.head(58))
    documents=dfUS.to_dict(orient='records')
    return documents

es=Elasticsearch()

pathname = os.path.dirname(sys.argv[0])
dataPath=pathname+'/time_series_covid19_confirmed_global.csv'
dataPathDeaths=pathname+'time_series_covid19_deaths_global.csv'
dataPathI=pathname+'/df_COVID_20AUG.xlsx'
dataPathUSDeaths=pathname+'/time_series_covid19_deaths_US.csv'
dataPathUsConfirmed=pathname+'/time_series_covid19_confirmed_US.csv'

# ExtractUSHopkins(dataPathUSDeaths)
# ExtractUSHopkins(dataPathUsConfirmed)
# docCG=ExtractCSVHopkins(dataPath)
# docDeaths=ExtractCSVHopkins(dataPathDeaths)
docI=ExtractINED(dataPathI)

#helpers.bulk(es,doc,index='my-index',doc_type='_doc')

#print(documents)


#print(dicI)








