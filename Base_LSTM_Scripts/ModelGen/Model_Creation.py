###   Model creation

from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam


from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout

import tensorflow as tf
from tensorflow import keras
from tensorflow.python.keras.layers.core import Activation




keras.backend.clear_session()  # Reseteo sencillo

#---------Layes are created

n_future = 1   # Number of units(day, min, hour, etc..) we want to look into the future based on the past days.
n_past =5
OneColum=False


if OneColum:
    Columns_N=7
    modelPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/OnlyCloseColum/Model/Models_fewColums/Model_LSTM_DayMonth5BackDlastFFTCloseValum150FFT400units1e-6"
else:
    modelPath="FFT_added_LSTM_All_In_Close_Out_all_relu_added_HG_X/ModelGen/High_Low_Close/Model/Models_fewColums/Model_LSTM_DayMonth5BackDlastFFTCloseValum150FFT400units1e-6"
    Columns_N=9

inputs=keras.Input(shape=(n_past,Columns_N))


LSTM_Layer1=keras.layers.LSTM(n_past, input_shape=(n_past,Columns_N), return_sequences=True,activation='PReLU')(inputs)

Dropout_layer2=keras.layers.Dropout(0.6)(LSTM_Layer1)# modify
#x=Dropout_layer1=keras.layers.Dropout(0.2)(x)
LSTM_Layer2=keras.layers.LSTM(400, return_sequences=False)(Dropout_layer2)

Dropout_layer3=keras.layers.Dropout(0.6)(LSTM_Layer2)# modify


#---------------------------Outputs
dense=keras.layers.Dense(1)(Dropout_layer3)



#-------Layers outputs are linked

outputs=dense




#-----The model it's created
outputArray=[outputs]

model=keras.Model(inputs=inputs, outputs=outputArray, name='Prices_Forcasting_LSTM_FFT')
#model=keras.Model(inputs=[inputs,None], outputs=[outputs,outputs2,outputs3,outputs4,outputs5,outputs6], name='Prices_Prediction')

#keras.utils.plot_model(model, "my_first_model_with_shape_info.png", show_shapes=True)


#------------------- Loss and optimizer ----------------------------------------
#got to ensure MeanAbsoluteError it's the good one for our data
loss = keras.losses.MeanSquaredError(reduction="auto", name="mean_squared_error")

#optim=keras.optimizers.Adam(1e-3)
optim=keras.optimizers.Adam(1e-6)
Metrics=["mean_squared_error"]

losses={
    "dense": loss
}

#model.compile(loss=losses, optimizer=optim, metrics=Metrics)
model.compile(loss=losses, optimizer=optim,metrics=Metrics)

print(model.summary())

#tf.keras.utils.plot_model(model, "FFT_added_LSTM/ModelGen/Model/Model_LSTM_31_FFT.png", show_shapes=True)

model.save(modelPath,save_format="h5")