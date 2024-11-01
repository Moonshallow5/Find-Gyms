from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = Options()
options.headless = True  # Run in headless mode for faster execution

# Automatically download and set up ChromeDriver

def scrape_website(website):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    try:
        driver.get(website)
        html=driver.page_source
        return html
    finally:
        driver.quit()
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    body_content=soup.body
    if body_content:
        return str(body_content)
    else:
        return ""
def clean_body_content(body_content):
    soup=BeautifulSoup(body_content,'html.parser')
    for script_or_style in soup(["script","style"]):
        script_or_style.extract()
    cleaned_content=soup.get_text(separator="\n")
    cleaned_content="\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())
    return cleaned_content

def extract_image_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    for img_tag in soup.find_all("img"):
        img_url = img_tag.get("src")
        alt_text = img_tag.get("alt", "No description")
        if img_url:
            images.append({"url": img_url, "alt_text": alt_text})
    return images

def split_dom_content(dom_content,max_length=6000):
    return[
        dom_content[i:i+max_length] for i in range(0,len(dom_content),max_length)
    ]
    
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


model=OllamaLLM(model="llama3.2")
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)



def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
    
    

