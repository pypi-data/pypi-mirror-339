from textblob import TextBlob

class SentimentAnalyzer:
    def analyze_text(self, text):
        """
            Analyzes the sentiment of a single text.
            Parameters:            
                text (str): The text to analyze.
            Returns: 
                str: Sentiment label ('positive', 'negative', or 'neutral').
        """
    
        # Clean text and create a TextBlob object
        blob = TextBlob(text.lower())
    
        # Calculate sentiment polarity (-1 to 1)
        polarity = blob.sentiment.polarity
    
        # Determine sentiment based on polarity
        if polarity > 0:
            return 'positive'
        elif polarity < 0:
            return 'negative'
        else:
            return 'neutral'
        
    def analyze_batch(self, texts):
        """
        Processes a batch of texts and aggregates sentiment results.
    
        Parameters:
            texts (list of str): List of texts to analyze.
    
        Returns:
            dict: Aggregated sentiment counts and percentages.
        """
        results = {"positive": 0, "negative": 0, "neutral": 0}
    
        get_sentiment = lambda polarity: 'positive' if polarity > 0 else ('negative' if polarity < 0 else 'neutral')

        for text in texts:
            blob = TextBlob(text.lower())
            polarity = blob.sentiment.polarity
            sentiment = get_sentiment(polarity)
            results[sentiment] += 1

        # Calculate percentages
        total = len(texts)
        percentages = {k: (v / total) * 100 for k, v in results.items()}
    
        return {"counts": results, "percentages": percentages}
