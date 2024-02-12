#!/usr/bin/env python
# coding: utf-8

# In[47]:


import os
import re
import glob
import numpy as np
import json
import os 

from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.utils import to_categorical


# In[48]:


data_scrapes =  os.path.join(".." , "data-scrapes" )


# In[49]:


import datetime, time
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H%M%S')

print("Converting sequences ... ")
out_file = os.path.join('..', 'data', 'protein-seqs-' + st + '.txt')

print("Writing to: %s" % out_file)


# In[50]:


num = 0
fasta_files = glob.glob(data_scrapes + "/*.fasta")
fasta_files


# In[51]:


# helper function 

def dump_to_file(protein_id, sequence):
    with open(out_file, "a") as f:
        f.write(protein_id + "," + sequence + "\n")


# In[300]:


for file in fasta_files:
    with open (file , 'r') as f:
        protein_id = ''
        protein_seq = ''
        
        for line in f:
            
            match = re.search(r'^>([a-z]{2})\|([A-Z0-9]*)\|', line) 
            if match:
                if protein_id != '':
                    dump_to_file(protein_id , protein_seq)
                    

            
                protein_id = match.group(2)
                protein_seq = ''
            
            else:
                protein_seq+=line.strip()
        
        if protein_id != '':
            dump_to_file(protein_id, protein_seq)


# In[52]:


print("Converting functions ...") 
out_file_fns = os.path.join('..', 'data', 'protein-functions-' + st + '.txt')
print(out_file_fns)
# target_functions = ['0005524'] #ATP binding   
# target_functions = ['0008565']  # protein transporter activity
# target_functions = ['0004707']   # centromeric DNA binding
target_functions = ['0004222' , '0005524']   #



# In[53]:


annot_files = glob.glob(data_scrapes + '/*.txt')
annot_files


# In[54]:


has_function = []
for file in annot_files:
    
    with open (file  , 'r') as f:
        
        for line in f:
            
            match = re.search(r'([A-z0-9]*)\sGO:(.*);\sF:.*', line)
            if match:
                protein_id = match.group(1)
                fun = match.group(2)
                
                if fun not in target_functions:
                    continue
                has_function.append(protein_id)
                
    import json
    with open(out_file_fns, 'w') as fp:
        json.dump(has_function, fp)
        
    # Take a peek 
    print(has_function[:10])        
    
    
