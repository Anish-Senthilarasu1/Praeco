import streamlit as st
from github import Github
from datetime import datetime
import re

REPO_NAME = "Anish-Senthilarasu1/Praeco"
CATEGORY_PAGES = {
    "News": "news.html",
    "Opinion": "opinion.html",
    "Lifestyle": "lifestyle.html",
    "Entertainment": "entertainment.html"
}

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "_", text.strip())
    return text[:60]

def parse_body(raw_text):
    paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
    html_parts = []
    for p in paragraphs:
        # Section headers: short line ending with colon
        if p.endswith(":") and "\n" not in p and len(p) < 80:
            html_parts.append(
                f'<h2 class="text-2xl font-bold mt-10 mb-4" style="font-family: \'Times New Roman\', serif;">{p}</h2>'
            )
        else:
            p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
            p = re.sub(r"\*(.+?)\*", r"<em>\1</em>", p)
            p = p.replace("\n", "<br>")
            html_parts.append(f'<p class="text-lg leading-relaxed mb-6">{p}</p>')
    return "\n\n            ".join(html_parts)

def generate_article_html(title, author, date_str, image_filename, body_html, refs_html=""):
    refs_section = ""
    if refs_html:
        refs_section = f"""
            <div class="mt-10 pt-6 border-t border-gray-400">
                <h2 class="text-xl font-bold mb-4" style="font-family: 'Times New Roman', serif;">References</h2>
                <ul class="text-sm leading-relaxed space-y-3 text-gray-700">
                    {refs_html}
                </ul>
            </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - The Praeco</title>
    <link rel="icon" type="image/png" href="praecoLogo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Exo+2:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html, body {{ height: 100%; margin: 0; padding: 0; overflow-x: hidden; background: #eae6ff; }}
        .source-serif {{ font-family: "Source Serif 4", serif; }}
        body {{ font-family: "Times New Roman", serif; background-color: #eae6ff; }}
        @media (max-width: 768px) {{ .navbar-content {{ flex-direction: column; align-items: center; }} }}
        @media (max-width: 640px) {{ .navbar-title {{ font-size: 1.5rem; }} .navbar-links {{ gap: 1rem; }} }}
    </style>
</head>
<body class="bg-[#eae6ff] min-h-screen">
    <div class="sticky top-0 z-30 bg-white shadow-md px-4 md:px-6 py-3">
        <div class="flex justify-between items-center navbar-content max-w-7xl mx-auto">
            <h1 class="source-serif text-3xl md:text-5xl font-semibold text-left flex items-center navbar-title">
                PRAECO
                <img src="praecoLogo.png" alt="Praeco Logo" class="ml-2 h-10 md:h-14">
            </h1>
            <div class="flex gap-3 md:gap-6 navbar-links">
                <a href="about_us.html" class="text-gray-700 hover:text-black transition-colors duration-300 font-semibold text-base md:text-xl">About Us</a>
                <a href="contact_us.html" class="text-gray-700 hover:text-black transition-colors duration-300 font-semibold text-base md:text-xl">Contact Us</a>
            </div>
        </div>
    </div>

    <div class="max-w-4xl mx-auto px-6 py-12">
        <h1 class="text-4xl font-bold mb-4" style="font-family: 'Times New Roman', serif;">{title}</h1>
        <div class="flex items-center gap-4 mb-4">
            <a href="#" class="text-[#8B7FD4] hover:text-[#6B5EAF]" style="font-family: 'Times New Roman', serif;">{author}</a>
            <span class="text-gray-600" style="font-family: 'Times New Roman', serif;">{date_str}</span>
        </div>
        <div class="mb-8">
            <img src="{image_filename}" alt="{title}" class="w-full h-[400px] object-cover rounded-lg shadow-lg">
        </div>
        <article class="prose prose-lg max-w-none" style="font-family: 'Times New Roman', serif;">
            {body_html}{refs_section}
        </article>
    </div>

    <div class="fixed bottom-8 right-8">
        <a href="index.html" class="bg-[#8B7FD4] text-white px-6 py-3 rounded-full hover:bg-[#6B5EAF] transition-colors duration-300 shadow-lg">
            Back to Home
        </a>
    </div>
</body>
</html>"""

def generate_card_html(article_filename, image_filename, title, author):
    return f"""        <a href="{article_filename}" class="relative rounded-lg shadow-xl h-[300px] sm:h-[350px] lg:h-[400px] transition-transform duration-300 transform scale-100 hover:scale-105">
            <img class="block h-full w-full object-cover rounded-lg opacity-40" src="{image_filename}" alt="{title}">
            <div class="absolute inset-0 flex flex-col justify-center h-full p-4 sm:p-6">
                <p class="font-['Playfair_Display'] text-black text-xl sm:text-2xl lg:text-3xl mb-auto leading-tight">{title}</p>
                <p class="font-['Playfair_Display'] text-black text-sm sm:text-base lg:text-lg mb-4">By: {author}</p>
            </div>
        </a>"""

def update_category_page(repo, category_page, new_card_html):
    file = repo.get_contents(category_page)
    content = file.decoded_content.decode("utf-8")
    marker = '<div id="articles-grid"'
    idx = content.find(marker)
    if idx == -1:
        return False
    end_of_tag = content.find(">", idx) + 1
    new_content = content[:end_of_tag] + "\n" + new_card_html + "\n" + content[end_of_tag:]
    repo.update_file(
        category_page,
        f"Add article card: {new_card_html[:60]}",
        new_content,
        file.sha,
        branch="main"
    )
    return True


# ── UI ──────────────────────────────────────────────────────────────────────

st.set_page_config(page_title="Praeco Publisher", page_icon="📰", layout="centered")

st.markdown("""
    <style>
        .block-container { max-width: 720px; }
        .stButton > button {
            background-color: #8B7FD4;
            color: white;
            border: none;
            border-radius: 9999px;
            padding: 0.6rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            width: 100%;
        }
        .stButton > button:hover { background-color: #6B5EAF; }
    </style>
""", unsafe_allow_html=True)

st.title("📰 Praeco Publisher")
st.markdown("Fill in the fields and hit **Publish** — the article goes live automatically.")
st.divider()

with st.form("publish_form"):
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Article Title *", placeholder="Gene Editing: Here's What We Know")
        author = st.text_input("Author *", placeholder="Rabia Ghanchi")
    with col2:
        date_input = st.date_input("Date *", value=datetime.today())
        category = st.selectbox("Category *", list(CATEGORY_PAGES.keys()))

    image_filename = st.text_input("Image Filename *", placeholder="gene_edit.png  (upload the image to the repo separately)")

    body_text = st.text_area(
        "Article Body *",
        placeholder="Paste your article here.\n\nSeparate paragraphs with a blank line.\n\nUse *italic* and **bold** for emphasis.\n\nSection headers: end a short line with a colon:",
        height=420
    )

    references_text = st.text_area(
        "References (optional — one per line)",
        placeholder='Broad Institute. "CRISPR Timeline." Broad Institute, 2018.',
        height=100
    )

    submitted = st.form_submit_button("🚀 Publish Article")

if submitted:
    missing = [f for f, v in [("Title", title), ("Author", author), ("Image filename", image_filename), ("Article body", body_text)] if not v.strip()]
    if missing:
        st.error(f"Missing required fields: {', '.join(missing)}")
    else:
        try:
            token = st.secrets["GITHUB_TOKEN"]
            g = Github(token)
            repo = g.get_repo(REPO_NAME)

            article_slug = slugify(title)
            article_filename = f"{article_slug}.html"
            date_str = date_input.strftime("%B %-d, %Y")
            body_html = parse_body(body_text)

            refs_html = ""
            if references_text.strip():
                lines = [r.strip() for r in references_text.strip().split("\n") if r.strip()]
                refs_html = "\n                    ".join(f"<li>{line}</li>" for line in lines)

            article_html = generate_article_html(title, author, date_str, image_filename, body_html, refs_html)

            with st.spinner("Publishing..."):
                # Check if file already exists
                try:
                    repo.get_contents(article_filename)
                    st.error(f"`{article_filename}` already exists in the repo. Rename your article slightly or delete the old file first.")
                    st.stop()
                except Exception:
                    pass

                repo.create_file(
                    article_filename,
                    f"Add article: {title}",
                    article_html,
                    branch="main"
                )

                card_html = generate_card_html(article_filename, image_filename, title, author)
                update_category_page(repo, CATEGORY_PAGES[category], card_html)

            st.success(f"✅ Published! Live at: https://www.thepraeco.com/{article_filename}")
            st.info(f"Remember to upload **{image_filename}** to the repo if you haven't already.")

        except KeyError:
            st.error("GitHub token not found. Make sure `GITHUB_TOKEN` is set in your Streamlit secrets.")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
