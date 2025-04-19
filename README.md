## Polarity Based Categorical Financial Dictionaries

This repository features the dictionaries as well as a simple script to gather statistics from them, associated with our paper, *Constructing a Polarity Based Dictionary for Financial Language*, authored by Chenhui Lucy Li and Amir Amel-Zadeh. You may find the paper here: 
http://ssrn.com/abstract=5162485

Our ambition for this project is to develop an open-source set of dictionaries for quantifying and analyzing financial language in noisy texts. Particularly, for each category of financial indicators, we look into how positive or negative the description of performance is. 

Existing resources like the Loughran McDonald dictionary provide general sentiment analysis. We intend to develop an alternative set of relational dictionaries that consist of comprehensive financial metrics. We build a general-purpose financial language dictionary using 87,834 management disclosure and analysis sections from 1998 to 2021. By incorporating relevant financial indicators, we demonstrate that our dictionaries accurately reflect financial performance. This toolkit will benefit organizations and researchers grappling with limited computing resources, enabling them to extract and quantify features from financial texts more effectively.

The dictionaries are classified to be categorical and modifying. 

Our categorical dictionaries consist of accounting vocabularies that are specifically associated with eight categories of financial indicators. These categories include "Bottom line," "Direct," "Financing," "Investing," "Operations," "Payout," and "Revenue growth." Each category contains phrases and terms related to the respective financial indicator.

In addition to the eight categories, our dictionaries also include modifiers that enhance or reverse the sentiment attached to the phrases. The modifiers are further divided into "amplifiers," "negators," "bads," and "goods." Amplifiers enhance the positive or negative meaning of a performance outcome, while negators reverse the sentiment. The "bads" and "goods" categories contain words that are inherently negative or positive, respectively.

These dictionaries, which we refer to as "modifiers" dictionaries, differ from the sentiment vocabulary in the Loughran McDonald dictionary. Our dictionaries capture specific modifiers like "increase" and "decrease," which impact financial indicators, whereas the Loughran McDonald dictionary focuses on sentiment-rich unigrams like "amazing" and "horrible." By including these modifiers and expanding the vocabulary, we provide a more comprehensive toolkit for analyzing financial language.

### Instructions on running our codes

To clone the repository, use the following command:

```bash
git clone https://github.com/chenhuililucy/Categorical-Financial-Dictionaries.git
```
Install the latest version of nltk:

```python
pip install nltk==3.8.1
```

Please ensure that you are in the ```Categorical-Financial-Dictionaries``` directory. The ```Categorical-Financial-Dictionaries/example_input``` directory should include the 10-K management discussion and analysis (MD&A) sections (or, potentially, any other text you want to analyse). You may like to have more MD&A sections from EDGAR, we have prepared more of them for you in https://github.com/chenhuililucy/MDA. 

At the top of the script, please define the topic you want to study, for example: 

```python
topic = "investing"
```
The topic can also be set to "bottom_line", "direct", "efficiency", "financing", "investing", "operations", "payout", or "revenue_growth".

Subsequently, you may run:

```python
python3 search.py
```
Your console should print the list of files being processed:

```python
example_input/20-2001mda.txt
example_input/20-2001mda.txt
example_input/20-1999mda.txt
example_input/20-1999mda.txt
example_input/20-1997mda.txt
example_input/20-1997mda.txt
example_input/20-2003mda.txt
example_input/20-2003mda.txt
example_input/20-1996mda.txt
example_input/20-1996mda.txt
```

After the script finishes running, you should find the files "words.csv" that includes example phrases that are matched, as well as "{topic}-per-sentence-metrics.csv" which produces a word count of the vocabulary within each category. Notice that the csv is at a sentence level, further processing will be needed to convert it into a document by document level. A further csv called "words.csv" will be created, showing you some example phrases that are identified from the search.

A small function to convert the metrics to document level is included in search.py named as finalcount(), you may need to modify this to satisfy your own needs. 

## Collaboration 

As the dictionaries are constructed objectively, we are open to any suggestions / edits you would like to make towards them, we welcome any edits made to the search code as well. To amend the dictionary through a pull request to the repository, follow these steps:

## 1. Fork the Repository:

Start by navigating to the original repository on GitHub, which is https://github.com/chenhuililucy/Categorical-Financial-Dictionaries. Click on the "Fork" button in the top-right corner to create a copy of the repository under your GitHub account.


Clone Your Fork:
Clone your forked repository to your local machine using the following command (replace <your-username> with your GitHub username):

```bash
git clone https://github.com/<your-username>/Categorical-Financial-Dictionaries.git
```

## 2. Commit and Push Changes:
After you've made your changes, commit them to your local repository using the following commands:

```bash
git add .
git commit -m "Describe the changes you made"
git push origin master
```

Navigate to your forked repository on GitHub and click on the "Pull Request" tab. Then click the "New Pull Request" button. GitHub will compare the changes you made in your fork with the original repository. Ensure that the base repository is set to the original repository, and the base branch is the branch you want to merge into (usually, it's "master"). One of the maintainers of the repository will review your PR.

