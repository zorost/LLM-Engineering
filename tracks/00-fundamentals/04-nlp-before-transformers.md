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
