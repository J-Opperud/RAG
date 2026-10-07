┌─────────────────────┐
│  1. User Question   │
│                     │
│ Technology: Python  │
│ Data: plain text    │
└──────────┬──────────┘
           │ question
           ▼
┌─────────────────────┐
│  2. Query Embedding │
│                     │
│ Technology:         │
│ Embedding model     │
│ Data: vector        │
└──────────┬──────────┘
           │ query vector
           ▼
┌─────────────────────┐
│ 3. Vector Database  │
│     Retrieval       │
│                     │
│ Technology: Vector  │
│ database            │
│ Data: relevant      │
│ document chunks     │
└──────────┬──────────┘
           │ retrieved chunks
           ▼
┌─────────────────────────────┐
│ 4. Prompt Assembly          │
│                             │
│ Technology: Python          │
│ prompt builder              │
│                             │
│ System prompt               │
│ + Retrieved context         │
│ + User question             │
│ + Citation instructions     │
└─────────────┬───────────────┘
              │ complete prompt
              ▼
┌─────────────────────────────┐
│ 5. LLM Generation           │
│                             │
│ Technology: LLM             │
│                             │
│ Input: assembled prompt     │
│ Output: grounded response   │
└─────────────────────────────┘
              │
              ▼
        User receives
          response