import numpy as np
from concurrent.futures import ThreadPoolExecutor
import traceback
import jax
import jax.numpy as jnp
from ._errors import *
import optax
from ._utils import *
import os
import flax
import time


class Debugger():
    def __init__(self,debug = False,path=None) -> None:
        self.debug = debug
        self.path = path
        if path is not None:
            self.logfile = open(path, "a")
    
    def turn_debugger_on(self):
        self.debug = True
        self.logfile = open(self.path, "a")

    def logger(self,message,state="DEBUG"):
        if self.debug:
            if self.path is None:
                print(f"[{state}] {message}")
            else:
                self.logfile.write(f"[{state}] {message}\n")
                self.logfile.flush()

    def trace_func(self,func):
        def wrapper(*args, **kwargs):
            self.logger(f"Calling {func.__name__} with args: {[type(i) for i in args]}, kwargs: {[type(i) for i in kwargs]}",state="FUNC_CALL")
            start_time = time.time()
            try:
                out = func(*args, **kwargs)
            except Exception as e:
                self.logger(f"{func.__name__} Exception:{e}",state="ERROR")
                self.logger(traceback.format_exc(), state="TRACEBACK")
                raise
            name = f"{args[0].__class__.__name__}.__init__" if func.__name__ == "__init__" else func.__name__
            self.logger(f"{name} returned: {type(out)} with shape/info: {getattr(out, 'shape', 'uk')}, {getattr(out, 'dtype', 'uk')}, Time taken:{time.time()-start_time}s",state="FUNC_RETURN")
            return out
        return wrapper

debug_state = Debugger()


class Tokenization():
    @debug_state.trace_func
    def __init__(self,vocab="gpt2") -> None:
        import tiktoken
        self.stuff = tiktoken
        self.vocab = vocab
        self.enc = tiktoken.get_encoding(self.vocab)

    @debug_state.trace_func
    def tokenize(self,batch:list, workers:int, max_length:int):
        self.enc = self.stuff.get_encoding(self.vocab)
        enc = self.enc
        eos_token = 50256
        pad_token = 0

        def encode_and_pad(text):
            tokens = enc.encode(text, allowed_special={'<|endoftext|>'})[:max_length]
            padded = np.full(max_length, pad_token, dtype=np.int32)
            mask = np.zeros(max_length, dtype=np.int32)
            padded[:len(tokens)] = tokens
            mask[:len(tokens)] = 1  # Mark real tokens as 1
            return padded, mask
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            results = list(executor.map(encode_and_pad, batch))
        
        encoded_batch, mask = zip(*results)  # Split tokens and masks
        encoded_batch = np.array(encoded_batch)
        mask = np.array(mask)
        
        return encoded_batch, mask

    @debug_state.trace_func
    def tokenize_(self, batch: list):
        self.enc = self.stuff.get_encoding(self.vocab)
        enc = self.enc
        eos_token = 50256

        encoded_batch = []
        mask = []

        for text in batch:
            tokens = enc.encode(text, allowed_special={'<|endoftext|>'})
            encoded_batch.append(np.array(tokens, dtype=np.int32))
            mask.append(np.ones(len(tokens), dtype=np.int32))  # Mask matches token length
        
        return jnp.array(encoded_batch), jnp.array(mask)
    
    @debug_state.trace_func
    def decode(self,tokens):
        return self.enc.decode(tokens)
    
class Flax_ds():
    @debug_state.trace_func
    def __init__(self,x_eq_y:bool) -> None:
        self.x_eq_y = x_eq_y
        self.x = None
        self.mask = None
        self.y = None
        self.batch = None
    
    @debug_state.trace_func
    def load_data(self,x,mask,y):
        self.x = np.array(x)
        self.mask = mask
        if not self.x_eq_y:
            self.y = np.array(y)
    
    @debug_state.trace_func
    def batch_it_(self,batch_size):
        if not self.x_eq_y:
            self.x = jnp.array(self.x)
            self.mask = jnp.array(self.mask)
            self.y = jnp.array(self.y)
            seq_len = self.x.shape[1]
            
            n_batches = len(self.x) // batch_size
            num_devices = jax.device_count()
            
            x_batch = [self.x[i * batch_size:(i + 1) * batch_size] for i in range(n_batches)]
            mask_batch = [self.mask[i * batch_size:(i + 1) * batch_size] for i in range(n_batches)]
            y_batch = [self.y[i * batch_size:(i + 1) * batch_size] for i in range(n_batches)]
            
            
            self.batch = [[i.reshape(num_devices,-1, seq_len), j.reshape(num_devices,-1, seq_len), k.reshape(num_devices,-1, seq_len)] for i, j, k in zip(x_batch, mask_batch, y_batch)]

            del self.x, self.mask, self.y
            return self.batch
        
        else:
            self.x = jnp.array(self.x)
            self.mask = jnp.array(self.mask)
            seq_len = self.x.shape[1]
            
            n_batches = len(self.x) // batch_size
            num_devices = jax.device_count()
            
            x_batch = [self.x[i * batch_size:(i + 1) * batch_size] for i in range(n_batches)]
            mask_batch = [self.mask[i * batch_size:(i + 1) * batch_size] for i in range(n_batches)]
            
            
            self.batch = [[i.reshape(num_devices,-1, seq_len), j.reshape(num_devices,-1, seq_len)] for i, j in zip(x_batch, mask_batch)]

            del self.x, self.mask
            return self.batch
        
    
    def __len__(self):
        return len(self.batch)

    def stream_it(self):
        if self.batch == None:
            IncorrectDtype("Bruh... You forgot to run '.batch_it' before trying to stream it.... T~T")
        if self.x_eq_y:
            for i in self.batch:
                yield i[0],i[1],i[0]
        else:
            for i in self.batch:
                yield i[0],i[1],i[2]
    
    @property
    def gimme_the_data(self):
        return self.batch
    
class Optimizer():
    @debug_state.trace_func
    def __init__(self,optimizer,lr,lrf,batches,epochs,params):
        decay_rate = (lrf / lr) ** (1 / (batches * epochs))
        self.lr_schedule = optax.exponential_decay(
            init_value=lr,
            transition_steps=1,
            decay_rate=decay_rate,
            staircase=False  # Smooth decay
        )
        self.optimizer = optimizer(self.lr_schedule)
        self.state = self.optimizer.init(params)
    
    @debug_state.trace_func
    def load(self,path,dtype=None):
        try:
            with open(os.path.join(path, "make_stuff_better.pkl"), "rb") as f:
                self.state = flax.serialization.from_bytes(self.state, f.read())
                if dtype is not None:
                    self.state = convert_tree(dtype,self.state)
                print("Using loaded optimizer states")
        except:
            print("No optimizers states found")

    @debug_state.trace_func
    def save(self,path):
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "make_stuff_better.pkl"), "wb") as f:
            f.write(flax.serialization.to_bytes(self.state))

