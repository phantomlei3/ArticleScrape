### Goals
- Re-scrape 10,678 anti-vaccination articles from 22 websites with clean contents
- Extend this corpus
    - Automatically identify the article components given a new website
    - Automatically scrape new anti-vaccination articles from X websites
    

### Design
- Article scraping
    - Base-line (finished): scrape article from given URL
        - Contents (still exists advertising and social media paragraphs)
        - Author names
        - *Comments
    - Advanced (developing): contents (pure article paragraphs)
- Relevant Article URL scraping
    - Idea:  Given a website, what are all anti-vaccination articles on this website?
    - Relevance Filter: Given a article title, what is the probability that it is a anti-vaccination article?


### Examples
#### Green Med Info
1. https://www.greenmedinfo.com/blog/how-will-unhealthy-americans-react-covid-19-vaccines
2. https://www.greenmedinfo.com/blog/invention-epidemic
#### Modern Alternative Mama
1. https://modernalternativemama.com/2018/07/25/how-to-get-a-vaccine-exemption-and-why-you-should/
2. https://modernalternativemama.com/2018/11/09/anti-vaxxers-are-bringing-back-disease-or-are-they/
#### Vaxxter
1. https://vaxxter.com/chilling-ingredient-in-covid19-vaccine/
2. https://vaxxter.com/fissures-emerge-in-the-covid-containment-plan/