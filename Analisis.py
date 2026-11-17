try:
    import colorama  # type: ignore[import-not-found]
    from colorama import Fore, Style  # type: ignore[import-not-found]
    colorama.init()
except ImportError:
    class _ColorFallback:
        def __getattr__(self, name):
            return ""

        RESET_ALL = ""

    colorama = type("ColoramaFallback", (), {"init": staticmethod(lambda *args, **kwargs: None)})()
    Fore = _ColorFallback()
    Style = _ColorFallback()

try:
    from textblob import TextBlob  # type: ignore[import-not-found]
except ImportError:
    TextBlob = None


def analyze_sentiment(text):
    if TextBlob is not None:
        return TextBlob(text).sentiment.polarity

    positive_words = {
        "good", "great", "happy", "love", "excellent", "amazing", "awesome",
        "wonderful", "fantastic", "joy", "excited", "positive", "beautiful",
        "nice", "kind", "fun", "smile", "success", "bright"
    }
    negative_words = {
        "bad", "terrible", "sad", "hate", "awful", "horrible", "angry",
        "negative", "upset", "disappointed", "pain", "worst", "poor", "boring",
        "stress", "fear", "failure", "ugly"
    }

    lowered = text.lower()
    score = 0.0

    for word in positive_words:
        if word in lowered:
            score += 0.25
    for word in negative_words:
        if word in lowered:
            score -= 0.25

    if "!" in text:
        score += 0.1 if score >= 0 else -0.1
    if "?" in text:
        score -= 0.05

    return max(-1.0, min(1.0, score))


print(f"{Fore.BLUE} Welcome to sentiment Spy! {Style.RESET_ALL}")
user_name = input(f"{Fore.MAGENTA} Please enter your name: {Style.RESET_ALL}")
if not user_name:
    user_name = "Mystery Agent"

conversation_history = []

if TextBlob is None:
    print(f"{Fore.YELLOW} TextBlob is not installed. Using built-in fallback sentiment analysis.{Style.RESET_ALL}")

print(f"{Fore.CYAN} Hello, Agent {user_name}!")
print("Type a sentence and I will analyze your sentences with TextBlob and show you the sentiment.")
print(f"Type {Fore.YELLOW}history{Fore.CYAN} or {Fore.YELLOW}exit{Fore.CYAN} to quit.{Style.RESET_ALL}\n")

while True:
    user_input = input(f"{Fore.GREEN}>> {Style.RESET_ALL}").strip()

    if not user_input:
        print(f"{Fore.RED}Please enter a valid sentence.{Style.RESET_ALL}")
        continue

    if user_input.lower() == "exit":
        print(f"{Fore.BLUE} Exiting Sentiment Spy. Goodbye, Agent {user_name}! {Style.RESET_ALL}")
        break

    if user_input.lower() == "history":
        if not conversation_history:
            print(f"{Fore.YELLOW} No conversation history yet. {Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN} Conversation History: {Style.RESET_ALL}")
            for idx, (text, polarity, sentiment_type) in enumerate(conversation_history, start=1):
                if sentiment_type == "Positive":
                    sentiment_color = Fore.GREEN
                    emoji = "😊"
                elif sentiment_type == "Negative":
                    sentiment_color = Fore.RED
                    emoji = "😞"
                else:
                    sentiment_color = Fore.YELLOW
                    emoji = "😐"

                print(f"{idx}. {sentiment_color}{emoji} {text} "
                      f"Polarity: {polarity:.2f}, {sentiment_type}{Style.RESET_ALL}")
        continue

    polarity = analyze_sentiment(user_input)

    if polarity > 0.25:
        sentiment_type = "Positive"
        color = Fore.GREEN
        emoji = "😊"
    elif polarity < -0.25:
        sentiment_type = "Negative"
        color = Fore.RED
        emoji = "😞"
    else:
        sentiment_type = "Neutral"
        color = Fore.YELLOW
        emoji = "😐"

    conversation_history.append((user_input, polarity, sentiment_type))
    print(f"{color}{emoji} {sentiment_type} sentiment detected! Polarity: {polarity:.2f}{Style.RESET_ALL}")
                        