# F1 · Mathematics for language models

## Why it exists

Every later module will say "gradient," "dot product," "softmax," or
"expectation" as if those were English. They are not. This file is the
minimum so the rest of the course does not have to pretend.

## The idea

### Linear algebra

A language model is mostly matrix multiplies. A vector is a list of
numbers with a direction. A matrix is a stack of those lists that
rotates, stretches, or projects other vectors.

You need, working, not ceremonial:

- **Dot product.** Two vectors are similar when this is large (after
  normalization, this is cosine similarity: the retrieval primitive).
- **Matrix multiply.** `(tokens × d_in) @ (d_in × d_out)` is how a linear
  layer maps features. Attention scores are also a multiply:
  `Q @ Kᵀ`.
- **Transpose.** Swapping rows and columns is how keys meet queries.
- **Eigenvectors** are optional until you read a paper about linear
  representations. Do not block on them.

Watch [3Blue1Brown, Essence of Linear Algebra](https://www.youtube.com/watch?v=fNk_zzaMoSs&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab)
before you read a textbook chapter. Geometry first, notation second.

### Calculus

Training is "change the weights a little so this number gets smaller."
That number is the loss. The little change is the negative gradient.

You need:

- **Derivative** as slope.
- **Partial derivative** as slope in one weight, holding the others.
- **Chain rule** as the reason backpropagation exists.
- **Gradient** as the vector of all partials. Gradient descent steps
  opposite that vector.

You do not need real analysis. You do need to stop saying "the model
learns" as if it were a mood.

Khan Academy calculus 1 is enough. StatQuest is enough for the
statistical side.

### Probability and statistics

Next-token prediction is a probability distribution over a vocabulary.
Sampling is a draw from that distribution. Evaluation is an estimate
with a sample size and a bias.

You need:

- **Random variable, expectation, variance.**
- **Softmax** as "turn scores into a distribution."
- **Cross-entropy / negative log-likelihood** as "how surprised was the
  model by the true next token?"
- **MLE** as "pick weights that make the training tokens likely."
- **Bayes** at the level of "prior, likelihood, posterior," because
  alignment papers will say it.
- **Confidence intervals and contamination** as the reason a 0.7%
  leaderboard gap is often noise.

[Seeing Theory](https://seeing-theory.brown.edu/) is the visual
companion. [StatQuest statistics](https://www.youtube.com/watch?v=qBigTkBLU6g&list=PLblh5JKOoLUK0FLuzwntyYI10UQFUhsY9)
is the spoken one.

## The gap most roadmaps leave

They list "linear algebra, calculus, probability" and move on. The
missing move is **which objects you will actually touch**:

| Object | Where it shows up |
|---|---|
| Cosine | RAG, eval of embeddings |
| Softmax + temperature | decoding |
| Cross-entropy | pre-training and SFT loss |
| KL divergence | DPO, PPO, distillation |
| Logits vs log-probs | every alignment paper |
| FLOPs vs memory | F5 and the operator track |

If you can define those six, you can read Scientist. If you cannot, stay
here.

## Practice

No notebook. Do this on paper:

1. Write a 2×3 matrix times a 3-vector by hand.
2. Softmax the scores `[2.0, 1.0, 0.1]` with temperature 1 and with
   temperature 0.5. Notice the mass concentrates.
3. If the true token is the first one, write the cross-entropy.

Then watch the 3Blue1Brown neural network series through the attention
episode.

## Watch and read

- 3Blue1Brown, linear algebra playlist and neural network series
- StatQuest, statistics fundamentals
- Khan Academy, linear algebra, calculus 1, statistics
- Immersive Linear Algebra, [immersivemath.com/ila](https://immersivemath.com/ila/learnmore.html)
- Stanford CS336 lecture 2 (resource accounting) once F5 is open

## Knowledge check

1. What does a dot product have to do with retrieval?
2. Why is temperature a thing you can put on softmax?
3. What is the training job, in one sentence, in math language?
4. Why is a 0.3% MMLU gap usually not a decision?
5. Name one place KL divergence will appear later in this course.

<details>
<summary>Answers</summary>

1. Retrieval ranks chunks by similarity of embedding vectors. Cosine
   similarity is a normalized dot product.
2. Temperature divides the logits before softmax. Lower temperature
   sharpens the distribution; higher flattens it.
3. Minimize expected cross-entropy of the next token under the data
   distribution (with regularization and engineering around that).
4. Sample size, contamination, and prompt format dominate that scale.
5. DPO, PPO's KL penalty to the reference model, or distillation.

</details>
