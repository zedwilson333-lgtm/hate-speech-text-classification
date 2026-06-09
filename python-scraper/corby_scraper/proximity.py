import re

def near(text, term, window=2000):
    pattern = (
        rf"schapelle corby(.{{0,{window}}}){re.escape(term)}|"
        rf"{re.escape(term)}(.{{0,{window}}})schapelle corby"
    )
    return re.search(pattern, text) is not None
