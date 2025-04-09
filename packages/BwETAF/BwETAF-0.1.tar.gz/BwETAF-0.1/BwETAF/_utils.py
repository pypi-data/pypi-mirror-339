import jax
import optax
import jax.numpy as jnp
import numpy as np
from ._errors import *
import time
from functools import partial


def time_it(fn, *args):
    t0 = time.time()
    out = fn(*args)
    t1 = time.time()
    return out, t1 - t0


def loss_fn(params, model,batch, rng):
    """Computes sparse categorical cross-entropy loss with autoregressive shifting."""
    inputs, mask, targets = batch  # Inputs: (batch, seq_len), Targets: (batch, seq_len)

    logits = model.apply(params, inputs, mask,rngs={"dropout": rng})  # Forward pass
    log_probs = jax.nn.log_softmax(logits)  # Convert logits to log probabilities

    # Shift targets left: Model predicts targets[:, 1:] given inputs[:, :-1]
    shifted_targets = targets[:, 1:]  # Remove first token
    shifted_logits = log_probs[:, :-1, :]  # Remove last token prediction

    # Get probability of correct class
    target_probs = jnp.take_along_axis(shifted_logits, shifted_targets[..., None], axis=-1)[..., 0]

    loss = -target_probs.mean()  # Negative log-likelihood loss

    return loss

def val_loss(params, loss_fn, model_struct, x,mask,y, key):
    return loss_fn(params, model_struct, [x,mask,y], key)


val_loss = jax.jit(
    val_loss,
    static_argnums=(1,2)
)

val_loss = jax.pmap(
    val_loss,
    in_axes=(None,None,None,0,0,0,None),
    static_broadcasted_argnums=(1,2),
    axis_name='batch'
    )
def BatchTrain(params, grad_fn, model_struct, x, mask, y, key, optimizer, opt_state):
    # Yeh this too... Sry I have to hide it
    return None

BatchTrain = jax.jit(
    BatchTrain,
    static_argnums=(1, 2, 7)
)

BatchTrain = jax.pmap(  
    BatchTrain,
    static_broadcasted_argnums=(1, 2, 7),
    in_axes=(None, None, None, 0, 0, 0, None, None, None),
    axis_name="batch",
    out_axes=None
)

def get_first(pytree):
    return jax.tree_util.tree_map(lambda x: x[0], pytree)

def convert_tree(dtype,pytree):
    return jax.tree_util.tree_map(lambda x: x.astype(dtype),pytree)

@partial(jax.jit, static_argnums=(0,))
def call_model_jit(model_struct, params, x, mask, rngs):
    return model_struct.apply(params, x, mask, rngs=rngs, training=False)