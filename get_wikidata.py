#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 21:53:43 2017
@author: vidhya
This script is used for generating textual contents for each celebrity using Wikipedia.
"""
import os
import requests
from bs4 import BeautifulSoup
import pyexcel as pe
import re

#--------------------------------------------------------------------------------------------------------------------------------
# This function uses mediawiki API provided by Wikipedia to check if a wikipedia page could be found for a given celebrit name.
#--------------------------------------------------------------------------------------------------------------------------------
def processURL(str, missingFlag,readerHandle):
    
        page = requests.get("https://en.wikipedia.org/w/api.php?action=query&format=xml&prop=pageprops&redirects&titles={0}".format(str))
        soup = BeautifulSoup(page.content, 'html.parser')
   
        if len(soup.api.contents) == 0:
             print("page has symbols") 
       
        elif "missing" in soup.page.attrs or "invalid" in soup.page.attrs:
            
            if missingFlag == 0:
               strCaps = str.title()
               missingFlag = 1
               processURL(strCaps, missingFlag, readerHandle)
            else:
               print("page not found")
     
        elif len(soup.page.contents) > 0:
        
            if "disambiguation" in soup.pageprops.attrs:
                print("page disambiguation")
            else:
                processData(str,readerHandle)
   
#        elif len(soup.page.contents) > 0 or (len(soup.page.contents) == 0 and "redirects" in soup.query.attrs):
        elif len(soup.page.contents) == 0:
            # Scrap the required contents from the wikipedia page found            
            processData(str,readerHandle)


#--------------------------------------------------------------------------------------------------------------------------------
# This function uses mediawiki API to collect the introduction section and the related categories from a Wikipedia celebrity page.
#--------------------------------------------------------------------------------------------------------------------------------
def processData(celebrity_str,readerHandle):
           
           # Get the celebrity name
           celebrity_name = celebrity_str
           
           # Create a directory for each user and store the input for further processing
           file_name = celebrity_name+".txt"
           dir_path  = "polls/input/"+readerHandle+"/list"
           if not os.path.exists(dir_path):
                 os.makedirs(dir_path)
           file = open("polls/input/"+readerHandle+"/list/"+file_name, 'w')
           
           # Get the categories section of a celebrity wikipedia page using Mediawiki API
           page1 = requests.get("https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=categories&redirects&cllimit=max&titles={0}".format(celebrity_name))
           
           # Parse all HTML entities using BeautifulSoup           
           soup1        = BeautifulSoup(page1.content, 'html.parser')
           category_tag = soup1.find_all('cl')
           for category in category_tag:
               categoryname       = category['title']
               celebrity_category = categoryname.encode('ascii', 'ignore').decode('ascii')
               # Remove punctuations and numbers from the text data
               category_output = re.sub('[^A-Za-z_]+', ' ', celebrity_category).strip().lower()
               # Append text data to output file
               file.write(category_output+' ')
           
           # Get the entire introduction section of a celebrity wikipedia page using Mediawiki API
           page2 = requests.get("https://en.wikipedia.org/w/api.php?format=xml&action=query&prop=extracts&redirects&exintro=&explaintext=&titles={0}".format(celebrity_name))
           
           # Parse all HTML entities using BeautifulSoup
           soup2 = BeautifulSoup(page2.content, 'html.parser')
           out   = soup2.find_all('extract')[0].string
           if out is not None:
              out_en  = out.encode('ascii', 'ignore').decode('ascii')
              # Remove punctuations and numbers from the text data
              intro_output = re.sub('[^A-Za-z_]+', ' ', out_en).strip().lower()
              # Append text data to output file
              file.write(intro_output)

           file.close()
