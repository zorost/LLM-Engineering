# F4 · NLP before transformers

## Why it exists

Transformers did not appear in a vacuum. If you do not know what
tokenization, n-grams, and recurrence were *for*, you will treat BPE
and attention as magic.

## The idea

### Text is not a tensor until you say how

**Tokenization** splits text into units. Words, characters, subwords.
Stemming and lemmatization were the pre-neural attempts to collapse
"running" and "ran." Stop-word lists were a blunt instrument. You still
need a policy for Unicode, numbers, and code.

### Features before embeddings

- **Bag-of-words / TF-IDF.** Counts, maybe weighted. Fast, strong
  baselines, no word order.
- **n-grams.** Local order, combinatorial explosion.
- **Word2Vec, GloVe, FastText.** Dense vectors. Similar words near each
  other. FastText helps rare and morphologically rich words.

Jay Alammar's illustrated Word2Vec and Lena Voita's embeddings chapter
are the right first readings.

### Recurrence

RNNs, LSTMs, GRUs read a sequence left to right (or both ways). They
were the seq2seq backbone before attention. LSTMs exist to carry a
gradient across time. They still lose long-range structure compared to
self-attention, which is the point of the 2017 Transformer paper.

colah's LSTM post remains the clearest picture of the gates.

### Attention (the bridge)

Self-attention lets every token look at every other token in the window.
That is the move that retired recurrence as the default backbone. You
meet the formula in lab 02 and the full wiring in S1. Here you only need
the claim: **order is in the computation, not in a hidden state that
forgets**. 3Blue1Brown's transformer video is the picture. Jay Alammar's
illustrated transformer is the labeled diagram.

### Transformer stack

A decoder-only block is: attention, residual, norm, MLP, residual, norm
(the exact order varies: Pre-LN vs Post-LN). Stack those blocks, add a
token embedding and an unembedding, and you have the object later modules
call "the model." Residual streams and RMSNorm are named in F3 so they
are not a surprise in S1.

### LLM families

Once the stack exists, products differ by **data, scale, and post-training**,
not by a new animal each month. Dense decoder-only, mixture of experts,
vision-language wrappers, and a handful of state-space hybrids are the
families you will actually meet. S1 names them. F5 and lab 17 tell you
why MoE changes the serving bill. Do not collect a zoo of logos. Collect
a way to read a model card.

## The gap most roadmaps leave

They mention Word2Vec and skip **the production leftover**:

- Search still uses BM25 (sparse). Hybrid RAG is TF-IDF plus dense, not
  dense alone. See lab 09 and E4.
- Byte-level BPE is a descendant of "we cannot keep a word vocabulary
  in production."
- Evaluation of embeddings is a retrieval problem (MTEB), not a word
  analogy toy.

Classical NLP is not a museum. It is half of hybrid retrieval.

## Practice

Lab `notebooks/01_tokenization_bpe.ipynb`. Then implement TF-IDF on ten
documents in five lines of NumPy or sklearn and retrieve with cosine.
You will reuse that in lab 09.

## Watch and read

- Lena Voita, [Word embeddings](https://lena-voita.github.io/nlp_course/word_embeddings.html)
- Jay Alammar, [Illustrated Word2Vec](https://jalammar.github.io/illustrated-word2vec/)
- colah, [Understanding LSTM Networks](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
- spaCy guide on Real Python
- Kaggle NLP micro-courses, as drills not as doctrine

## Knowledge check

1. What does TF-IDF punish?
2. Why did subword tokenization win over word vocabularies?
3. What problem does FastText solve that Word2Vec does not?
4. Why are LSTMs not the default LLM backbone?
5. Where does BM25 still belong in 2026?

<details>
<summary>Answers</summary>

1. Terms that appear in almost every document. They carry little
   identity.
2. Open vocabulary, rarer words, morphology, and code tokens, without a
   UNK disaster.
3. Character n-grams inside a word, so unseen words still have a vector.
4. Sequential training is slow to parallelize; long-range credit
   assignment is weaker than self-attention; inference KV caches are a
   transformer story.
5. Hybrid retrieval: keyword precision next to dense recall.

</details>
