function_file = os.path.join('..' , 'data' ,'protein-functions-2024-02-12-161701.txt')
sequence_file = os.path.join('..' , 'data' ,'protein-seqs-2024-02-12-151317.txt')


# In[56]:


with open (function_file , 'r') as f:
    has_function = json.load(f)


# In[57]:


has_function[-10:]


# In[58]:


max_seq_len = 500


# In[59]:


X = []
y = []


# In[ ]:





# In[60]:


pos_example = 0
neg_example = 0


# In[61]:


with open (sequence_file , 'r') as seq_file:
    
    for line in seq_file:
        ln = line.split(',')
        protein_id = ln[0]
        protein_seq = ln[1].strip()
        
        if len(protein_seq) > max_seq_len:
            continue
        if protein_id in has_function:
            
            y.append(1)
            pos_example+=1
        
        else:
            y.append(0)
            neg_example+=1
        
        X.append(protein_seq)
        
        


# In[62]:


neg_example


# In[63]:


pos_example


# In[64]:


def sequence_to_indices(sequence):
    """Convert amino acid letters to indices. 
       _ means no amino acid (used for padding to accommodate for variable length)"""
    
    try:
        acid_letters = ['_', 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M',
                'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

        indices = [acid_letters.index(c) for c in list(sequence)]
        return indices
    except Exception:
        print(sequence)
        raise Exception


# In[ ]:





# In[ ]:





# In[27]:


X_all = []

for x in X:
    seq_ind = sequence_to_indices(x)
    X_all.append(seq_ind)


# In[29]:


X_all = np.array(X_all)
y_all = np.array(y)


# In[30]:


print(y[0])
print(X_all[0])
print(len(X_all[0]))


# In[31]:


X_all = sequence.pad_sequences(X_all , maxlen=max_seq_len)


# In[32]:


print(X_all[1])
print(len(X_all[1]))


# In[33]:


print(X_all.shape)
print(y_all.shape)


# In[34]:


n = X_all.shape[0]


# In[35]:


# randomize to shuffle first
randomize = np.arange(n)
np.random.shuffle(randomize)


# In[36]:


X_all = X_all[randomize]
y_all = y_all[randomize]


# In[ ]:





# In[37]:


test_split  = round(n *2/3)


# In[ ]:





# In[38]:


X_train = X_all[:test_split]
X_test = X_all[test_split:]
y_train = y_all[:test_split]
y_test = y_all[test_split:]


# In[ ]:


from tensorflow.keras.utils import to_categorical
y_train_categorical = to_categorical(y_train)
y_test_categorical = to_categorical(y_test)


# In[39]:


X_train.shape


# In[40]:


y_train.shape


# In[41]:


from tensorflow.keras.layers import Embedding, Input, Dropout, Flatten, Dense, Activation
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.optimizers import SGD


# In[42]:


num_amino_acids = 23 
embedding_dims = 10 
nb_epoch = 2
batch_size = 32


# In[43]:


model = Sequential()
model.add(Embedding(num_amino_acids , embedding_dims, input_length=max_seq_len))
model.add(Flatten())
model.add(Dense(25 ,activation='sigmoid'))
model.add(Dense(len(target_functions) ,activation='softmax'))



# In[44]:


model.summary()


# In[45]:


model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


# In[46]:


# hist = model.fit(X_train, y_train,
#                   batch_size = batch_size,
#                   epochs = nb_epoch, 
#                   validation_data = (X_test, y_test),
#                   verbose=1)
hist = model.fit(X_train, y_train_categorical, 
                 batch_size=batch_size, 
                 epochs=nb_epoch, 
                 validation_data=(X_test, y_test_categorical), verbose=1)


# In[332]:


# model.evaluate(X_test,y_test)
model.evaluate(X_test, y_test_categorical)
