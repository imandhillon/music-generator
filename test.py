import tensorflow as tf
from keras import backend as K
K.clear_session()
from keras.layers import LSTM, Dense, Activation, Dropout
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.models import load_model

block_size = 2700
	seq_len = 215
	#print('oy')
	#print(request.form, request.data, request.args, request.files, request.values, request.json)
	#print('pppp', request.form.get('filePath'))
	#print(request.form['filePath'])
	upl_str = '/'#request.form['filePath']
	#with app.open_resource(upl_str) as f:
	# with open(upl_str) as wf:
	# 	print(wf)
	# 	upl_file = wf
	#contents = f.read() - for txt testing

	#with open(upl_str, 'r') as f:
	x_data, y_data = make_tensors(upl_str, seq_len, block_size)

model = tf.keras.models.load_model('soundmodel.k')
model = tf.keras.models.load_model('soundmodel.k')
print(model)