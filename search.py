# Libraries imported
import re
import glob
import os
import csv
from collections import defaultdict
from nltk.tokenize import word_tokenize
import logging
import nltk
nltk.download('punkt')

# ======================     Category.    ======================    #
# Please change this according to the category you are tracking
# Available categories are:

# bottom_line
# direct
# efficiency
# financing
# investing
# operations
# payout
# revenue_growth

topic = "investing"

# =====================       YOUR INPUT FILES          =================== #

# The corpus is the main folder that contains all your text files
corpus = "example_input/*.txt"

negator = "modifiers_dictionaries/negatorfinal.csv"
amplifier = "modifiers_dictionaries/amplifiedfinal.csv"
bad = "modifiers_dictionaries/bad.csv"
good = "modifiers_dictionaries/good.csv"

negative = f'categorical_dictionaries/{topic}-neg.csv'
positive = f'categorical_dictionaries/{topic}-pos.csv'


# =====================       YOUR OUTPUT FILES          =================== #

# Define the name of your output csv
csv1 = f'{topic}-metrics.csv'

# ==================       LOAD DICTIONARY      ============================ #

# performance dictionaries
posperdict = defaultdict(list)
negperfdict = defaultdict(list)
amplifierset = set()
negatorset = set()
badset = set()
goodset = set()

# LM dictionaries
LMpositive = set()
LMnegative = set()

logger = logging


def read_dictinonaries():
    """
    Read in the list of dictionaries
    positive/negative dictionary consists of bigrams/unigrams
    the modifier dictionaires consist of unigrams only
    """
    with open(positive, "r") as posfile:
        records = csv.reader(posfile)
        for row in records:
            posperf = row[0].lower()
            # case where word consists of a bi-gram
            if len(posperf.split(" ")) > 1:
                w1 = posperf.split(" ")[0]
                w2 = posperf.split(" ")[1]
            else:
                # case where word consists of a uni-gram
                w1 = posperf
                w2 = "."
            posperdict[w1].append(w2)

    with open(negative, "r") as negfile:
        records = csv.reader(negfile)
        for row in records:
            negperf = row[0].lower()
            if len(negperf.split(" ")) > 1:
                w1 = negperf.split(" ")[0]
                w2 = negperf.split(" ")[1]
            else:
                w1 = negperf
                w2 = "."
            negperfdict[w1].append(w2)

    with open(bad, "r") as badf:
        records1 = csv.reader(badf)
        for row in records1:
            badf1 = row[0].lower()
            badset.add(badf1)

    with open(good, "r") as goodf:
        records1 = csv.reader(goodf)
        for row in records1:
            goodf1 = row[0].lower()
            goodset.add(goodf1)

    with open(amplifier, "r") as ampfile:
        records1 = csv.reader(ampfile)
        for row in records1:
            amplifier1 = row[0].lower()
            amplifierset.add(amplifier1)

    with open(negator, "r") as negfile:
        records1 = csv.reader(negfile)
        for row in records1:
            negator1 = row[0].lower()
            negatorset.add(negator1)

    with open("modifiers_dictionaries/LMpositive.csv", "r") as posfile:
        poswords = csv.reader(posfile)
        for row in poswords:
            singleposperword = row[0].lower()
            LMpositive.add(singleposperword)

    with open("modifiers_dictionaries/LMnegative.csv", "r") as negfile:
        negwords = csv.reader(negfile)
        for row in negwords:
            singlenegperfword = row[0].lower()
            LMnegative.add(singlenegperfword)


# =========================================================================== #


def check_presence(dictionary, ww, i, a, b):
    """
        Check the presence of words in a dictionary and perform corresponding operations.

    Args:
        dictionary (dict): The dictionary to check against.
        ww (list): The list of words.
        i (int): Current index.
        a (int): Offset.
        b (int): Offset.

    Returns:
        tuple: A tuple containing:
        i (int): the updated index,
        polarity_count (list): a list of consisting of the total word length for each of the 8 possibilities in a given sentence
        check_ (list): a list containing example phrases that is matched within each category
        check_polarity (list): a list consisting of the classification (eg. amp_pos, neg_pos) of example phrases
        result (int): overall polarity of this particular phrase (1 for positive, -1 for negative)
    """

    global polarity_cnt
    global check_
    global check_polarity

    # ======================================================= #

    # case where matched result is a bigram
    if ww[i + b] in dictionary[ww[i].lower()]:
        if dictionary == posperdict:
            if ww[i + a + b] in amplifierset:
                polarity_cnt[0] += sum([a, b])
                check_polarity.append("amp_pos")
            elif ww[i + a + b] in negatorset:
                polarity_cnt[2] += sum([a, b])
                check_polarity.append("neg_pos")
            elif ww[i + a + b] in badset:
                polarity_cnt[6] += sum([a, b])
                check_polarity.append("bad_pos")
            elif ww[i + a + b] in goodset:
                polarity_cnt[4] += sum([a, b])
                check_polarity.append("good_pos")
            check_.append(ww[i : i + a + b + 1])
            i = i + a + b
            return i, polarity_cnt, check_, check_polarity, 1

        elif dictionary == negperfdict:
            if ww[i + a + b] in amplifierset:
                polarity_cnt[1] += sum([a, b])
                check_polarity.append("amp_neg")
            elif ww[i + a + b] in negatorset:
                polarity_cnt[3] += sum([a, b])
                check_polarity.append("neg_neg")
            elif ww[i + a + b] in badset:
                polarity_cnt[7] += sum([a, b])
                check_polarity.append("bad_neg")
            elif ww[i + a + b] in goodset:
                polarity_cnt[5] += sum([a, b])
                check_polarity.append("good_neg")
            
            check_.append(ww[i : i + a + b + 1])
            i = i + a + b
            return i, polarity_cnt, check_, check_polarity, -1
        # ================================================== #

    elif "." in dictionary[ww[i].lower()]:
        if dictionary == posperdict:
            polarity_map = {
                tuple(amplifierset): ("amp_pos", 0, 1),
                tuple(negatorset): ("neg_pos", 2, -1),
                tuple(badset): ("bad_pos", 6, -1),
                tuple(goodset): ("good_pos", 4, 1)
            }
        elif dictionary == negperfdict:
            polarity_map = {
                tuple(amplifierset): ("amp_neg", 1, -1),
                tuple(negatorset): ("neg_neg", 3, 1),
                tuple(badset):("bad_neg", 7, -1),
                tuple(goodset): ("good_neg", 5, 1)
            }
        for set_, (description, index, polarity) in polarity_map.items():
            if ww[i + b] in set_:
                polarity_cnt[index] += b
                check_.append(ww[i: i + b + 1])
                check_polarity.append(description)
                i += b
                return i, polarity_cnt, check_, check_polarity, polarity


def check_existence(dictionary, temp, ww, i, a, b):
    global polarity_cnt
    global check_
    global check_polarity
    if ww[i].lower() in dictionary and i + a + b < len(ww):
        if dictionary.get(ww[i + b]):
            if ww[i + a + b] in dictionary[ww[i + b]]:
                if dictionary == negperfdict and temp == -1:
                    polarity_cnt[3] += sum([a, b])
                    check_polarity.append("neg_neg")
                elif dictionary == negperfdict and temp == 1:
                    polarity_cnt[1] += sum([a, b])
                    check_polarity.append("amp_neg")
                elif dictionary == posperdict and temp == -1:
                    polarity_cnt[2] += sum([a, b])
                    check_polarity.append("neg_pos")
                elif dictionary == posperdict and temp == 1:
                    polarity_cnt[0] += sum([a, b])
                    check_polarity.append("amp_pos")
                elif dictionary == posperdict and temp == 2:
                    polarity_cnt[4] += sum([a, b])
                    check_polarity.append("good_pos")
                elif dictionary == negperfdict and temp == 2:
                    polarity_cnt[5] += sum([a, b])
                    check_polarity.append("good_neg")
                elif dictionary == posperdict and temp == -2:
                    polarity_cnt[6] += sum([a, b])
                    check_polarity.append("bad_pos")
                elif dictionary == negperfdict and temp == -2:
                    polarity_cnt[7] += sum([a, b])
                    check_polarity.append("bad_neg")
                check_.append(ww[i : i + a + b + 1])
                i = i + a + b
                return i, polarity_cnt, check_, check_polarity
            elif "." in dictionary[ww[i + b]]:
                if dictionary == negperfdict and temp == -1:
                    polarity_cnt[3] += b
                    check_polarity.append("neg_neg")
                elif dictionary == negperfdict and temp == 1:
                    polarity_cnt[1] += b
                    check_polarity.append("amp_neg")
                elif dictionary == posperdict and temp == -1:
                    polarity_cnt[2] += b
                    check_polarity.append("neg_pos")
                elif dictionary == posperdict and temp == 1:
                    polarity_cnt[0] += b
                    check_polarity.append("amp_pos")
                elif dictionary == posperdict and temp == 2:
                    polarity_cnt[4] += b
                    check_polarity.append("good_pos")
                elif dictionary == negperfdict and temp == 2:
                    polarity_cnt[5] += b
                    check_polarity.append("good_neg")
                elif dictionary == posperdict and temp == -2:
                    polarity_cnt[6] += b
                    check_polarity.append("bad_pos")
                elif dictionary == negperfdict and temp == -2:
                    polarity_cnt[7] += b
                    check_polarity.append("bad_neg")
                check_.append(ww[i : i + b + 1])
                i = i + b
                return i, polarity_cnt, check_, check_polarity
    return None


def searchwords():
    """
    Searches for specific tokens in the text
    """

    global polarity_cnt
    global check_
    global check_polarity

    read_dictinonaries()
    sentlog_outputfields = [
        "filename",
        "sentnolist",
        "amp_pos",
        "amp_neg",
        "neg_pos",
        "neg_neg",
        "bad_pos",
        "bad_neg",
        "good_pos",
        "good_neg",
        "LMpositivesent",
        "LMnegtivesent",
        "positive_perf",
        "negative_perf",
        "verbose_good",
        "verbose_bad",
        "total_sent_cnt",
        "sentlen",
    ]
    amp_pos = []
    amp_neg = []
    neg_pos = []
    neg_neg = []
    bad_pos = []
    bad_neg = []
    good_pos = []
    good_neg = []
    polarity_cnt = [0] * 8


    # ===== augmented june 30 2021 ======== #

    v_bad = 0
    v_good = 0
    # ===================================== #

    verbose_bad = []
    verbose_good = []

    LMpositivesent = []
    LMnegativesent = []

    check_ = []
    check_polarity = []
    # ===================================== #

    positive_perf = []
    negative_perf = []


    sentnolist = []
    total_sent_cnt = []
    filename = []
    sentlen = []
    filenum = 1  # correct as filenum
    f_out = open(csv1, "w")
    wr = csv.writer(f_out)
    wr.writerow(sentlog_outputfields)

    for files in glob.glob(corpus):
        print(files)
        logger.info(files)
        with open(files) as f:
            print(files)

            try:
                content = f.read()
                filenum = filenum + 1

                content = re.sub("\n", "", content)  # remove whitespace
                sent = re.split("(?<=[a-z])\\.\\s+", content)
                # declare variables to record
                polarity_cnt = [0] * 8
                LMposcnt = 0
                LMnegcnt = 0
                sentno = 0

                # ===== augmented june 30 2021 ======== #

                v_bad = 0
                v_good = 0
                # ===================================== #

                attributioncnt = [0, 0, 0, 0]

                for sentences in sent:
                    
                    positive_perf_phrase = 0
                    negative_perf_phrase = 0
                    
                    sentno += 1

                    total_sent = 1
                    ww = []
                    for r in word_tokenize(sentences):
                        if r.isalpha():
                            ww.append(r.lower())

                    if len(ww) >= 1:
                        sentnolist.append(sentno)
                        if sentno == 1:
                            filename.append(files)
                        else:
                            filename.append("none")

                        # conduct LM dictionary search
                        for i in range(len(ww)):
                            if ww[i].lower() in LMpositive:
                                logger.info("LMpositive")
                                logger.info(ww[i])
                                LMposcnt += 1
                            if ww[i].lower() in LMnegative:
                                logger.info("LMnegative")
                                logger.info(ww[i])
                                LMnegcnt += 1

                        # for perf
                        a = 0
                        i = 0
                        b = 0

                        while i + a + b < len(ww):
                            
                            record_bad = True
                            record_good = True                        
                            
                            Continue_Search = True
                            # search in window of 3 words
                            for b in range(1, 3):
                                for a in range(1, 3):
                                    if Continue_Search:
                                        # add to the positive/negative dictionary
                                        if ww[i].lower() in negatorset and i + a + b < len(
                                            ww
                                        ):
                                            temp = -1
                                            ans = check_existence(
                                                negperfdict, temp, ww, i, a, b
                                            )
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                ) = ans
                                                Continue_Search = False
                                                positive_perf_phrase += 1
                                                break
                                            
                                            ans = check_existence(
                                                posperdict, temp, ww, i, a, b
                                            )
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                ) = ans
                                                Continue_Search = False
                                                negative_perf_phrase += 1
                                                break
                                        elif ww[
                                            i
                                        ].lower() in amplifierset and i + a + b < len(ww):
                                            temp = 1
                                            ans = check_existence(
                                                posperdict, temp, ww, i, a, b
                                            )
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                ) = ans
                                                Continue_Search = False
                                                positive_perf_phrase += 1
                                                
                                                break
                                            ans = check_existence(
                                                negperfdict, temp, ww, i, a, b
                                            )                                   
                                            
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                ) = ans
                                                Continue_Search = False
                                                negative_perf_phrase += 1
                                                break
                                        elif ww[i].lower() in badset and i + a + b < len(
                                            ww
                                        ):
                                            temp = -2
                                            
                                            ans = check_existence(
                                                posperdict, temp, ww, i, a, b
                                            )
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                ) = ans
                                                Continue_Search = False
                                                negative_perf_phrase += 1
                                                break
                                            
                                            ans = check_existence(
                                                negperfdict, temp, ww, i, a, b
                                            )
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                ) = ans
                                                Continue_Search = False
                                                negative_perf_phrase += 1
                                                break
                                            
                                            if record_bad :
                                                v_bad += 1
                                                record_bad = False

                                        elif ww[i].lower() in goodset and i + a + b < len(
                                            ww
                                        ):

                                            temp = 2
                                            
                                            ans = check_existence(
                                                posperdict, temp, ww, i, a, b
                                            )
                                            
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                ) = ans
                                                Continue_Search = False
                                                positive_perf_phrase += 1
                                                break
                                            ans = check_existence(
                                                negperfdict, temp, ww, i, a, b
                                            )
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                ) = ans
                                                Continue_Search = False
                                                positive_perf_phrase += 1
                                                break
                                            
                                            if record_good:
                                                v_good += 1
                                                record_good = False

                                        elif negperfdict.get(
                                            ww[i].lower()
                                        ) and i + a + b < len(ww):
                                            ans = check_presence(negperfdict, ww, i, a, b)
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                    perf
                                                ) = ans
                                                if perf == 1:
                                                    positive_perf_phrase += 1
                                                elif perf == -1:
                                                    negative_perf_phrase += 1
                                                Continue_Search = False
                                                break
                                            

                                        elif posperdict.get(
                                            ww[i].lower()
                                        ) and i + a + b < len(ww):
                                            ans = check_presence(posperdict, ww, i, a, b)
                                            if ans:
                                                (
                                                    i,
                                                    polarity_cnt,
                                                    check_,
                                                    check_polarity,
                                                    perf
                                                ) = ans
                                                if perf == 1:
                                                    positive_perf_phrase += 1
                                                elif perf == -1:
                                                    negative_perf_phrase += 1
                                                Continue_Search = False
                                                break

                            i += 1
                            record_good = True
                            record_bad = True

                        amp_pos.append(polarity_cnt[0])
                        amp_neg.append(polarity_cnt[1])
                        neg_pos.append(polarity_cnt[2])
                        neg_neg.append(polarity_cnt[3])
                        bad_pos.append(polarity_cnt[6])
                        bad_neg.append(polarity_cnt[7])
                        good_pos.append(polarity_cnt[4])
                        good_neg.append(polarity_cnt[5])

                        positive_perf.append(positive_perf_phrase)
                        negative_perf.append(negative_perf_phrase)

                        LMpositivesent.append(LMposcnt)
                        LMnegativesent.append(LMnegcnt)

                        verbose_bad.append(v_bad)
                        verbose_good.append(v_good)
                        total_sent_cnt.append(total_sent)

                        polarity_cnt = [0] * 8
                        LMposcnt = 0
                        LMnegcnt = 0

                        v_bad = 0
                        v_good = 0

                        attributioncnt = [0, 0, 0, 0]
                        sentlen.append(len(ww))

                    else:
                        sentno -= 1
            except UnicodeDecodeError:
                print("Error")

    p = zip(
        filename,
        sentnolist,
        amp_pos,
        amp_neg,
        neg_pos,
        neg_neg,
        bad_pos,
        bad_neg,
        good_pos,
        good_neg,
        LMpositivesent,
        LMnegativesent,
        positive_perf,
        negative_perf,
        verbose_good,
        verbose_bad,
        total_sent_cnt,
        sentlen,
    )
    for row in p:
        wr.writerow(row)

    with open("words.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(zip(check_, check_polarity))


searchwords()



