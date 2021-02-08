

from paragraphs import combine_paragraph
from paragraphs import split_paragraph
from nltk.tokenize import sent_tokenize




if __name__ == '__main__':
    # result = combine_paragraph(paragraphs, min_words_len=3)
    # print(result)
    paragraphs = ["In 2017 there were 120 cases of measles.",
                  "In 2016, there were 86.",
                  "In 2015, there were 188 cases.",
                  "In 2014 there were 667 cases of measles, no cases of encephalitis, and no death.",
                  "In 2013 there were 189 cases of measles, no encephalitis and no death.",
                  "I could go on, but you get the point. By and large, measles is an unpleasant rash with a fever but it isn’t deadly. The clinical definition doesn’t support that and neither do the facts. By comparison, as of March 1, 2012 there were 842 serious injuries following the MMR vaccine and 140 deaths. Between 1990 and 2014, were more than 6,058 serious adverse events reported to the Vaccine Adverse Events Reporting System (VAERS). That’s significant when you consider that only 1-10% of adverse events are actually reported to this system. "]

    result = combine_paragraph(paragraphs, 10)

    print(result[0])
    print()
    print(result[1])
    print()
    print(result[2])