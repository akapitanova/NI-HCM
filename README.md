# Sentiment Analysis of Czech Websites  

## Authors  
**Anna Kapitánová & Tomáš Holas**  

## Project Goals  
- Perform sentiment analysis on scraped Czech websites  
- Compare sentiment differences between disinformation and mainstream news sources  
- Analyze sentiment trends during the 2023 Czech presidential election

📄 **For detailed analysis and results, see the presentation:** [HCM.pdf](HCM.pdf) 

## Web Scraping  
**Successfully Scraped Websites:**  
- `iDNES.cz`, `Lidovky.cz`, `Aktualně.cz` (Mainstream)  
- `AC24.cz`, `CzechFreePress.cz`, `Pravdive.cz`, `Zvedavec.news`, `Novarepublika.cz`, `ParlamentníListy.cz` (Disinformation)  

**Challenges in Scraping:**  
- Disinformation sites were harder to scrape (e.g., Aeronet blocked bot access attempts)  

## Sentiment Analysis  
- **Model:** `bert-base-multilingual-uncased-sentiment` (Hugging Face)  
- **Sentiment scale:** `-2` (negative) to `2` (positive)  

## Key Findings  
- **Disinformation sites** had stronger negativity (`-1.129` avg.) compared to **mainstream sites** (`-0.737` avg.)  
- **Main targets of negative sentiment:** `Petr Pavel` & `Danuše Nerudová`  
- **Pro-disinformation sentiment:** Support for `Jaroslav Bašta` & `Andrej Babiš`  
- **Common disinformation narratives:**  
  - NATO, EU, U.S. criticism  
  - Climate change denial  
  - Conspiracy theories (e.g., "global depopulation plan")  
