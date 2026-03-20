import streamlit as st
import requests
import time
import random
import urllib.parse

headers = {"User-Agent": "Mozilla/5.0"}

# -----------------------------
# GOOGLE SUGGEST
# -----------------------------
def google_suggest(q, country):
    try:
        url = f"https://suggestqueries.google.com/complete/search?client=firefox&hl=en-GB&gl={country}&q={urllib.parse.quote(q)}"
        return requests.get(url, headers=headers).json()[1]
    except:
        return []

# -----------------------------
# FILTER
# -----------------------------
def is_valid_query(q):
    q = q.lower()

    blocked = ["walgreens", "walmart", "cvs", "wawa", "fda"]
    countries = ["usa", "canada", "australia", "germany", "france", "italy", "spain"]
    foreign = ["kaufen", "preis", "avis", "comprar", "precio"]

    if any(x in q for x in blocked):
        return False
    if any(x in q for x in countries):
        return False
    if any(x in q for x in foreign):
        return False

    return True

# -----------------------------
# PREFIXES (FULL FUNNEL)
# -----------------------------
prefixes = [
    "how", "what", "why", "when", "where", "who",
    "is", "are", "can", "does", "do",
    "what is", "what does", "how does",
    "why is", "why does",
    "how good is", "is it worth it",
    "is it good", "is it better than",
    "difference between", "compare", "vs",
    "best", "top", "recommended",
    "price", "cost", "how much",
    "where to buy", "buy", "cheap",
    "deal", "discount", "offer",
    "near me", "for sale",
    "what features does", "what options are",
    "reviews of", "opinions on"
]

# -----------------------------
# UI
# -----------------------------
st.title("Search Scraper I")

product = st.text_input("Enter Product Name")
country = st.selectbox("Select Country", ["uk", "us"])

if st.button("Find Customer Queries"):

    if not product:
        st.warning("Please enter a product")
    else:
        product = product.lower()
        results = set()

        queries = set()

        for p in prefixes:
            queries.add(f"{p} {product}")
            queries.add(f"{p} {product} {country}")

        queries.update([
            product,
            f"{product} price",
            f"{product} review",
            f"{product} features",
            f"{product} vs",
            f"{product} alternatives"
        ])

        with st.spinner("Scraping search queries..."):
            for q in queries:
                suggestions = google_suggest(q, country)

                for s in suggestions:
                    s = s.lower().strip()

                    if product in s and is_valid_query(s):
                        results.add(s)

                time.sleep(random.uniform(0.2, 0.5))

        final = sorted(results)

        st.success(f"Found {len(final)} queries")

        for i, q in enumerate(final[:150], 1):
            st.write(f"{i}. {q}")
