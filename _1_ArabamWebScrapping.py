from bs4 import BeautifulSoup # type: ignore
import requests # type: ignore
import math
import pandas as pd # type: ignore
import numpy as np # type: ignore
from collections import Counter


header = {"user-agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}


class ArabamComExtractInformation():

    def __init__(self):

        self.header = {"user-agent":
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        
        self.main_page_url = "https://www.arabam.com/ikinci-el/otomobil"

        self.Arabalar = self.GuncelArabaBilgileri()

    
    def OrtakOzellikler(self, veri):

        delMotorHacimGücListe = []
        
        for arac in veri:

            aracozellikler = list(veri[arac].keys())
            if "Motor Hacmi" not in aracozellikler or "Motor Gücü" not in aracozellikler or "Renk" not in aracozellikler:
                delMotorHacimGücListe.append(arac)

        for arac in delMotorHacimGücListe:
            del veri[arac]


        liste = []

        for key in veri:
            liste.append(list(veri[key].keys()))

        tum_elemanlar = [eleman for alt_liste in liste for eleman in alt_liste]
        eleman_sayisi = Counter(tum_elemanlar)
        ortak_elemanlar = [eleman for eleman, sayi in eleman_sayisi.items() if sayi == len(liste)]

        silinecekler = []  # Silinecek öğelerin listesini tutmak için
        for arac in veri:
            aracozellikler = list(veri[arac].keys())
            
            if set(ortak_elemanlar).issubset(set(aracozellikler)):
                
                for j in aracozellikler:
                    if j not in ortak_elemanlar:
                        del veri[arac][j]
            else:        
                silinecekler.append(arac)  # Silinecek öğeleri listeye ekleyelim

        # Silinecek öğeleri döngü dışında sil
        for arac in silinecekler:
            del veri[arac]
        

    def GuncelArabaBilgileri(self):

        self.TumMarkalar = {}
        html = requests.get(self.main_page_url, headers = self.header).content
        soup = BeautifulSoup(html, "html.parser")
        div = soup.find("div", {"class": "category-facet"}).find_all("a")

        for i in div[1:]:

            marka = i.text.strip().split("\n")[0].replace("\r", "")
            linkmarka = [marka.lower().replace(" ", "-") if "-" not in marka else marka.lower().replace(" ", "")][0]
            arabasayisi = int(i.text.strip().split("\n")[-1].replace(".", "").strip())
            link = "https://www.arabam.com/" + i["href"] + "?take=50"

            self.TumMarkalar[marka] = {"arabasayisi": arabasayisi, "linkmarka": linkmarka, "link": link}

        return self.TumMarkalar
    

    def TekAracBilgiCikar(self, url):

        ozellikler = {}
        html = requests.get(url, headers = self.header).content
        soup = BeautifulSoup(html, "html.parser")

        adresbilgisi = soup.find("div", {"class": "product-info-container"}).text.strip().split("\n")[-1]
        fiyat_div = soup.find("div", {"class": "product-price"})
        if fiyat_div.find("div", {"class":"price-discount"}):
            fiyat = [i for i in fiyat_div.text.split("\n") if "TL" in i][1].strip().replace(".", "").replace("TL", "")
        else:
            fiyat = fiyat_div.text.strip().replace(".", "").replace("TL", "")
        # aciklama = soup.find("div", {"class": "tab-description"}).text.replace("Açıklama", "").lstrip()


        ozellikler["Adress"]   =  adresbilgisi
        ozellikler["Fiyat"]    =  fiyat
        # ozellikler["Açıklama"] =  aciklama
        ozellik_divs = soup.find_all("div", {"class": "property-item"})[2:]

        for i in ozellik_divs:

            anahtar = i.find("div", {"class": "property-key"}).text.strip()
            deger = i.find("div", {"class": "property-value"}).text.strip()

            ozellikler[anahtar] = deger

        return ozellikler
    

    def TekMarkaTumAraclar(self, marka):

        self.MarkaAracBilgileri = {}
        aracsayisi = self.Arabalar[marka]["arabasayisi"]
        aracadi = self.Arabalar[marka]["linkmarka"]

        # if aracsayisi < 1000:
        #     return
        # else:
        #     print(aracadi)

        if aracsayisi < 2500:

            sayfasaysi = math.ceil(aracsayisi / 50) 
            toplambilgialinanarac = 0
            key_number = 1

            for sayfa in range(1, sayfasaysi+1):

                new_url = self.Arabalar[marka]["link"] + f"&page={str(sayfa)}"
                new_html = requests.get(new_url, headers = self.header).content
                new_soup = BeautifulSoup(new_html, "html.parser")

                car_url_tr = new_soup.find_all("tr", {"class": "listing-list-item should-hover bg-white"})

                 
                for a in car_url_tr:

                    car_link = "https://www.arabam.com/" + a.find("a")["href"]
                    key_value = f"{marka}_{str(key_number)}"
                    self.MarkaAracBilgileri[key_value] = self.TekAracBilgiCikar(car_link)
                    toplambilgialinanarac +=1
                    key_number +=1
                    if key_number%50==0:
                        print(key_number)

        else:

            new_link_list = []
            new_url = self.Arabalar[marka]["link"]
            new_html = requests.get(new_url, headers = self.header).content
            new_soup = BeautifulSoup(new_html, "html.parser")

            div = new_soup.find("div", {"class": "category-facet"}).find_all("a")

            for i in div[2:]:

                link = "https://www.arabam.com/" + i["href"] + "?take=50"
                arabasayisi = int(i.text.strip().split("\n")[-1].replace(".", "").strip())

                new_link_list.append((link, arabasayisi))

            
            toplambilgialinanarac = 0
            key_number = 1

            for car in new_link_list:

                link = car[0]
                aracsayisi = car[1]

                sayfasaysi = math.ceil(aracsayisi / 50) 


                for sayfa in range(1, sayfasaysi+1):

                    new_url = link + f"&page={str(sayfa)}"
                    new_html = requests.get(new_url, headers = self.header).content
                    new_soup = BeautifulSoup(new_html, "html.parser")

                    car_url_tr = new_soup.find_all("tr", {"class": "listing-list-item should-hover bg-white"})

                    for a in car_url_tr:

                        car_link = "https://www.arabam.com/" + a.find("a")["href"]
                        key_value = f"{marka}_{str(key_number)}"
                        self.MarkaAracBilgileri[key_value] = self.TekAracBilgiCikar(car_link)
                        toplambilgialinanarac +=1
                        key_number +=1
                        if key_number%50==0:
                            print(key_number)

        self.OrtakOzellikler(self.MarkaAracBilgileri)

        rows = list(self.MarkaAracBilgileri.keys())

        arac = rows[0]
        cols = list(self.MarkaAracBilgileri[arac].keys())

        df = pd.DataFrame(index = rows, columns=cols)

        for row in df.index:

            df.loc[row] = list(self.MarkaAracBilgileri[row].values())

        df.to_excel(f"OriginalDatas/{arac}.xlsx")

        return self.MarkaAracBilgileri


m1 = ArabamComExtractInformation()
# result = m1.TekMarkaTumAraclar("Daewoo")
result = m1.TekMarkaTumAraclar("Cupra")

# for i in list(m1.Arabalar.keys()):
#     result = m1.TekMarkaTumAraclar(i)