from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):

    scores = analyzer.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
        emoji = "😊"

    elif compound <= -0.05:
        sentiment = "Negative"
        emoji = "😠"

    else:
        sentiment = "Neutral"
        emoji = "😐"

    return {
        "sentiment": sentiment,
        "emoji": emoji,
        "score": compound
    }