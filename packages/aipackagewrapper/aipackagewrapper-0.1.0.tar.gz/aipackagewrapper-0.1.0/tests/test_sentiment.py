from modules.sentiment_analyzer_module import SentimentAnalyzer

def test_analyze_text_positive():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_text("I love this!")
    assert result == "positive"

def test_analyze_text_negative():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_text("I hate this!")
    assert result == "negative"

def test_analyze_text_neutral():
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze_text("It is a table.")
    assert result == "neutral"
