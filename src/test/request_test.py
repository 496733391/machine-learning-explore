#! /usr/bin/python
# -*- coding: utf-8 -*-

import requests
import pandas as pd

# url = 'https://www.scopus.com/author/affilHistory.uri?auId=55574234356'

url = 'https://www.scopus.com/onclick/export.uri?oneClickExport=%7b%22Format' \
      '%22%3a%22CSV%22%2c%22SelectedFields%22%3a%22+' \
      'Authors++' \
      'AuthorIds++' \
      'Title++' \
      'Year++' \
      'EID++' \
      'SourceTitle++' \
      'Volume+' \
      'Issue+' \
      'ArtNo+' \
      'PageStart+' \
      'PageEnd+' \
      'PageCount++' \
      'CitedBy++' \
      'DocumentType+' \
      'Source++' \
      'PublicationStage++' \
      'DOI++' \
      'ACCESSTYPE++' \
      'Affiliations++' \
      'ISSN+' \
      'ISBN+' \
      'CODEN++' \
      'PubMedID++' \
      'Publisher++' \
      'Editors++' \
      'LanguageOfOriginalDocument++' \
      'CorrespondenceAddress++' \
      'AbbreviatedSourceTitle++' \
      'Abstract++' \
      'AuthorKeywords++' \
      'IndexKeywords++' \
      'Number++' \
      'Acronym++' \
      'Sponsor++' \
      'Text++' \
      'Manufacturers+' \
      'Tradenames++' \
      'ChemicalsCAS+' \
      'MolecularSequenceNumbers++' \
      'ConferenceName+' \
      'ConferenceDate+' \
      'ConferenceLocation+' \
      'ConferenceCode+' \
      'Sponsors++' \
      'References+' \
      'Link+' \
      '%22%2c%22View%22%3a%22SpecifyFields%22%7d&origin=AuthorProfile&zone=exportDropDown&dataCheckoutTest=' \
      'false&sort=plf-f&tabSelected=docLi&authorId=7102137996&txGid=316a75b60daf488f1e81f3689ae2859b'

# url = 'https://www.scopus.com/results/authorNamesList.uri?origin=searchauthorlookup&src=al&edit=&poppUp=&basi' \
#       'cTab=&affiliationTab=&advancedTab=&' \
#       'st1=liu&' \
#       'st2=bo&' \
#       'institute=wuhan+university' \
#       '&orcidId=&authSubject=LFSC&_authSubject=on&authSubject=HLSC&_authSubject=on&authSubject=PHSC&_authSubjec' \
#       't=on&authSubject=SOSC&_authSubject=on&s=AUTHLASTNAME%28liu%29+AND+AUTHFIRST%28bo%29&sdt=al&sot=al&se' \
#       'archId=42a0860e2008958faf4e6c644b496275&exactSearch=on&sid=42a0860e2008958faf4e6c644b496275'


proxies = {
            "http": "http://202.120.43.93:8059"
}

headers = {
            'cookie': '__cfduid=dbf2e076d5187308fd7dff007b95013a91588830445; scopus.machineID=C95FAA82D76902CFBA9'
                      'ADB44D5C59CF2.wsnAw8kcdt7IPYLO0V48gA; optimizelyEndUserId=oeu1588830449793r0.7402451939845718; '
                      'optimizelyBuckets=%7B%7D; xmlHttpRequest=true; optimizelySegments=%7B%22278797888%22%3A%22gc%'
                      '22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22refe'
                      'rral%22%7D; SCSessionID=A337037364551016112E02E0A97F04B0.wsnAw8kcdt7IPYLO0V48gA; scopusSess'
                      'ionUUID=4762980f-f2ac-4e6e-9; AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB19B012A28DAFC'
                      '444A412FCD01D4E3F0713B3EBC7E9702A35664A34B4B9FB3A2B010BA32070D9964CEACBAE7C5777723B7EDAD7BF'
                      '5F528F7FCE6B9C1A140CFB7AC; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; AMCV_4D6368F454EC41'
                      '940A4C98A6%40AdobeOrg=1075005958%7CMCIDTS%7C18394%7CMCMID%7C2361211320004507033053132432291'
                      '0847678%7CMCAAMLH-1589770475%7C11%7CMCAAMB-1589770475%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHa'
                      'MWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1589172875s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1185074918%7CvVe'
                      'rsion%7C4.4.1; __cfruid=795ee9dcb0f81c1ddbf14fc7b41116a4d9dbe034-1589166500; check=true; ja'
                      'vaScript=true; screenInfo="1080:1920"; mbox=PC#0d2fc3c7b0294bd788e2024d386337d6.22_0#16524'
                      '11309|session#1bc8ea1efad24cb39f40f1448c48083a#1589167320; optimizelyPendingLogEvents=%5B%'
                      '5D; s_sess=%20c21%3Dlastname%253Dliu%2526firstname%253Dbo%2526affiliation%253Dwuhan%2520u'
                      'niversity%3B%20e13%3Dlastname%253Dliu%2526firstname%253Dbo%2526affiliation%253Dwuhan%2520u'
                      'niversity%253A1%3B%20c13%3Ddocument%2520count%2520%2528high-low%2529%3B%20s_cpc%3D0%3B%20e'
                      '41%3D1%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Aauthor%252520results%252C39%252'
                      'C39%252C1337%252C1920%252C937%252C1920%252C1080%252C1%252CP%3B%20s_ppv%3Dsc%25253Arecord%25'
                      '253Aauthor%252520details%252C18%252C18%252C937%252C771%252C937%252C1920%252C1080%252C1%252'
                      'CL%3B; s_pers=%20c19%3Dsc%253Arecord%253Aauthor%2520details%7C1589168308873%3B%20v68%3D158'
                      '9166507244%7C1589168308891%3B%20v8%3D1589166880269%7C1683774880269%3B%20v8_s%3DLess%2520th'
                      'an%25207%2520days%7C1589168680269%3B',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrom'
                          'e/81.0.4044.138 Safari/537.36'
}

text = requests.get(url,
                    proxies=proxies,
                    headers=headers,
                    timeout=300,
                    )

with open('result1.csv', 'w', encoding='utf-8') as js:
    js.write(text.text)

df = pd.read_csv('result.csv', na_values=0, keep_default_na=False)
print(df)
