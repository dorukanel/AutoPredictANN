import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Car = "Cupra"

def DataPreProcessing(car):

    df = pd.read_excel(f"OriginalDatas/{car}_1.xlsx")
    df = df.rename(columns={'Unnamed: 0': 'Indeks'})
    df.set_index("Indeks", inplace=True)

    deleted_columns = ["Marka", "Kasa Tipi", "Çekiş", "Yakıt Deposu", "Araç Durumu"]
    for col in deleted_columns:
        if col in df.columns:
            del df[col]

    df = df[df.apply(lambda row: "-" not in row.values, axis=1)]

    # Adres sütununun düzenlenmesi
    rows_to_delete = df[df['Adress'].str.contains(',') == False]
    df = df.drop(rows_to_delete.index)
    df["Adress"] = df['Adress'].apply(lambda x: x.split(',')[1].replace(" ", ""))
        
    # KM ve Yıl sütunlarının düzenlenmesi
    df["Kilometre"] = df['Kilometre'].str.replace(".", "", regex=True).str.split(" ").str[0]
    df['Kilometre'] = pd.to_numeric(df['Kilometre'], errors='coerce')
    df['Yıl'] = pd.to_numeric(df['Yıl'], errors='coerce')
    df['Fiyat'] = pd.to_numeric(df['Fiyat'], errors='coerce')

    # Motor hacmi sütununun düzenlenmesi
    df = df[df['Motor Hacmi'].str.contains('CC|cc|cm|CM')]
    df["Motor Hacmi"] = df['Motor Hacmi'].str.split(" ").str[0]
    df['Motor Hacmi'] = pd.to_numeric(df['Motor Hacmi'], errors='coerce')

    # Motor Gücü değişkeninin düzenlenmesi
    df = df[df['Motor Gücü'].str.contains('HP|hp|Hp')]
    df["Motor Gücü"] = df['Motor Gücü'].str.split(" ").str[0]
    df['Motor Gücü'] = pd.to_numeric(df['Motor Gücü'], errors='coerce')

    df.dropna() # Nul verilerin silinmesi


    df_original = df.copy(deep=True)

    # Arayüz için tüm sütunların ve string veri içeren sütunların çekilmesi

    All_Columns = ['Adress', 'Seri', 'Model', 'Yıl', 'Kilometre', 'Vites Tipi', 'Yakıt Tipi', 'Renk', 'Motor Hacmi', 'Motor Gücü', 'Boya-değişen', 'Kimden', 'Fiyat']
    StringColumns = ['Adress', 'Seri', 'Model', 'Vites Tipi', 'Yakıt Tipi', 'Renk', 'Boya-değişen', 'Kimden']
    IntegerColumns = ['Yıl', 'Kilometre', 'Motor Hacmi', 'Motor Gücü', 'Fiyat']

    StringColumnsValues = {}

    for col in StringColumns:
        StringColumnsValues[col] = set(list(df[col]))


    # Kategorik veriler için Dummy değişkenlerin oluşturulması  
    df = pd.get_dummies(df, columns=StringColumns)


    # Her bir Integer sütun için min ve max değerlerin elde edilmesi / dönüşüm işlemleri için
    
    dfmins = df[IntegerColumns].min()
    dfmaks = df[IntegerColumns].max()


    # Integer olan sütunların standardize edilmesi
    scaler = MinMaxScaler()
    df[IntegerColumns] = scaler.fit_transform(df[IntegerColumns])


    # Benzer verilerin silinmesi
    duplicate_subset = df.iloc[:, :-1]
    duplicate_rows = df[duplicate_subset.duplicated()]

    if not duplicate_rows.empty:
        df = df.drop_duplicates(subset=duplicate_subset.columns, keep=False)

    
    # Fiyat sütununun son sütuna alınması
    price_col = df.pop('Fiyat')  
    df.insert(len(df.columns), 'Fiyat', price_col)  
    

    CategoricalColumnValues = list(df.columns)[0:-1]

    # Verisetinin son halinin kaydedilmesi
    df.to_excel(f"ProcessedDatas/{car}.xlsx")


    return dfmins, dfmaks, All_Columns[0:-1], StringColumnsValues, CategoricalColumnValues, df_original


# DataPreProcessing(Car)
