# NLP Sequence Model Architecture

## 0. FNN (Feedforward Neural Network) — NO sequence

```
┌─────────────────────────────────────────────────────────────────┐
│  FNN  ← simplest neural network                                │
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                    │
│  │  Input    │──→│  Hidden  │──→│  Output  │                    │
│  │  Layer    │   │  Layer   │   │  Layer   │                    │
│  └──────────┘   └──────────┘   └──────────┘                    │
│                                                                 │
│  One direction only: input → output, NO memory                  │
│  ❌ Cannot handle sequences (no word order)                     │
└─────────────────────────────────────────────────────────────────┘
```

## 1. RNN Family (Contains Relationship)

### RNN — FNN + Recurrent Loop

```
┌─────────────────────────────────────────────────────────────────┐
│  RNN  ← contains FNN + recurrent loop                          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  FNN (at each time step)                            │        │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐        │        │
│  │  │  Input   │──→│  Hidden  │──→│  Output  │        │        │
│  │  │  Layer   │   │  Layer   │   │  Layer   │        │        │
│  │  └──────────┘   └────┬─────┘   └──────────┘        │        │
│  └──────────────────────┼──────────────────────────────┘        │
│                         │                                       │
│                    ┌────▼────┐                                   │
│                    │Recurrent│ ← hidden state loops back        │
│                    │  Loop   │   to next time step              │
│                    └─────────┘                                   │
│                                                                 │
│  ✅ Solved: can read sequences word by word                     │
│  ❌ Problem: vanishing gradient (forgets early words)           │
└─────────────────────────────────────────────────────────────────┘
```

### LSTM — Contains RNN + 3 Gates

```
┌─────────────────────────────────────────────────────────────────┐
│  LSTM  ← contains RNN + 3 gates                                │
│                                                                 │
│  ┌─────────────────────────────────────────────────────┐        │
│  │  RNN (recurrent unit)                               │        │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐        │        │
│  │  │  Input   │──→│  Hidden  │──→│  Output  │        │        │
│  │  │  Layer   │   │  Layer   │   │  Layer   │        │        │
│  │  └──────────┘   └──────────┘   └──────────┘        │        │
│  └─────────────────────────────────────────────────────┘        │
│                                                                 │
│  + 3 Gates (NEW!)                                               │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │ Forget Gate  │ │ Input Gate   │ │ Output Gate  │            │
│  │ (what to     │ │ (what to     │ │ (what to     │            │
│  │  forget)     │ │  remember)   │ │  output)     │            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                 │
│  + Cell State (long-term memory highway)                        │
│                                                                 │
│  ✅ Solved: vanishing gradient (gates control what to remember) │
│  ❌ Problem: sequential (slow), only reads one direction        │
└─────────────────────────────────────────────────────────────────┘
```

### Bi-LSTM — Contains 2 LSTMs (forward + backward)

```
┌─────────────────────────────────────────────────────────────────┐
│  Bi-LSTM  ← contains 2 LSTMs                                   │
│                                                                 │
│  ┌──────────────────────────────┐                               │
│  │  Forward LSTM (fwd)          │                               │
│  │  ┌────────────────────────┐  │                               │
│  │  │  RNN + 3 Gates         │  │                               │
│  │  └────────────────────────┘  │                               │
│  │  reads: "I" → "love" → "NLP"│                               │
│  └──────────────────────────────┘                               │
│                                    ← outputs are concatenated   │
│  ┌──────────────────────────────┐                               │
│  │  Backward LSTM (bwd)        │                               │
│  │  ┌────────────────────────┐  │                               │
│  │  │  RNN + 3 Gates         │  │                               │
│  │  └────────────────────────┘  │                               │
│  │  reads: "NLP" → "love" → "I"│                               │
│  └──────────────────────────────┘                               │
│                                                                 │
│  ✅ Solved: each word sees both left and right context          │
│  ❌ Problem: still sequential, still slow                       │
└─────────────────────────────────────────────────────────────────┘
```

### 2014 Seq2Seq (NO Attention)

```
┌─────────────────────────────────────────────────────────────────┐
│  Seq2Seq (2014)  ← NO Attention                                │
│                                                                 │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐ │
│  │  Encoder                 │  │  Decoder                     │ │
│  │  ┌────────────────────┐  │  │  ┌────────────────────────┐  │ │
│  │  │  Bi-LSTM           │  │  │  │  LSTM                  │  │ │
│  │  │  ┌──────┐┌──────┐  │  │  │  │  ┌──────────────────┐  │  │ │
│  │  │  │LSTM→ ││←LSTM │  │  │  │  │  │ RNN + 3 Gates    │  │  │ │
│  │  │  │(fwd)  ││(bwd)  │  │  │  │  │  │ (forget/input/  │  │  │ │
│  │  │  └──────┘└──────┘  │  │  │  │  │  │  output)        │  │  │ │
│  │  └────────────────────┘  │  │  │  └──────────────────┘  │  │ │
│  │                          │  │  └────────────────────────┘  │ │
│  └──────────────────────────┘  │                              │ │
│                                │  Decoder only sees encoder's │ │
│                                │  LAST hidden state           │ │
│                                │  ← Information Bottleneck!   │ │
│                                └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### 2015 Seq2Seq + Attention (Bottleneck solved, but still slow)

```
┌─────────────────────────────────────────────────────────────────┐
│  Seq2Seq + Attention (2015)  ← Added Cross-Attention           │
│                                                                 │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐ │
│  │  Encoder                 │  │  Decoder                     │ │
│  │  ┌────────────────────┐  │  │  ┌────────────────────────┐  │ │
│  │  │  Bi-LSTM           │  │  │  │  LSTM                  │  │ │
│  │  │  ┌──────┐┌──────┐  │  │  │  │  ┌──────────────────┐  │  │ │
│  │  │  │LSTM→ ││←LSTM │  │  │  │  │  │ RNN + 3 Gates    │  │  │ │
│  │  │  │(fwd)  ││(bwd)  │  │  │  │  │  └──────────────────┘  │  │ │
│  │  │  └──────┘└──────┘  │  │  │  └────────────────────────┘  │ │
│  │  └────────────────────┘  │  │                              │ │
│  │                          │  │  + Cross-Attention (NEW!)    │ │
│  │  Outputs ALL hidden      │◄─┤    Decoder looks back at    │ │
│  │  states: h1, h2, ... hn  │  │    ALL encoder outputs      │ │
│  │  (keep all, not just last)│  │    at every step            │ │
│  └──────────────────────────┘  └──────────────────────────────┘ │
│                                                                 │
│  ✅ Solved: information bottleneck (decoder sees all positions) │
│  ❌ Remaining: RNN is sequential (slow), weak long-range deps  │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Transformer (2017) — NO RNN Inside!

```
┌─────────────────────────────────────────────────────────────────┐
│  Transformer (2017)  ← Completely new, NO RNN/LSTM!            │
│                                                                 │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐ │
│  │  Encoder Stack (x6)      │  │  Decoder Stack (x6)         │ │
│  │                          │  │                              │ │
│  │  ┌────────────────────┐  │  │  ┌────────────────────────┐  │ │
│  │  │  Self-Attention    │  │  │  │  Masked Self-Attention │  │ │
│  │  │  (each word sees   │  │  │  │  (can only see left)   │  │ │
│  │  │   all words)       │  │  │  └────────────────────────┘  │ │
│  │  └────────────────────┘  │  │  ┌────────────────────────┐  │ │
│  │  ┌────────────────────┐  │  │  │  Cross-Attention       │  │ │
│  │  │  Feed-Forward      │  │  │  │  (looks at encoder)    │  │ │
│  │  └────────────────────┘  │  │  └────────────────────────┘  │ │
│  │                          │  │  ┌────────────────────────┐  │ │
│  │  + Positional Encoding   │  │  │  Feed-Forward          │  │ │
│  └──────────────────────────┘  │  └────────────────────────┘  │ │
│                                └──────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## 3. BERT / GPT — Split Transformer in Half

```
       Transformer (full)
       ┌────────┬────────┐
       │Encoder │Decoder │
       │ Stack  │ Stack  │
       └───┬────┴───┬────┘
           │        │
      take left   take right
           │        │
           ▼        ▼
    ┌──────────┐ ┌──────────┐
    │   BERT   │ │   GPT    │
    │ Encoder  │ │ Decoder  │
    │ only     │ │ only     │
    │ (NLU)    │ │ (NLG)    │
    └──────────┘ └──────────┘
```

## 4. Summary

| Model | Year | Contains | Self-Attn? | Cross-Attn? | Problem | Status |
|---|---|---|---|---|---|---|
| RNN | 1986 | basic recurrent unit | ❌ | ❌ | vanishing gradient | obsolete |
| LSTM | 1997 | RNN + 3 gates (forget/input/output) | ❌ | ❌ | sequential, slow | obsolete |
| Bi-LSTM | — | forward LSTM + backward LSTM | ❌ | ❌ | sequential, slow | obsolete |
| Seq2Seq | 2014 | Bi-LSTM enc + LSTM dec | ❌ | ❌ | info bottleneck + slow | obsolete |
| Seq2Seq+Attn | 2015 | above + Cross-Attention | ❌ | ✅ | bottleneck solved, still slow | obsolete |
| Transformer | 2017 | Self-Attn + Cross-Attn + FF (NO RNN!) | ✅ | ✅ | — | current |
| BERT | 2018 | Transformer Encoder only | ✅ | ❌ | — | current |
| GPT | 2018 | Transformer Decoder only | ✅ | ❌ | — | current |
