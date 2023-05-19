## Polarity Based Categorical Financial Dictionaries

This repository features the dictionaries as well as a simple script to gather statistics from them, associated with our paper, *Constructing a Polarity Based Dictionary for Financial Language*, authored by Chenhui Lucy Li and Amir Amel-Zadeh. You may find the paper here: https://drive.google.com/file/d/1UwgTCrnr__8iZqehFts-tNNzw0Kbu1Cg/view?usp=sharing

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

After the script finishes running, you should find the files "words.csv" that includes example phrases that are matched, as well as "{topic}-metrics.csv" which produces a word count of the vocabulary within each category. Notice that the csv is at a sentence level, further processing will be needed to convert it into a document by document level. 



