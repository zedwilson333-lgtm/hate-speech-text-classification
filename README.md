# Schapelle Corby Web Scraping and Data Analysis Project

## Overview
This project examined online discussion surrounding the Schapelle Corby case by collecting and analysing publicly available user-generated content from online platforms. The project focused on how high-profile criminal cases are discussed online, including themes around justice, legality, media influence, public opinion and hate-related discourse.

## Purpose
The aim of this project was to develop a structured and ethical framework for identifying, collecting, storing and analysing case-related online information. The project also explored the practical challenges of collecting online data within digital forensics, including ethical limits, platform restrictions, API access, cost barriers and data availability.

## Tools and Methods
This project used both programmed and web-based scraping methods, including:

- Python
- Scrapy
- JSON data storage
- ParseHub
- Browse AI
- Octoparse
- Apify
- Data cleaning and preprocessing
- Hate term categorisation
- Hate intensity scoring
- Data visualisation and analysis

## Method
The project involved:

1. Identifying relevant public online platforms and sources
2. Reviewing platform rules, ethical constraints and scraping limitations
3. Creating standardised search terms for consistency
4. Collecting publicly available posts, comments and text data
5. Storing collected data in structured formats such as JSON
6. Cleaning and preprocessing the dataset using Python
7. Categorising hate-related terms into themes
8. Comparing scraping methods based on data yield and practicality
9. Analysing trends, frequency, severity and platform limitations

## Key Findings
The project found that ethical, technical and financial constraints strongly affected the data that could be collected. Reddit and browser-based scraping tools produced the largest amount of accessible discussion data, while Python scraping was more limited when dealing with JavaScript-heavy sites, CAPTCHAs and restricted platforms.

The analysis also found that most collected content had low hate intensity overall. Discussion was more often focused on case-related, legal, familial and crime-based themes rather than explicit hate speech. This suggested that the dataset reflected public narrative and news-style reporting more than highly extreme online abuse.

## Digital Forensics Relevance
This project is relevant to digital forensics because it highlights the real-world difficulties involved in collecting online evidence responsibly. Investigators may face platform restrictions, privacy concerns, legal limitations, API costs and inconsistent access to online data. By comparing multiple scraping methods, this project demonstrates why flexible and ethical data collection frameworks are important in modern digital investigations.

## Repository Structure
- `data/` - cleaned or sample data, where appropriate to share
- `docs/` - reports and supporting documents
- `presentations/` - presentation files
- `src/` - Python scraper
- `results/` - Raw analysed hate results and screenshots
- `workflow/` - workflow files or process documentation

## Ethical Considerations
This project used publicly available information and was completed for educational purposes. Public files have been reviewed to remove unnecessary personal information, student numbers and group member details where appropriate.

## Future Improvements
Future work could expand the dataset, include more platforms, improve reproducibility, and integrate machine learning methods for automated hate speech detection or real-time monitoring.
