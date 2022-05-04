from tabula.io import read_pdf
import pandas as pd
import re

filepath = "./list_of_bc_hospitals.pdf"
tables = read_pdf(filepath, pages="1-14", lattice=True, silent=True)

city = []
postalCode = []
name = []
healthAuthority = []

authorities = ["Fraser Health Authority", 
                "Vancouver Island Health Authority", 
                "Interior Health Authority",
                "Vancouver Coastal Health Authority",
                "Northern Health Authority",
                "Provincial Health Services Authority",
                "Providence Health Care Society"]


# functions to extract information from a cell

extractCity = lambda x: x.split("\r",1)[0] # split string by carriage return '\r' and retrieve first line

extractPostalCode = lambda x: re.findall("[A-Z][0-9][A-Z] [0-9][A-Z][0-9]", x)[0] # find postal code by matching regex

def extractName(x): # find name of hospital by returning substring before health authority
    x = x.replace("\r", " ")
    i = 0
    for a in authorities:
        if a in x: 
            i = x.index(a)
            return x[:i]
    return 'St. Joseph’s General Hospital' # corner case

def extractHealthAuthority(x): # check if a known health authority is within the column and return the name
    x = x.replace("\r", " ")
    
    if 'St. Joseph’s General Hospital' in x: # corner case
        return "Vancouver Island Health Authority"
    
    for a in authorities:
        if a in x:
            return a
    return "No Authority Found"



# iterate over each table found in the pdf and collect data from the cells

for i, table in enumerate(tables):
    
    columnOne = list(tables[i].iloc[:,0])
    
    cities = map(extractCity, columnOne)
    city += cities
    
    postalCodes = map(extractPostalCode, columnOne) 
    postalCode += postalCodes
    
    columnTwo = list(tables[i].iloc[:,1])
    
    healthAuthorities = map(extractHealthAuthority, columnTwo)
    healthAuthority += healthAuthorities
    
    names = map(extractName, columnTwo)
    name += names

data = {'city': city, 'postal_code': postalCode,
        'hospital_name': name, 'health_authority': healthAuthority}

df = pd.DataFrame(data)

df.to_csv('hospital_list.csv', index=False)
