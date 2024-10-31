from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

options = Options()
options.headless = True  # Run in headless mode for faster execution

# Automatically download and set up ChromeDriver

'''
def get_gym_details_with_selenium(url):
    driver.get(url)
    
    # Adding a delay to allow the page to fully load
    driver.implicitly_wait(5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the price elements using data-testid
    standard_price = soup.select_one('[data-testid="monthlyPrice-Standard"] strong')
    premium_price = soup.select_one('[data-testid="monthlyPrice-Premium"] strong')
    
    # Extract text if elements are found
    standard_price_text = standard_price.text if standard_price else "Standard price not available"
    premium_price_text = premium_price.text if premium_price else "Premium price not available"
    
    return {
        "standard_membership_price": standard_price_text,
        "premium_membership_price": premium_price_text
    }
'''    
'''
# Example usage
gym_url = "https://www.puregym.com/gyms/edinburgh-quartermile/"
gym_details = get_gym_details_with_selenium(gym_url)
print(gym_details)

driver.quit()
'''
'''
import re

def re_stuff(url):
    driver.get(url)
    
    # Adding a delay to allow the page to fully load
    driver.implicitly_wait(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Expanded pattern: capture surrounding text with each price
    price_pattern = re.compile(r"((?:\w+\s?){0,5})£(\d+\.\d{2})((?:\s?\w+){0,5})")

    # Get matches with context
    matches = price_pattern.findall(soup.text)

    # Process matches to find descriptive keywords
    prices_with_descriptions = []
    for before, price, after in matches:
        context = f"{before.strip()} {after.strip()}"
        # Check for keywords in the context
        if "core" in context.lower():
            description = "Core Membership"
        elif "off-peak" in context.lower():
            description = "Off-Peak"
        else:
            description = "Unknown"  # Fallback if no keyword matches
        
        prices_with_descriptions.append({
            "price": f"£{price}",
            "description": description,
            "context": context  # Optional, to see full context if needed
        })

    # Print or process the result
    for item in prices_with_descriptions:
        print(f"{item['description']}: {item['price']} (Context: {item['context']})")
'''
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
    
    


'''        
gym_url = "https://www.puregym.com/gyms/edinburgh-quartermile/"
gym_details = scrape_website(gym_url)
body_content = extract_body_content(gym_details)
cleaned_content = clean_body_content(body_content)  # Call the function here

# Now, split the cleaned content into chunks
dom_chunks = split_dom_content(cleaned_content)

# Pass dom_chunks to parse_with_ollama
parse_description = "how many machines/kits do you have?"
parsed_results = parse_with_ollama(dom_chunks, parse_description)

print(parsed_results)
'''
    
'''
def get_gym_details(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Customize these selectors based on each website’s HTML structure.
        membership_price = soup.select_one(".membership-price").text if soup.select_one(".membership-price") else "Not available"
        equipment_list = [item.text for item in soup.select(".equipment-item")]

        return {
            "membership_price": membership_price,
            "equipment": equipment_list
        }
    except Exception as e:
        print(f"Error fetching details from {url}: {e}")
        return None



gym_url = "https://www.puregym.com/gyms/edinburgh-quartermile/"  # Replace with an actual gym URL
gym_details = get_gym_details(gym_url)
print(gym_details)
'''