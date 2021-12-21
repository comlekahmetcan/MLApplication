#********************* Web sitesinden verileri çektiðiniz kod bölümleri**********************

###python kütüphanelerimizi ekleme iþlemleri.####
import numpy as np
import pandas as pd
import requests
###BeautifulSoup modeli ile datasetimizi oluþturma için kütüphaneyi import ettik.###
from bs4 import BeautifulSoup
###link-fiyat-key-value dizileri oluþturuldu####
urls = []
price_list = []
itemKeys = []
itemValues = []
###for döngümüzün içerisinde trendyol sitemizden laptop verilerimizi çekerek veri seti oluþturduk.###
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
###Yukarýda yaptýðýmýz iþlem linkler arasý dolaþarak get iþlemi ile laptop verilerimizi çektik###            
len(itemKeys)###itemKeys dizimizin içerisinde ki deðeri öðrendik.###
len(itemValues)###itemValues dizimizin içerisinde ki deðeri öðrendik.###
len(urls)###Burada kaç bilgisayar çýktýðýmýzý öðreniyoruz.###
###dataframemizi oluþturuyoruz(fiyat,link ve alýnan veri kadar tablo oluþturuluyor.###
dataf = pd.DataFrame()
columns = np.array(itemKeys)
columns = np.unique(columns)
dataf = pd.DataFrame(columns = columns)
dataf["url"] = urls
dataf["prices"] = price_list
###For döngümüz bir bilgisayarýn özelliklerini çekip,dataframemize yazdýrmak için kullanýldý.###
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
       
dataf.to_csv('on_isleme_oncesi.csv', index=False)###dataframeyi ön iþleme öncesi csvye yazdýrdýk.###
dataset = pd.read_csv('on_isleme_oncesi.csv')###ön iþleme için dataframemizi okuyoruz.###
dataf.to_excel('on_isleme_oncesi.xlsx', engine='xlsxwriter')###dataframemizi excel tablosuna dönüþtürdük.###

#*******************Ýlgili verileri çektikten sonra veriler üzerindeki ön iþleme adýmlarý*******************
###SimpleImputer import ederek,dataframede ki boþ deðerleri(nan)kolonda ki verilerin ortalamasý ile dolduruldu.###
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent',fill_value=None,verbose=0,copy=True,add_indicator=False,)
imputer.fit(dataf.loc[:,:])
dataf.loc[:,:] = imputer.transform(dataf.loc[:,:])


###LabelEncoder import ederek,dataframede ki kolonlarýmýzý labelencoding ile sayýsal verilere dönüþtürdük.###
from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
dataf['Arttýrýlabilir Azami Bellek:'] = enc.fit_transform(dataf['Arttýrýlabilir Azami Bellek:'])
dataf['Baðlantý Giriþleri:'] = enc.fit_transform(dataf['Baðlantý Giriþleri:'])
dataf['Baðlantýlar:'] = enc.fit_transform(dataf['Baðlantýlar:'])
dataf['Cihaz Aðýrlýðý:'] = enc.fit_transform(dataf['Cihaz Aðýrlýðý:'])
dataf['Dokunmatik Ekran:'] = enc.fit_transform(dataf['Dokunmatik Ekran:'])
dataf['Ekran Boyutu:'] = enc.fit_transform(dataf['Ekran Boyutu:'])
dataf['Ekran Kartý Bellek Tipi:'] = enc.fit_transform(dataf['Ekran Kartý Bellek Tipi:'])
dataf['Ekran Kartý Hafýzasý:'] = enc.fit_transform(dataf['Ekran Kartý Hafýzasý:'])
dataf['Ekran Kartý Tipi:'] = enc.fit_transform(dataf['Ekran Kartý Tipi:'])
dataf['Ekran Kartý:'] = enc.fit_transform(dataf['Ekran Kartý:'])
dataf['Ekran Özelliði:'] = enc.fit_transform(dataf['Ekran Özelliði:'])
dataf['Garanti Tipi:'] = enc.fit_transform(dataf['Garanti Tipi:'])
dataf['Görüntü Kalitesi:'] = enc.fit_transform(dataf['Görüntü Kalitesi:'])
dataf['HDMI:'] = enc.fit_transform(dataf['HDMI:'])
dataf['Hard Disk Kapasitesi:'] = enc.fit_transform(dataf['Hard Disk Kapasitesi:'])
dataf['Kapasite:'] = enc.fit_transform(dataf['Kapasite:'])
dataf['Klavye:'] = enc.fit_transform(dataf['Klavye:'])
dataf['Kullaným Amacý:'] = enc.fit_transform(dataf['Kullaným Amacý:'])
dataf['Optik Sürücü Tipi:'] = enc.fit_transform(dataf['Optik Sürücü Tipi:'])
dataf['Optik Sürücü:'] = enc.fit_transform(dataf['Optik Sürücü:'])
dataf['Panel Tipi:'] = enc.fit_transform(dataf['Panel Tipi:'])
dataf['Ram (Sistem Belleði):'] = enc.fit_transform(dataf['Ram (Sistem Belleði):'])
dataf['Renk:'] = enc.fit_transform(dataf['Renk:'])
dataf['SSD Kapasitesi:'] = enc.fit_transform(dataf['SSD Kapasitesi:'])
dataf['Web Color:'] = enc.fit_transform(dataf['Web Color:'])
dataf['Çözünürlük Standartý:'] = enc.fit_transform(dataf['Çözünürlük Standartý:'])
dataf['Çözünürlük:'] = enc.fit_transform(dataf['Çözünürlük:'])
dataf['Ýþlemci Frekansý:'] = enc.fit_transform(dataf['Ýþlemci Frekansý:'])
dataf['Ýþlemci Hýzý (GHz):'] = enc.fit_transform(dataf['Ýþlemci Hýzý (GHz):'])
dataf['Ýþlemci Modeli:'] = enc.fit_transform(dataf['Ýþlemci Modeli:'])
dataf['Ýþlemci Nesli:'] = enc.fit_transform(dataf['Ýþlemci Nesli:'])
dataf['Ýþlemci Tipi:'] = enc.fit_transform(dataf['Ýþlemci Tipi:'])
dataf['Ýþlemci Çekirdek Sayýsý:'] = enc.fit_transform(dataf['Ýþlemci Çekirdek Sayýsý:'])
dataf['Ýþletim Sistemi:'] = enc.fit_transform(dataf['Ýþletim Sistemi:'])
dataf['Þarjlý Kullaným Süresi:'] = enc.fit_transform(dataf['Þarjlý Kullaným Süresi:'])


dataf.drop(dataf.columns[[35]], axis=1, inplace=True)###Dataframemizde ki url kolonunu silme iþlemi.###
dataf.to_csv('on_isleme_sonrasi.csv', index=False)###Dataframemizi ön iþleme sonrasý csv dosyasýna dönüþtürdük.###
dataf.to_excel('on_isleme_sonrasi.xlsx', engine='xlsxwriter')###Dataframemizi ön iþleme sonrasý excel dosyasýna dönüþtürdük