# Tutorial · Tokenization

## Why it exists

People debug "the model cannot spell" and "the model is bad at
Korean" for days before they look at the tokenizer. This note is
how lab 01 is supposed to change what you see when you look at a
string.

## The idea

A **token** is an integer the model was trained to read. The
**tokenizer** is the reversible-enough map between bytes and those
integers. Modern LLM tokenizers are usually **byte-level BPE**
(or a close cousin): start from bytes, merge frequent pairs, stop
at a vocabulary size. WordPiece and Unigram are the other names
you will see on older cards. SentencePiece is a container and
training library, not a third algorithm in the abstract.

You need four facts in your hands:

1. **Fertility** is tokens per word (or per character). High
   fertility means a "short" sentence is a long context and a
   large bill. Code, URLs, and some languages pay more.
2. **The chat template is part of the tokenizer contract.** Special
   tokens (`bos`, `eos`, `eot`, role markers) are why lab 04 exists.
   Serving with the wrong template is a silent quality regression
   (O1).
3. **Detokenization is lossy in the ways that hurt.** Leading
   spaces, NFC versus NFD Unicode, and byte fallbacks explain
   "the model inserted a weird character."
4. **You cannot mix tokenizers.** Embeddings, log-probs, and fine-
   tunes are in token-id space. Counting GPT-4 tokens for a Llama
   bill is how finance tickets start.

Lab 01 builds BPE on a tiny corpus so the merge table is not magic.
It will look toy. That is the point. After it, a Hugging Face
`AutoTokenizer` is a file format, not a personality.

## The gap most tutorials leave

They `encode()` once and print ids. They never make you train merges
by hand, so you do not feel why rare names shatter into bytes. They
never connect fertility to **cost** (O3) and **multilingual failure**
(S11).

## How the lab should feel

You start with characters or bytes. You count pair frequencies. You
merge. You watch a common word become one token and a rare word stay
a pile of pieces. If you feel slightly bored by the counting, you
are doing it right. If you skip to a pretrained tokenizer before
you have a merge list, you missed the lab.

When you later call `tokenizer(text, return_tensors="pt")` in other
labs, you should be able to print `input_ids` and guess which tokens
are whole words and which are shrapnel.

## Practice

1. Run `notebooks/01_tokenization_bpe.ipynb`.
2. Tokenize the same English sentence, a code snippet, and a short
   line of a language you know that is not English, with a public
   Llama-family tokenizer and a public GPT-family tokenizer (tiktoken
   or the matching Hugging Face name). Write fertility for each.
3. Read one model card's tokenizer section. Note vocab size and
   whether the card names the chat template.

Karpathy's tokenizer video is the watch-along, not a substitute for
the notebook.

## Watch and read

- Andrej Karpathy, [Let's build the GPT Tokenizer](https://www.youtube.com/watch?v=zduSFxRajkE)
- Sennrich et al., Neural Machine Translation of Rare Words with
  Subword Units, 2016, [arXiv:1508.07909](https://arxiv.org/abs/1508.07909)
  (BPE in NMT)
- Hugging Face tokenizers docs
- CS336 tokenization lectures (see [YOUTUBE.md](../reference/YOUTUBE.md))

## Knowledge check

1. Why can two English sentences with the same word count differ in
   token count?
2. What breaks if you fine-tune with tokenizer A and serve with
   tokenizer B?
3. Why do some languages look "worse" on a model that scores well
   on English MMLU?
4. Where do chat role markers live: in the weights, or in the
   tokenizer and template?
5. Why does lab 01 use a tiny corpus on purpose?

<details>
<summary>Answers</summary>

1. Different words hit different merge paths. Rare or mixed-script
   strings split more. Numbers and code often have high fertility.
2. Ids no longer mean the same pieces. The network sees garbage
   compared with training. Loss and quality both lie.
3. Higher fertility uses more of the context window and more of
   the loss budget per word. The tokenizer was often trained on a
   different mix than the advertised "multilingual" label.
4. In the tokenizer's special tokens and the chat template applied
   before encode. Weights only see ids.
5. So you can watch merges happen. A production vocab hides the
   algorithm behind a 128k table.

</details>
