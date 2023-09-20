from bs4 import BeautifulSoup
import tqdm
import requests
import pandas as pd
#Generate Search Page Links
keywords = ['Financial Analyst','Investment Banking','Asset Management','Taxation','Portfolio Management','Credit Analysis','Private Equity','Derivatives','Risk Management','Financial Planning',
            'Corporate Finance','Accounting','Auditing','Hedge Funds','Wealth Management','Fixed Income','Equity Research','Financial Modeling','Compliance Officer','Quantitative Analysis',
            'Financial Controller','Actuarial Science','Mergers and Acquisitions','Capital Markets','Software Engineer','Data Scientist','Systems Administrator','AI',
            'Front-End Developer','IT Project Manager','Software Architect','Blockchain','Web Developer','Network Engineer','Cloud Computing','Machine Learning','Back-End Developer',
            'UX/UI Designer','QA','IoT','Cybersecurity Analyst','Database Administrator','DevOps Engineer','Big Data','Full-Stack Developer',
            'Mobile App Developer','IT Support Specialist','Network Security']
total_pages_per_category = 2
keywords = list(set(keywords))
refined_keywords =[x.replace("/","%2F").replace(" ","+").lower() for x in keywords]
url_dict = {z:[f"https://www.postjobfree.com/resumes?q={x}&l=&radius=25&p={y}" for y in range(total_pages_per_category)] for x,z in zip(refined_keywords,keywords)}

#Fetch Resume Links
data = pd.DataFrame()
for keywrd in keywords:
    urls = url_dict[keywrd]
    resume_links = []
    for url in tqdm.tqdm(urls,desc=keywrd):
        c = requests.get(url).content
        soup = BeautifulSoup(c, 'html5lib') 
        resume_links.extend(["https://www.postjobfree.com"+x.find('h3',{'class':'itemTitle'}).find('a')['href'] for x in soup.findAll('div',attrs = {'class':'snippetPadding'})])
    tmp = pd.DataFrame()
    tmp['resume_link']=resume_links
    tmp['keyword'] = keywrd
    data = pd.concat([data,tmp])
data.to_excel('ResumeLinks.xlsx',index=False)
    