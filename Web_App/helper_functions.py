def interpret_prediction(prediction):
    """
    Convert a prediction (0 or 1) into a sentiment label ('negative' or 'positive')
    """
    # turn list of probabilities into a single string 
    prediction = str(prediction)
    return prediction

def preprocess_text(text):
    """
    Preprocess text: remove punctuation, convert to lowercase, and return as a list of words
    import string
    return text.translate(str.maketrans('', '', string.punctuation)).lower().split()
    """
    # Return text as a list 
    return [text]
    