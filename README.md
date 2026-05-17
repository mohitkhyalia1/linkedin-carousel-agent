# 🎠 LinkedIn Carousel Generation Agent

A GenAI workflow that takes a topic + reference examples and generates a complete, style-matched LinkedIn carousel — slide by slide — using a 3-step AI pipeline.

Built with Python, Streamlit, and the Gemini API.

---

## 🚀 Features

- **Style-aware generation** — analyzes your reference carousels and matches their tone, hook style, and writing patterns
- **Slide-by-slide output** — generates each slide with a title, content, and visual idea
- **Self-review step** — a reviewer agent improves weak slides before final output
- **Downloadable JSON** — export the full carousel for further use
- **Simple, clean UI** — no clutter, just input → generate → read

---

## 🔁 Workflow Explanation

```
User Input (topic + references)
        │
        ▼
  [1] ANALYZER
  Reads reference carousels
  Extracts: tone, hook style, CTA style,
            slide length, emoji usage
        │
        ▼ style_profile (JSON)
  [2] WRITER
  Generates carousel slide-by-slide
  Uses topic + style_profile to stay on-brand
        │
        ▼ raw_carousel (JSON)
  [3] REVIEWER
  Checks for: weak hooks, long slides,
              repetition, off-brand tone
  Rewrites only what needs fixing
        │
        ▼ final_carousel (JSON)
  Displayed in Streamlit UI
```

---

## 🧩 Component Breakdown

### `agents/analyzer.py`
Reads reference carousel text and returns a structured JSON style profile.
Asks Gemini to extract tone, hook style, CTA style, slide length, etc.

### `agents/writer.py`
Takes the topic + style profile and generates the full carousel.
Each slide has: title, content, visual idea, and a CTA flag.

### `agents/reviewer.py`
Reviews the generated carousel against the style profile.
Fixes weak hooks, long slides, repeated points, and vague visuals.

### `utils/gemini_client.py`
Simple wrapper around the Gemini API. One function: `call_gemini(prompt)`.

### `utils/parser.py`
Extracts JSON from Gemini's response text. Handles markdown code fences.

### `prompts/`
Plain text prompt templates with `{{VARIABLE}}` placeholders.
Keeping prompts in `.txt` files makes them easy to edit without touching Python.

---

## 📁 Folder Structure

```
linkedin-carousel-agent/
│
├── app.py                  # Streamlit UI
├── requirements.txt
├── README.md
│
├── agents/
│   ├── analyzer.py         # Style extraction agent
│   ├── writer.py           # Carousel generation agent
│   ├── reviewer.py         # Review & improvement agent
│
├── prompts/
│   ├── analyzer_prompt.txt
│   ├── writer_prompt.txt
│   ├── reviewer_prompt.txt
│
├── utils/
│   ├── gemini_client.py    # Gemini API wrapper
│   ├── parser.py           # JSON extractor
```

---

## ⚙️ Installation

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/linkedin-carousel-agent.git
cd linkedin-carousel-agent
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set your Gemini API key**
Option A: set it in your terminal/session
```bash
export GEMINI_API_KEY=your_key_here        # Mac/Linux
set GEMINI_API_KEY=your_key_here           # Windows CMD
```
Option B: create a local `.env` file in the project root
```bash
echo GEMINI_API_KEY=your_key_here > .env
# then edit .env and replace your_key_here with your actual key
```
Get your free key at: https://aistudio.google.com/app/apikey

---

## ▶️ How to Run

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📝 Example Input / Output

**Input Topic:**
> 5 habits that made me a better software engineer

**Input Reference (paste plain text of a carousel):**
> Slide 1: Most developers write code. The best ones write *readable* code.
> Slide 2: Habit 1 — Code review everything, including your own work...
> ...

**Output (sample):**
```json
{
  "topic": "5 habits that made me a better software engineer",
  "slides": [
    {
      "title": "Hook",
      "content": "I was a mediocre developer for 2 years.\nThen I changed 5 habits.\nHere's what actually worked 👇",
      "visual": "Split image: messy desk vs clean setup, or 'before/after' code snippet",
      "is_cta": false
    },
    {
      "title": "Habit 1: Read other people's code",
      "content": "Most devs only read their own code.\nThe best engineers study open-source repos daily.\nIt rewires how you think about problems.",
      "visual": "Screenshot of a GitHub repo with highlighted, well-structured code",
      "is_cta": false
    },
    ...
    {
      "title": "Found this useful?",
      "content": "Follow me for weekly insights on software engineering, career growth, and developer habits.\nSave this post to revisit later 🔖",
      "visual": "Profile photo with 'Follow' button highlighted, friendly and approachable look",
      "is_cta": true
    }
  ]
}
```

---

## 🧠 Design Decisions

| Decision | Reason |
|---|---|
| No LangChain/frameworks | Easier to understand, explain, and debug |
| Prompts in `.txt` files | Easy to edit without touching Python; clear separation |
| Simple JSON between steps | Each component is independently testable |
| `gemini-1.5-flash` model | Fast, free tier available, reliable for structured outputs |
| Reviewer as a separate step | Shows AI workflow thinking without overcomplicating |
| `{{VARIABLE}}` in prompts | Readable template system without added dependencies |

---

## ⚠️ Failure Cases / Limitations

- **Gemini returns malformed JSON** → The parser tries to recover but may return empty output. Adding a retry loop would help.
- **Very short references** → With less context, the style profile will be vague and output quality drops.
- **Hallucinated visuals** → Visual ideas are suggestions only; they need manual review.
- **Slide count not guaranteed** → Gemini may generate fewer or more slides than requested in rare cases.
- **No memory across runs** → Each generation is independent; there's no history stored.

---

## 🔮 Future Improvements

- Add a retry mechanism when JSON parsing fails
- Let users edit individual slides before download
- Export to PowerPoint / Canva template
- Add prompt A/B testing to compare different writing styles
- Allow image generation per slide using Imagen API
- Add a "regenerate this slide" button per slide

---

## 👤 Author

Built as a Generative AI internship assignment.
Demonstrates: modular AI workflows, prompt engineering, multi-step generation, and structured outputs.
