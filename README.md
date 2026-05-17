# 🎠 LinkedIn Carousel Generation Agent

A GenAI workflow that takes a topic and reference LinkedIn carousels, then generates a complete style-matched carousel slide-by-slide using a 3-step AI pipeline.

Built with **Python**, **Streamlit**, and **Gemini API**.

🔗 **Live Demo:** https://linkedin-carousel-agent.streamlit.app/
📁 **GitHub:** https://github.com/mohitkhyalia1/linkedin-carousel-agent

---

## How It Works

```
User Input (topic + reference carousels)
        │
        ▼
  [1] ANALYZER  →  extracts tone, hook style, CTA style, slide structure
        │
        ▼  style_profile (JSON)
  [2] WRITER    →  generates slides with title, content, visual idea
        │
        ▼  draft_carousel (JSON)
  [3] REVIEWER  →  fixes weak hooks, long slides, repetition
        │
        ▼
  Final Carousel
```

---

## Why Python Instead of Gumloop?

The assignment was inspired by Gumloop-style modular AI workflows. I implemented the equivalent pipeline directly in Python, which gave more control over prompt engineering and JSON chaining between stages. The architecture still follows the same node-based design — each agent is an independent, reusable component with a clear input/output contract.

---

## Features

- Analyzes reference carousels and extracts writing style
- Generates slides with title, content, and a visual idea per slide
- Includes a CTA slide automatically
- Reviewer step improves weak slides before final output
- Download carousel as JSON

---

## Folder Structure

```
linkedin-carousel-agent/
├── app.py
├── requirements.txt
├── agents/
│   ├── analyzer.py
│   ├── writer.py
│   └── reviewer.py
├── prompts/
│   ├── analyzer_prompt.txt
│   ├── writer_prompt.txt
│   └── reviewer_prompt.txt
└── utils/
    ├── gemini_client.py
    └── parser.py
```

---

## Setup

```bash
pip install -r requirements.txt
```

Set your Gemini API key (get one free at [aistudio.google.com](https://aistudio.google.com/app/apikey)):

```bash
export GEMINI_API_KEY=your_key_here
```

Run the app:

```bash
streamlit run app.py
```

---

## Example Output

**Topic:** 5 habits that made me a better software engineer

```json
{
  "topic": "5 habits that made me a better software engineer",
  "slides": [
    {
      "title": "Hook",
      "content": "I was a mediocre developer for 2 years.\nThen I changed 5 habits.\nHere's what actually worked 👇",
      "visual": "Before/after split: messy desk vs clean setup",
      "is_cta": false
    },
    {
      "title": "Habit 1: Read other people's code",
      "content": "Most devs only read their own code.\nThe best engineers study open-source repos daily.\nIt rewires how you think about problems.",
      "visual": "GitHub repo screenshot with well-structured, highlighted code",
      "is_cta": false
    },
    {
      "title": "Found this useful?",
      "content": "Follow me for weekly engineering insights.\nSave this post to revisit later 🔖",
      "visual": "Profile photo with a friendly, approachable look",
      "is_cta": true
    }
  ]
}
```

---

## Design Decisions

| Decision | Reason |
|---|---|
| Prompts in `.txt` files | Easy to edit without touching Python code |
| JSON between stages | Each component is independently testable |
| Separate reviewer step | Shows multi-step workflow thinking; improves output reliability |
| No LangChain or frameworks | Keeps the code simple and easy to explain |

---

## Limitations

- Output quality depends on the reference examples provided
- Gemini may occasionally return malformed JSON
- Slide count may vary slightly from what's requested
- Visual suggestions are text-only ideas, not actual images

---

## Author

### Mohit Khyalia
IIT Bombay

- Built as a Generative AI internship assignment.
- Demonstrates: modular AI workflows, prompt engineering, multi-step generation, and structured outputs.
