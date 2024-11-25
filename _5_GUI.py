import tkinter
from tkinter import ttk
import pandas as pd
import numpy as np
import pickle
import os
from _3_ANNStructure import Layer, FCLayer, ActivationLayer
import matplotlib.pyplot as plt
import matplotlib.gridspec as gr
from sklearn.metrics import r2_score


dosya_isimleri = os.listdir('TrainingModels')
TrainingModels = []

for dosya_adi in dosya_isimleri:
    TrainingModels.append(dosya_adi)



class MainScreen():
    
    def __init__(self):

        self.root = tkinter.Tk()

        self.root.title("GİRİŞ EKRANI")
        self.root.geometry("500x800+0+0")
        self.root.config(bg = "teal")

        self.generateLabel(self.root, "İKİNCİ EL ARABA FİYAT TAHMİN MODELİ","teal", ("Cambria 18 bold"), 20,20)

        self.generateLabel(self.root, "MODEL SEÇİMİ", "teal", ("calibri 14 bold"), 15, 75)
        
        self.ComboBoxTrainingModel = self.generateCombobox(self.root, 35, ("calibri 12 bold"), 150,75)
        self.ComboBoxTrainingModel["values"] = TrainingModels
        self.ComboBoxTrainingModel.set(TrainingModels[0])


        self.ButtonModel = tkinter.Button(self.root, text="Model Uygula", bg="black",
                                            fg="white", width=14, font = ("arial 13 bold"),
                                            command=lambda:[self.ButtonModelUygula()])
        
        self.ButtonModel.pack()
        self.ButtonModel.place(x = 300, y = 110)

        yatay_cizgi = tkinter.Frame(self.root, height=1, width=470, bg="black")
        yatay_cizgi.pack() 
        yatay_cizgi.place(x = 15, y = 160)

        #--------------------------------------------------------
        #--------------------------------------------------------


        self.FrameResult = tkinter.Frame(self.root, height=600, width=470, background="white", 
                                         highlightbackground="black", highlightcolor="blue", highlightthickness=3)        
        self.FrameResult.pack() 
        self.FrameResult.place(x = 15, y = 175)





        self.root.mainloop()


    def ButtonModelUygula(self):

        plt.close()

        for widget in self.FrameResult.winfo_children():
            widget.destroy()

        model = self.ComboBoxTrainingModel.get()
        model = "TrainingModels/" + model

        with open(model, 'rb') as f:
            self.TrainingModel = pickle.load(f) # deserialize using load()

        
        self.ModelAttributes = self.TrainingModel[-1]
        dfmin = self.ModelAttributes["dfmin"]
        dfmax = self.ModelAttributes["dfmax"]
        AllColumns = self.ModelAttributes["allColumns"]
        StringColumns = list(self.ModelAttributes["StringColumns"].keys())
        OriginalData = self.ModelAttributes["df"]


        y = 10
        for stringcol in StringColumns:
            self.generateLabel(self.FrameResult, stringcol+":", "white", ("calibri 14 bold"), 15, y)
            y+=40

        for col in AllColumns:

            if col not in StringColumns:
                self.generateLabel(self.FrameResult, col+":", "white", ("calibri 14 bold"), 15, y)
                y+=40


        self.ComboBoxAdres = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,10)
        self.ComboBoxAdres["values"] = list(self.ModelAttributes["StringColumns"]["Adress"])
        self.ComboBoxAdres.set(list(self.ModelAttributes["StringColumns"]["Adress"])[0])
      

        self.ComboBoxSeri = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,50)
        self.ComboBoxSeri["values"] = list(self.ModelAttributes["StringColumns"]["Seri"])
        self.ComboBoxSeri.set(list(self.ModelAttributes["StringColumns"]["Seri"])[0])

        self.ComboBoxModel = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,90)
        self.ComboBoxModel["values"] = list(self.ModelAttributes["StringColumns"]["Model"])
        self.ComboBoxModel.set(list(self.ModelAttributes["StringColumns"]["Model"])[0])


        self.ComboBoxVites = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,130)
        self.ComboBoxVites["values"] = list(self.ModelAttributes["StringColumns"]["Vites Tipi"])
        self.ComboBoxVites.set(list(self.ModelAttributes["StringColumns"]["Vites Tipi"])[0])

        self.ComboBoxYakit = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,170)
        self.ComboBoxYakit["values"] = list(self.ModelAttributes["StringColumns"]["Yakıt Tipi"])
        self.ComboBoxYakit.set(list(self.ModelAttributes["StringColumns"]["Yakıt Tipi"])[0])

        self.ComboBoxRenk = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,210)
        self.ComboBoxRenk["values"] = list(self.ModelAttributes["StringColumns"]["Renk"])
        self.ComboBoxRenk.set(list(self.ModelAttributes["StringColumns"]["Renk"])[0])

        self.ComboBoxBoyaDegisen = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,250)
        self.ComboBoxBoyaDegisen["values"] = list(self.ModelAttributes["StringColumns"]["Boya-değişen"])
        self.ComboBoxBoyaDegisen.set(list(self.ModelAttributes["StringColumns"]["Boya-değişen"])[0])


        self.ComboBoxKimden = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,290)
        self.ComboBoxKimden["values"] = list(self.ModelAttributes["StringColumns"]["Kimden"])
        self.ComboBoxKimden.set(list(self.ModelAttributes["StringColumns"]["Kimden"])[0])


        yillar = list(range(int(dfmin["Yıl"]), int(dfmax["Yıl"])+1))
        self.ComboBoxYil = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,330)
        self.ComboBoxYil["values"] = yillar
        self.ComboBoxYil.set(yillar[0])

        KM = list(range(0, int(dfmax["Kilometre"])+1, 10000))
        self.ComboBoxKM = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,370)
        self.ComboBoxKM["values"] = KM
        self.ComboBoxKM.set(KM[1])

        MotorHacim = list(range(int(dfmin["Motor Hacmi"]), int(dfmax["Motor Hacmi"])+1))
        self.ComboBoxMotorHacim = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,410)
        self.ComboBoxMotorHacim["values"] = MotorHacim
        self.ComboBoxMotorHacim.set(MotorHacim[1])

        MotorGüc = list(range(int(dfmin["Motor Gücü"]), int(dfmax["Motor Gücü"])+1))
        self.ComboBoxMotorGüc = self.generateCombobox(self.FrameResult, 32, ("calibri 12 bold"), 152,450)
        self.ComboBoxMotorGüc["values"] = MotorGüc
        self.ComboBoxMotorGüc.set(MotorGüc[1])


        self.ButtonPredict = tkinter.Button(self.FrameResult, text="Tahmin", bg="black",
                                            fg="white", width=14, font = ("arial 13 bold"),
                                            command=lambda:[self.predict()])
        
        self.ButtonPredict.pack()
        self.ButtonPredict.place(x = 280, y = 490)


        self.generateLabel(self.FrameResult, "TAHMİN SONUCU",  "white", ("calibri 16 bold"), 15, 540, fg="red")
        self.EntryPredictResult = tkinter.Entry(self.FrameResult, width=21, font=("cambira 15"), 
                                                highlightbackground="red", highlightthickness=2)
        self.EntryPredictResult.pack()
        self.EntryPredictResult.place(x = 190, y = 540)
        self.EntryPredictResult.config(state="disabled")

        self.Graphics()

    def predict(self):

        self.EntryPredictResult.config(state="normal")
        self.EntryPredictResult.delete(0, tkinter.END)
        self.EntryPredictResult.config(state="disabled")

        dfmin = self.ModelAttributes["dfmin"]
        dfmax = self.ModelAttributes["dfmax"]


        df = pd.DataFrame(index = ["Original", "Standart"], columns=self.ModelAttributes["CategoricalColumnsValues"])
        
        IntegerValues = {"Yıl": int(self.ComboBoxYil.get()),
                         "Kilometre": int(self.ComboBoxKM.get()),
                         "Motor Hacmi": int(self.ComboBoxMotorHacim.get()),
                         "Motor Gücü": int(self.ComboBoxMotorGüc.get())}
        
        Adres = self.ComboBoxAdres.get()
        Seri = self.ComboBoxSeri.get()
        Model = self.ComboBoxModel.get()
        Vites = self.ComboBoxVites.get()
        Yakıt = self.ComboBoxYakit.get()
        Renk = self.ComboBoxRenk.get()
        BoyaDegisen = self.ComboBoxBoyaDegisen.get()
        Kimden = self.ComboBoxKimden.get()
        
        StringVaues = [f"Adress_{Adres}", f"Seri_{Seri}", f"Model_{Model}", f"Vites Tipi_{Vites}", 
                       f"Yakıt Tipi_{Yakıt}",f"Renk_{Renk}",f"Boya-değişen_{BoyaDegisen}", 
                       f"Kimden_{Kimden}"]

        for i in IntegerValues.keys():
            df.loc["Original",i] = IntegerValues[i]
        

        for i in StringVaues:
            df.loc["Original",i] = i


        for col in df.columns:

            X = df.loc["Original", col]
            
            if type(X) == int:
                 df.loc["Standart", col] = (X - dfmin[col]) / (dfmax[col] - dfmin[col])
            elif type(X) == str:
                df.loc["Standart", col] = 1
        
        df.fillna(0, inplace=True)

        

        input = np.array(list(df.loc["Standart"])).reshape(1,df.shape[1])

        output = input
        
        for layer in range(len(self.TrainingModel) - 1):
            output = self.TrainingModel[layer].forward_propagation(output)
        
        output = output[0][0]
        MaxPrice = dfmax["Fiyat"]
        MinPrice = dfmin["Fiyat"]

        OriginalOutput = output * (MaxPrice - MinPrice) + MinPrice
        

        AfterDot = str(OriginalOutput).split(".")[1][0:3]
        PreDot = str(OriginalOutput).split(".")[0]

        Value = ""

        i = 1
        for char in reversed(PreDot):
            if i%4 != 0:
                Value = char + Value
                i+=1
            else:
                Value = char + "." + Value
                i+=2

        PredictedValue = Value + "," + AfterDot
            

        self.EntryPredictResult.config(state="normal")
        self.EntryPredictResult.insert(0, PredictedValue)
        self.EntryPredictResult.config(state="disabled")

    
    def Graphics(self):

        df = self.ModelAttributes["df"]
        errors = self.ModelAttributes["Err"]
        test_errors = self.ModelAttributes["TestErr"]
        accuracy = self.ModelAttributes["r2"]

        PredictedValuesDf = self.ModelAttributes["PredictedDf"]

        PredictedValuesSampleDf = PredictedValuesDf[['Real', 'Predicted']].sample(n=50)
        RealValuesSeries = PredictedValuesSampleDf["Real"].values
        PredictedValuesSeries = PredictedValuesSampleDf["Predicted"].values


        fig = plt.figure(figsize = (10,8))
        gs = gr.GridSpec(3,3)
        ax1 = plt.subplot(gs[0,0])
        ax2 = plt.subplot(gs[0,1])
        ax2_1 = plt.subplot(gs[0,2])
        ax3 = plt.subplot(gs[1,0]) 
        ax4 = plt.subplot(gs[1,1]) 
        ax5 = plt.subplot(gs[1,2])
        ax6 = plt.subplot(gs[2,0])
        ax7 = plt.subplot(gs[2,1])
        ax8 = plt.subplot(gs[2,2])
        

        ax1.plot(errors, "b", label = "Train")
        ax1.plot(test_errors, "r", label = "Test")
        ax1.set_xlabel("EPOCS")
        ax1.set_ylabel("Error")
        ax1.set_title("Error Graph", fontweight = "bold")
        ax1.legend()


        r2 = r2_score(PredictedValuesDf["Real"].values,
                       PredictedValuesDf["Predicted"].values)
        
        ax2.plot(RealValuesSeries, "r-", linewidth = 1, label = "Real")
        ax2.plot(PredictedValuesSeries, "b-", linewidth = 1, label = "Predicted")
        ax2.set_xlabel("Cars")
        ax2.set_ylabel("Normalized Price")
        ax2.set_title(f"Real vs Predicted Values r2: {round(r2,2)}", fontweight = "bold")
        ax2.set_xlim(xmin = 0)
        ax2.legend(loc = 1)

        ax2_1.plot(accuracy, "b", label = "Test Accuracy")
        ax2_1.set_xlabel("EPOCS")
        ax2_1.set_ylabel("Accuracy")
        ax2_1.set_title("Accuracy Graph", fontweight = "bold")
        ax2_1.legend()

        value_counts = df['Yakıt Tipi'].value_counts()
        labels = value_counts.index
        sizes = value_counts.values
        ax3.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax3.set_title('Yakıt Tipi', fontweight = "bold")
        ax3.axis('equal')  # Daireyi tam bir daire olarak ayarla

        value_counts = df['Adress'].value_counts().head(7)
        labels = list(value_counts.index)
        sizes = list(value_counts.values)
        ax4.bar(labels, sizes, color ='maroon', 
        width = 0.4)
        ax4.set_title('Şehir Dağılımı', fontweight = "bold")
        ax4.set_xticklabels(labels, rotation=90)

        value_counts = df['Kimden'].value_counts()
        labels = value_counts.index
        sizes = value_counts.values
        ax5.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax5.set_title('Kimden', fontweight = "bold")
        ax5.axis('equal')  # Daireyi tam bir daire olarak ayarla

        value_counts = df['Vites Tipi'].value_counts()
        labels = value_counts.index
        sizes = value_counts.values
        ax6.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        ax6.set_title('Vites Tipi', fontweight = "bold")
        ax6.axis('equal')  # Daireyi tam bir daire olarak ayarla

        value_counts = df['Seri'].value_counts().head(5)
        labels = list(value_counts.index)
        sizes = list(value_counts.values)
        ax7.bar(labels, sizes, color ='maroon', 
        width = 0.4)
        ax7.set_title('Seri', fontweight = "bold")
        ax7.set_xticklabels(labels, rotation=90)

        value_counts = df['Renk'].value_counts().head(10)
        labels = list(value_counts.index)
        sizes = list(value_counts.values)
        ax8.bar(labels, sizes, color ='teal', 
        width = 0.4)
        ax8.set_title('Renk', fontweight = "bold")
        ax8.set_xticklabels(labels, rotation=90)


        plt.tight_layout()
        plt.show()


    def generateEntry(self, main,width, x, y, tv = None):
        text = tkinter.Entry(main, width=width, font=("cambira 12"), textvariable=tv)
        text.pack()
        text.place(x = x, y = y)
        return text

    def generateSpin(self, main, from_, to, width, values, font, x,y):
        spin =  ttk.Spinbox(main, from_=from_,  to=to, width=width, values= values,  font = font)
        spin.pack()
        spin.set(3)
        spin.place(x = x, y = y)

        return spin

    def generateLabel(self, main, text, bg, font, x, y, fg = "black", width = None):
        label = ttk.Label(main, text = text, background=bg, font = font, foreground= fg, width=width)
        label.pack()
        label.place(x = x, y = y)
        return label

    def generateCombobox(self, main, width, font, x, y):
        players_list = ttk.Combobox(main, width=width, font = font)
        players_list.pack()
        players_list.place(x = x, y = y)

        return players_list

    def generateButton(self, main, text, bg, fg, width, font, x, y):
        girisbutonu = tkinter.Button(main, text=text, bg=bg,fg=fg, width=width, font = font)                                  
        girisbutonu.pack()
        girisbutonu.place(x = x, y = y)

        return girisbutonu







        

        


    


       

        









        



        


        








        






MainScreen()

