import streamlit as st
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from agents.analyzer import analyze_references
from agents.writer import write_carousel
from agents.reviewer import review_carousel
from utils.gemini_client import get_api_key

# --- Page Config ---
st.set_page_config(page_title="LinkedIn Carousel Agent", page_icon="🎠", layout="centered")

st.title("🎠 LinkedIn Carousel Generator")
st.markdown("**AI-powered carousel generation in 3 steps: Analyze → Write → Review**")

# Debug section
with st.expander("🔧 Debug Info", expanded=False):
    api_key = get_api_key()
    if api_key:
        st.success(f"✅ API Key found (length: {len(api_key)} chars)")
    else:
        st.error("❌ GEMINI_API_KEY not found. Set it via:")
        st.code("export GEMINI_API_KEY=your_key_here  # or add to .env", language="bash")

st.divider()

# --- Inputs ---
topic = st.text_input("📌 Carousel Topic", placeholder="e.g. 5 habits of great software engineers")

reference_text = st.text_area(
    "📋 Paste Reference Carousel Examples (text only)",
    placeholder="Paste 1–2 example carousels here. Plain text is fine.",
    height=200
)

num_slides = st.slider("Number of slides (excluding CTA)", min_value=3, max_value=8, value=5)

def create_pdf(carousel_data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    title = carousel_data.get("topic", "LinkedIn Carousel")

    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 20))

    for i, slide in enumerate(carousel_data["slides"], start=1):

        elements.append(
            Paragraph(f"<b>Slide {i}: {slide['title']}</b>", styles['Heading2'])
        )

        elements.append(
            Paragraph(
                slide["content"].replace("\n", "<br/>"),
                styles['BodyText']
            )
        )

        elements.append(
            Paragraph(
                f"<b>Visual Idea:</b> {slide['visual']}",
                styles['Italic']
            )
        )

        elements.append(Spacer(1, 20))

    doc.build(elements)

    buffer.seek(0)

    return buffer

# --- Generate Button ---
if st.button("🚀 Generate Carousel", type="primary"):

    if not topic.strip():
        st.error("Please enter a topic.")
    elif not reference_text.strip():
        st.error("Please paste at least one reference carousel.")
    else:
        # Step 1: Analyze
        with st.spinner("🔍 Step 1/3 — Analyzing reference carousels..."):
            style_profile = analyze_references(reference_text)

        if not style_profile:
            # Show actual error if available
            if "last_gemini_error" in st.session_state:
                st.error(f"❌ API Error: {st.session_state.last_gemini_error}")
            else:
                st.error("❌ Failed to analyze references. Check your API key and ensure GEMINI_API_KEY is set.")
            st.stop()

        st.success("✅ Style profile extracted!")
        with st.expander("📊 View Extracted Style Profile"):
            st.json(style_profile)

        # Step 2: Write
        with st.spinner("✍️ Step 2/3 — Writing carousel slides..."):
            raw_carousel = write_carousel(topic, style_profile, num_slides)

        if not raw_carousel:
            if "last_gemini_error" in st.session_state:
                st.error(f"❌ API Error during writing: {st.session_state.last_gemini_error}")
            else:
                st.error("❌ Failed to generate carousel. Try again or check your API key.")
            st.stop()

        # Step 3: Review
        with st.spinner("🔍 Step 3/3 — Reviewing and improving slides..."):
            final_carousel = review_carousel(raw_carousel, style_profile)

        if not final_carousel:
            st.error("Failed during review step. Showing raw output instead.")
            final_carousel = raw_carousel

        st.success("🎉 Carousel ready!")
        st.divider()

        # --- Display Output ---
        st.subheader(f"📱 Your LinkedIn Carousel: *{topic}*")

        slides = final_carousel.get("slides", [])
        for i, slide in enumerate(slides):
            label = "🎯 CTA Slide" if slide.get("is_cta") else f"Slide {i + 1}"
            with st.container(border=True):
                st.markdown(f"### {label}: {slide.get('title', '')}")
                st.markdown(slide.get("content", ""))
                st.caption(f"🖼️ Visual idea: {slide.get('visual', 'N/A')}")

        st.divider()

        pdf_file = create_pdf(final_carousel)

        st.download_button(
            label="📄 Download Carousel as PDF",
            data=pdf_file,
            file_name="carousel.pdf",
            mime="application/pdf"
        )

        # Download as JSON
        st.download_button(
            label="⬇️ Download Carousel (JSON)",
            data=json.dumps(final_carousel, indent=2),
            file_name="carousel.json",
            mime="application/json"
        )
