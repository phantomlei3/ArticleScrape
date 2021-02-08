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

### Agenda
1. Redo the logistic of duplicates and remove all duplicates
2. Use archive.org 
3. annotate anti-vaccinated websites (1 hour: 50 articles)

### Data Statistic
- Total: 11441
- 1. Vaxxter: 989 articles
- 2. Green Med Info: 2819 articles
- 3. Modern Alternative Mama: 912 articles
- 4. Thinking Moms Revolution: 1031 articles 
- 5. Ago Of Autism (www.ageofautism.com): 4698 articles (2014-2020)   \* Total 10741 (2007-2020) *\
- 6. Australian Vaccination-risks Network (avn.org.au): 300 articles
- 7. The Vaccine Reaction(thevaccinereaction.org): 312 articles
- 8. Kelly Brogan MD (kellybroganmd.com): 498 articles
- 9. Living Whole(www.livingwhole.org): 90 articles
- 10. Mom Across America(www.momsacrossamerica.com): 391 articles (Need to re-scrape)
- 11. Vactruth(vactruth.com): 1117 articles
- 12. Focus For Health(www.focusforhealth.org): 185 articles
- 13. CMSRI(info.cmsri.org): 43 articles (They also contains academic paper(pdf) that I cannot scrape)




- 14. Fearless Parent: 20 articles in archives

- 15. *The Healthy Home Economist: 110 articles (switched to membership-only on 12/10/2020)
- 16. *National Vaccine Information Center(): use javascript to display more articles (need a different way to scrape)
- 17. *Mercola: use javascript to display more articles (need a different way to scrape)

- 20. *Children Health Defense (childrenshealthdefense.org): *membership-only


https://childrenshealthdefense.org/defender/

-- 18. *Vaccines Risk Awareness: Page not found(by using Felicia's Method). I also cannot find any blog/article from this website except manual and guide.

- 21. *Immunity (www.immunity.org.uk): *PDF format(academic journals)


- 22. *Immunity Education(immunityeducationgroup.org): *36 articles and all of them are published on 2019-10-16

## Anti-vaccine Articles (Word Extraction)
#### By using methods metioned in https://dl.acm.org/doi/pdf/10.3115/1119282.1119287
#### p(word) = document frequency of one word / the number of documents
#### informativeness score for one word = log(p(word) in anti-vax corpus / p(word) in wiki corpus)*p(word)
#### Add-one Smoothing: p(word) in wiki = (document frequency of one word + 1) / the number of documents

#### Related Articles: 11361     percent: 11361/14027 = 81%  


vaccine 1.9970773133704716
autism 1.6437303646129742
vaccines 1.6411273299144116
vaccination 1.0577197447292297
vactruth 0.7413375215456125
vaccinated 0.7313966423200544
vaxxter 0.6337753162808757
health 0.6208202843881787
please 0.5769047638661201
cdc 0.559920287196255
vaccinations 0.5379590401838544
thank 0.5333650794657457
know 0.5083223156785777
greenmedinfo 0.5032316750015554
disease 0.41828639086228087
vaccinate 0.41060188467540826
amp 0.3949242971290338
deductible 0.39437258507493167
subscribing 0.381388742663894
kids 0.37217173109706814
medical 0.37068097612921663
finders 0.3647606777174692
flu 0.3501429237231428
jeopardize 0.3464188337712815
immune 0.34143002421176627
moms 0.3384687448685796
mmr 0.33254344859639856
dachel 0.3231111580023788
pharma 0.3168336163199986
irrevocable 0.3138496547470645
pharmaceutical 0.3113521215937346
healthy 0.31130814117195904
measles 0.3000868758535321
children 0.2976091918471673
email 0.2952869095716385
patients 0.29358693732047364
doctors 0.29179707554130935
parents 0.29065770899780513
login 0.2888693881389342
recommend 0.28476468115313053
unvaccinated 0.28461409940702737
symptoms 0.26241951999874225
www 0.26026672497274017
mom 0.25989597949718335
adverse 0.25934275384617383
liabilities 0.25863627045686166
expended 0.2571494935640714
immunization 0.2554479803492131
autistic 0.25474778650845203
dr 0.2411445184526221


### Data Statistic
Total: 11441 articles
related-article filter: 10484 articles

For 10484 articles:
- 0 character limit: 395750 paragraphs
- 25 character limit: 186463 paragraphs
- 41 character limit: 174398 paragraphs
- 68 character limit:: 157549 paragraphs
- 100 character limit:: 142576 paragraphs
- 200 character limit:: 104690 paragraphs

For 10484 articles:
- 0 word limit: 395750 paragraphs
- 10 limit: 158362 paragraphs
- 20 word limit: 129602 paragraphs
- 30 word limit:: 105994 paragraphs
- 40 limit: 84717 paragraphs
- 50 word limit: 66307 paragraphs
- 60 word limit:: 51088 paragraphs

For 10484 articles (no char limit and word limit):
Longest paragraph in characters: 9166 character
Longest paragraph in words: 1522 words
Shortest paragraph in characters: 1 characters
Shortest paragraph in words: 1 words

Average number of paragraphs per article: 19.93256390690576 paragraphs



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

