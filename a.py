#********************* Web sitesinden verileri �ekti�iniz kod b�l�mleri**********************

###python k�t�phanelerimizi ekleme i�lemleri.####
import numpy as np
import pandas as pd
import requests
###BeautifulSoup modeli ile datasetimizi olu�turma i�in k�t�phaneyi import ettik.###
from bs4 import BeautifulSoup
###link-fiyat-key-value dizileri olu�turuldu####
urls = []
price_list = []
itemKeys = []
itemValues = []
###for d�ng�m�z�n i�erisinde trendyol sitemizden laptop verilerimizi �ekerek veri seti olu�turduk.###
for i in range(1,30):
    url = "https://www.trendyol.com/laptop?pi=" + str(i)
    r = requests.get(url)
    source = BeautifulSoup(r.content,"lxml")
       
    prices = source.find_all("div",attrs={"class":"prc-box-sllng"})  
    for price in prices:
        price_list.append(price.text)
        
    comps = source.find_all("div",attrs={"class":"p-card-chldrn-cntnr"})
    for comp in comps:
        url_comps = "https://www.trendyol.com/"+comp.a.get("href")
        urls.append(url_comps)
        
        r_comp = requests.get(url_comps)
        source_laptop = BeautifulSoup(r_comp.content,"lxml")
        
        laptop_Keys = source_laptop.find_all("div",attrs={"class":"item-key"})
        for laptop_Key in laptop_Keys:
            itemKeys.append(laptop_Key.text)
        
        laptop_Values = source_laptop.find_all("div",attrs={"class":"item-value"})
        for laptop_Value in laptop_Values:
            itemValues.append(laptop_Value.text)
###Yukar�da yapt���m�z i�lem linkler aras� dola�arak get i�lemi ile laptop verilerimizi �ektik###            
len(itemKeys)###itemKeys dizimizin i�erisinde ki de�eri ��rendik.###
len(itemValues)###itemValues dizimizin i�erisinde ki de�eri ��rendik.###
len(urls)###Burada ka� bilgisayar ��kt���m�z� ��reniyoruz.###
###dataframemizi olu�turuyoruz(fiyat,link ve al�nan veri kadar tablo olu�turuluyor.###
dataf = pd.DataFrame()
columns = np.array(itemKeys)
columns = np.unique(columns)
dataf = pd.DataFrame(columns = columns)
dataf["url"] = urls
dataf["prices"] = price_list
###For d�ng�m�z bir bilgisayar�n �zelliklerini �ekip,dataframemize yazd�rmak i�in kullan�ld�.###
for i in range(0,695):
    url = dataf['url'].loc[i]
    r = requests.get(url)
    source = BeautifulSoup(r.content,"lxml")
    
    properties = source.find_all("div",attrs={"class":"prop-item"})
    for prop in properties:
        prop_title = prop.find("div",attrs={"class":"item-key"}).text
        prop_value = prop.find("div",attrs={"class":"item-value"}).text
        print(prop_title+prop_value)
        dataf[prop_title].loc[i] = prop_value   
       
dataf.to_csv('on_isleme_oncesi.csv', index=False)###dataframeyi �n i�leme �ncesi csvye yazd�rd�k.###
dataset = pd.read_csv('on_isleme_oncesi.csv')###�n i�leme i�in dataframemizi okuyoruz.###
dataf.to_excel('on_isleme_oncesi.xlsx', engine='xlsxwriter')###dataframemizi excel tablosuna d�n��t�rd�k.###

#*******************�lgili verileri �ektikten sonra veriler �zerindeki �n i�leme ad�mlar�*******************
###SimpleImputer import ederek,dataframede ki bo� de�erleri(nan)kolonda ki verilerin ortalamas� ile dolduruldu.###
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent',fill_value=None,verbose=0,copy=True,add_indicator=False,)
imputer.fit(dataf.loc[:,:])
dataf.loc[:,:] = imputer.transform(dataf.loc[:,:])


###LabelEncoder import ederek,dataframede ki kolonlar�m�z� labelencoding ile say�sal verilere d�n��t�rd�k.###
from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
dataf['Artt�r�labilir Azami Bellek:'] = enc.fit_transform(dataf['Artt�r�labilir Azami Bellek:'])
dataf['Ba�lant� Giri�leri:'] = enc.fit_transform(dataf['Ba�lant� Giri�leri:'])
dataf['Ba�lant�lar:'] = enc.fit_transform(dataf['Ba�lant�lar:'])
dataf['Cihaz A��rl���:'] = enc.fit_transform(dataf['Cihaz A��rl���:'])
dataf['Dokunmatik Ekran:'] = enc.fit_transform(dataf['Dokunmatik Ekran:'])
dataf['Ekran Boyutu:'] = enc.fit_transform(dataf['Ekran Boyutu:'])
dataf['Ekran Kart� Bellek Tipi:'] = enc.fit_transform(dataf['Ekran Kart� Bellek Tipi:'])
dataf['Ekran Kart� Haf�zas�:'] = enc.fit_transform(dataf['Ekran Kart� Haf�zas�:'])
dataf['Ekran Kart� Tipi:'] = enc.fit_transform(dataf['Ekran Kart� Tipi:'])
dataf['Ekran Kart�:'] = enc.fit_transform(dataf['Ekran Kart�:'])
dataf['Ekran �zelli�i:'] = enc.fit_transform(dataf['Ekran �zelli�i:'])
dataf['Garanti Tipi:'] = enc.fit_transform(dataf['Garanti Tipi:'])
dataf['G�r�nt� Kalitesi:'] = enc.fit_transform(dataf['G�r�nt� Kalitesi:'])
dataf['HDMI:'] = enc.fit_transform(dataf['HDMI:'])
dataf['Hard Disk Kapasitesi:'] = enc.fit_transform(dataf['Hard Disk Kapasitesi:'])
dataf['Kapasite:'] = enc.fit_transform(dataf['Kapasite:'])
dataf['Klavye:'] = enc.fit_transform(dataf['Klavye:'])
dataf['Kullan�m Amac�:'] = enc.fit_transform(dataf['Kullan�m Amac�:'])
dataf['Optik S�r�c� Tipi:'] = enc.fit_transform(dataf['Optik S�r�c� Tipi:'])
dataf['Optik S�r�c�:'] = enc.fit_transform(dataf['Optik S�r�c�:'])
dataf['Panel Tipi:'] = enc.fit_transform(dataf['Panel Tipi:'])
dataf['Ram (Sistem Belle�i):'] = enc.fit_transform(dataf['Ram (Sistem Belle�i):'])
dataf['Renk:'] = enc.fit_transform(dataf['Renk:'])
dataf['SSD Kapasitesi:'] = enc.fit_transform(dataf['SSD Kapasitesi:'])
dataf['Web Color:'] = enc.fit_transform(dataf['Web Color:'])
dataf['��z�n�rl�k Standart�:'] = enc.fit_transform(dataf['��z�n�rl�k Standart�:'])
dataf['��z�n�rl�k:'] = enc.fit_transform(dataf['��z�n�rl�k:'])
dataf['��lemci Frekans�:'] = enc.fit_transform(dataf['��lemci Frekans�:'])
dataf['��lemci H�z� (GHz):'] = enc.fit_transform(dataf['��lemci H�z� (GHz):'])
dataf['��lemci Modeli:'] = enc.fit_transform(dataf['��lemci Modeli:'])
dataf['��lemci Nesli:'] = enc.fit_transform(dataf['��lemci Nesli:'])
dataf['��lemci Tipi:'] = enc.fit_transform(dataf['��lemci Tipi:'])
dataf['��lemci �ekirdek Say�s�:'] = enc.fit_transform(dataf['��lemci �ekirdek Say�s�:'])
dataf['��letim Sistemi:'] = enc.fit_transform(dataf['��letim Sistemi:'])
dataf['�arjl� Kullan�m S�resi:'] = enc.fit_transform(dataf['�arjl� Kullan�m S�resi:'])


dataf.drop(dataf.columns[[35]], axis=1, inplace=True)###Dataframemizde ki url kolonunu silme i�lemi.###
dataf.to_csv('on_isleme_sonrasi.csv', index=False)###Dataframemizi �n i�leme sonras� csv dosyas�na d�n��t�rd�k.###
dataf.to_excel('on_isleme_sonrasi.xlsx', engine='xlsxwriter')###Dataframemizi �n i�leme sonras� excel dosyas�na d�n��t�rd�k