import numpy as np
import tensorflow as tf

from keras import backend as K
K.clear_session()
from keras.layers import LSTM, Dense, Activation, Dropout
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.optimizers import RMSprop
from keras.models import load_model

class Singleton:
   __instance = None
   model = None

   @staticmethod
   def get_instance():
      if Singleton.__instance == None:
         Singleton()
      return Singleton.__instance

   def __init__(self):
      if Singleton.__instance != None:
         """ Raise exception if init is called more than once. """
         raise Exception("This class is a singleton!")
      else:
         Singleton.__instance = self

   def get_model(self):
        if self.model is None:
            self.model = self.load_ml_model('soundmodel.k')
        return self.model

   def load_ml_model(self, model):
        """ Load deep learning model and return. """
        return tf.keras.models.load_model(model)





def construct_layers(timestep=215, block_size=2048):
	print('adding layers...\n')
	model = Sequential()
	model.add(LSTM(block_size, input_shape=(timestep, block_size), return_sequences=True))
	#model.add(Dropout(0.2))
	model.add(Dense(block_size))
	#model.add(Activation('linear'))
	return model

def train_model(model, x_data, y_data, nb_epochs=1):
	print('training...\n')
	optimizer = RMSprop(lr=0.01)
	model.compile(loss='mse', optimizer='rmsprop')
	model.fit(np.asarray(x_data), np.asarray(y_data), batch_size=500, epochs=nb_epochs, verbose=2)
	#Make it save weights
	print('tttt\n\n\n')
	return model


# def run():
# 	out_file = 'train'
# 	'''					sample rate * clip len / seq_len '''
# 	block_size = 2700	# Around min # of samples for human to (begin to) percieve a tone at 16Hz
# 	seq_len = 215


# 	'''*****(pseudo-code)*****
# 	corpus = []
# 	for file in dir:
# 		if file.endswith(.wav):
# 			music, rate = wav_to_np(file)
# 			music = music.sum(axis=1)/2
# 			corpus.extend(music)'''
			
# 	x_data, y_data = make_tensors('./ChillingMusic.wav', seq_len, block_size)


# 	model = construct_layers(seq_len, block_size)
# 	model = train_model(model, x_data, y_data)
# 	masterpiece = compose(model, x_data)

	
# 	masterpiece = convert_sample_blocks_to_np_audio(masterpiece[0]) #Not final, but works for now
# 	#print(masterpiece) #			Should now be a flat list
# 	masterpiece = write_np_as_wav(masterpiece)
# 	play_music()
# 	# print('\n\nWas it a masterpiece (or at least an improvement)?')

# 	'''Add CNN classifier after converting from Keras to Tensorflow to use generative-adversarial model.
# 	'''

# 	return


def load_model():
	pass

def get_seed(seed_len, data_train):
	nb_examples, seq_len = data_train.shape[0], data_train.shape[1]
	r = np.random.randint(data_train.shape[0])
	seed = np.concatenate(tuple([data_train[r+i] for i in range(seed_len)]), axis=0)
	#1 example by (# of examples) timesteps by (# of timesteps) frequencies
	seed_selection = np.reshape(seed, (1, seed.shape[0], seed.shape[1]))
	return seed_selection

def compose(model, x_data, graph):
	'''Could add choice of length of composition (roughly)'''
	print('composing...\n')
	generation = []
	muse = get_seed(1, x_data)
	with graph.as_default():
		for ind in range(1):
			print('predicting')
			preds = model.predict(muse)
			print(preds)
			print(len(preds), len(preds[0]), len(preds[0][0]))
			generation.extend(preds)
	return generation
