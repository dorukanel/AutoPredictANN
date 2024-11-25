from _3_ANNStructure import FCLayer, ActivationLayer, Network, sigmoid, sigmoid_prime,mse, mse_prime
from _2_DataPreProcessing import DataPreProcessing
from sklearn.metrics import r2_score
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt


car = "Honda"


dfmins, dfmaks, All_Columns, StringColumnsValues, CategoricalColumnValues, df = DataPreProcessing(car)
OtherModelAttributes = {"dfmin": dfmins, "dfmax": dfmaks,"allColumns": All_Columns,"StringColumns": StringColumnsValues, "CategoricalColumnsValues": CategoricalColumnValues, "df": df}

Data = pd.read_excel(f"ProcessedDatas/{car}.xlsx", index_col="Indeks")

X = Data.iloc[:, :-1].values.reshape(Data.shape[0],1, Data.shape[1]-1)
y = Data.iloc[:, -1].values.reshape(Data.shape[0],1, 1)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


net = Network()
LayerNeuronInfo = [15]
epochs = 250
learning_rate = 0.4


def Training(X_Values,  activation, activation_rpime,e, lr, LayerNeuronInfo = [20]):

    for i in range(len(LayerNeuronInfo)):

        if i == 0:
            net.add(FCLayer(X_Values.shape[2], LayerNeuronInfo[i]))
            net.add(ActivationLayer(activation, activation_rpime))
        else:
            net.add(FCLayer(LayerNeuronInfo[i-1], LayerNeuronInfo[i]))
            net.add(ActivationLayer(activation, activation_rpime))

    net.add(FCLayer(LayerNeuronInfo[i], 1))
    net.add(ActivationLayer(activation, activation_rpime))

    net.use(mse, mse_prime)
    net.fit(X_train, y_train, X_test, y_test, epochs=e, learning_rate=lr)



Training(X, sigmoid, sigmoid_prime, epochs, learning_rate, LayerNeuronInfo)

y_real = [x[0] for x in y_test.reshape(y_test.shape[0],1)]
y_predicted = net.predict(X_test)
r2 = r2_score(y_real, y_predicted)

df = pd.DataFrame(columns = ["Real", "Predicted"])
df["Real"] = y_real
df["Predicted"] = y_predicted
df.to_excel(f"PredictedValues/{car}_{epochs}_{round(r2,2)}.xlsx")

ModelName = f"TrainingModels/{car}_"

for i in LayerNeuronInfo:
    ModelName += str(i)
    ModelName += "_"


ModelName += f"epoc-[{epochs}]_"
ModelName += "r2-[{}]".format(str(round(r2,2)).split(".")[-1])

ModelName +=".pkl"

OtherModelAttributes["PredictedDf"]=df
OtherModelAttributes["Err"] = net.err_list
OtherModelAttributes["TestErr"] = net.test_err_list
OtherModelAttributes["r2"] = net.r2


net.layers.append(OtherModelAttributes)

with open(ModelName, 'wb') as f:  # open a text file
    pickle.dump(net.layers, f) # serialize the list
