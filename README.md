## Polarity Based Financial Dictionaries

This repository features the dictionaries as well as a simple script to gather statistics from them, associated with our paper, *Constructing a Polarity Based Dictionary for Financial Language*, authored by Chenhui Lucy Li and Amir Amel-Zadeh

Our ambition for this project is to develop an open-source toolkit for quantifying and analyzing financial language in noisy texts. Existing resources like the Loughran McDonald dictionary only provide sentiment analysis, lacking comprehensive financial metrics. We build a general-purpose financial language dictionary using 87,834 management disclosure and analysis sections from 1998 to 2021. By incorporating relevant financial indicators, we demonstrate that our dictionaries accurately reflect financial performance. This toolkit will benefit organizations and researchers grappling with limited computing resources, enabling them to extract and quantify features from financial texts more effectively.

The dictionaries are classified to be categorical and modifying. 

Our categorical dictionaries consist of accounting vocabularies that are specifically associated with seven categories of financial indicators. These categories include "Bottom line," "Direct," "Financing," "Investing," "Operations," "Payout," and "Revenue growth." Each category contains phrases and terms related to the respective financial indicator.

In addition to the seven categories, our dictionaries also include modifiers that enhance or reverse the sentiment attached to the phrases. The modifiers are further divided into "amplifiers," "negators," "bads," and "goods." Amplifiers enhance the positive or negative meaning of a performance outcome, while negators reverse the sentiment. The "bads" and "goods" categories contain words that are inherently negative or positive, respectively.

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

