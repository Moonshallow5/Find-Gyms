# Find-Gyms

## 💡 What is this project about

I'm from Malaysia, and something I realized here is that we don't have a good system of gyms here. We have many gyms here but getting a membership and recurring subscriptions here are pretty expensive, not to mention going trough the websites of each gym is really tidious with content split everywhere.

## 🔧 What I implemented

This project works by utlizing API from the Google Cloud Console, I'm currently utiilizing Places API and Maps Javascript API

If a company registers itself as a Gym on Google, and is near a specific location, it'll be displayed as a red marker on Google Maps, as well as its other details; Name, Website, Rating. As well as my own website which is shown on the text "Analyze on Streamlit"

By pressing "Analyze on Streamlit" I've built a function which allows you to parse a website for all it's valuable content. The function utilizes Beautiful Soup and in the specific commpany website I am only scraping information in body while removing all tags with "script" and "style"

The textbox which asks for input utilizes Ollama to classify the input sentences correctly and produces a valid response depending on the data in the gym.

and you can ask questions about the website and receive the correct output.


## How to use the program

Enter your location and find gyms near you, and press Analyze on Streamlit to parse the data on the company website for you, and ask questions like " What are your membership prices" or "What are your opening hours" and get a valid output



## Future implementations

- Utilize geojson API so that for users can just input a an adress and get gyms close to that postcode 

- Fix web scraping data so the machine learning model can understand webscraping data better