
def t_countries(c):   
    # nothing to translate
    country_dict = {
        "Man (Isle of)": "Isle of Man",
        "Netherlands The":"Netherlands",
    }
    if c in country_dict:
        return country_dict[c]
    
    return c
