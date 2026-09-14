# F3 · Neural networks

## Why it exists

A transformer is a neural network with a specific wiring. If the words
"layer," "loss," "overfit," and "Adam" are mush, every later diagram is
decoration.

## The idea

### The object

A network is functions composed: `y = f_L(...f_1(x)...)`. Each `f` is
usually a linear map plus a nonlinearity (ReLU, GELU, SiLU). Weights
are the numbers you change. Biases are the offsets. Activations are the
values that flow.

### Training

1. Forward: compute `y` and a **loss** against the target.
2. Backward: chain rule, every weight gets a gradient.
3. Update: AdamW is the default in LLM work. SGD still exists.
4. Repeat.

Loss for language is almost always token-level cross-entropy. MSE is
for regression demos, not for GPT.

### Regularization

Overfit means train loss went down and val loss did not, or val
accuracy is a fantasy. Dropout, weight decay, early stopping, and *more
data of the right kind* are the usual levers. Data augmentation in
language is not a random crop. It is rewriting, filtering, and packing.

### Implement one

You should, once, build a multilayer perceptron in PyTorch (or NumPy)
on a tiny dataset. Not because production LLMs are MLPs. Because
autograd has to become boring.

Patrick Loeber's PyTorch playlist and 3Blue1Brown's network series are
the pair. fast.ai if you want the "code first, theory as needed" path.

## The gap most roadmaps leave

They stop at MLP. LLM training adds:

- **Residual streams.** Add the block's output back to its input. This
  is why very deep transformers train at all.
- **LayerNorm / RMSNorm.** Stabilize the residual stream.
- **Teacher forcing.** During training you feed the true previous token,
  not the model's last guess.
- **Mixed precision.** fp16/bf16 are why the GPU fits.
- **Gradient clipping.** Loss spikes happen. Clip before you diverge.

You will see all five in S2 and S4. Meet them here as names so they are
not a surprise.

## Practice

Lab `notebooks/02_attention.ipynb` after you can write a linear layer.
If PyTorch is not installed, the lab uses NumPy. That is enough.

Optional: fast.ai lesson 1, then come back.

## Watch and read

- 3Blue1Brown, [But what is a neural network?](https://www.youtube.com/watch?v=aircAruvnKk)
- freeCodeCamp, [Deep Learning Crash Course](https://www.youtube.com/watch?v=VyWAvY2CF9c)
- [fast.ai Practical Deep Learning](https://course.fast.ai/)
- Patrick Loeber, [PyTorch playlist](https://www.youtube.com/playlist?list=PLqnslRFeH2UrcDBWF5mfPGpqQDSta6VK4)

## Knowledge check

1. What is a residual connection for?
2. Why is language modeling loss cross-entropy rather than MSE?
3. What is teacher forcing?
4. Name two ways a training run dies besides "NaN."
5. Why is dropout less fashionable inside modern transformers than it
   was in 2015 CNNs?

<details>
<summary>Answers</summary>

1. Let gradients and information skip the block so depth is usable.
2. The target is a class (a token id), not a continuous vector. The
   model outputs a distribution.
3. Training feeds the ground-truth prefix, not the model's own samples.
4. Loss spike / divergence; silently overfitting the val set; data
   loader deadlock; GPU OOM; learning rate too high.
5. Pre-training data volume, residual + norm, and weight decay do a lot
   of the work. Dropout still appears, but it is not the main story.

</details>
