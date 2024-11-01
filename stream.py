import streamlit as st
from main import scrape_website, extract_body_content, clean_body_content, split_dom_content, parse_with_ollama,extract_image_urls
from urllib.parse import urlparse, parse_qs

# Retrieve URL from the query parameter
query_params = st.experimental_get_query_params()
default_url = query_params.get("url", [""])[0]  # Default to an empty string if "url" parameter isn't provided

st.title("Gym Web Scraper")
# Use the default_url as the initial value for the input field
url = st.text_input("Enter Website URL", value=default_url)

if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)
        st.session_state.dom_content = cleaned_content
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
        images = extract_image_urls(dom_content)
        if images:
            st.subheader("Images Found on the Website:")
            for img in images:
                st.image(img["url"], caption=img["alt_text"])
        else:
            st.write("No images found on the website.")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_ollama(dom_chunks, parse_description)
            st.write(parsed_result)
