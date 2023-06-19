import redis
import spacy
from textblob import TextBlob


class ConversationManager:
    def __init__(self, host='localhost', port=6379, db=0, max_buffer_size=10):
        self.redis_client = redis.Redis(host=host, port=port, db=db)
        self.MAX_BUFFER_SIZE = max_buffer_size

    def add_to_circular_buffer(self, user_input, bot_response):
        conversation = {
            'user_input': user_input,
            'bot_response': bot_response
        }
        self.redis_client.lpush('circular_buffer', conversation)
        self.redis_client.ltrim('circular_buffer', 0, self.MAX_BUFFER_SIZE - 1)

    def get_circular_buffer(self):
        circular_buffer = self.redis_client.lrange('circular_buffer', 0, -1)
        return [eval(conversation.decode()) for conversation in circular_buffer]

    def get_conversation_history(self, user_input, entities):
        circular_buffer = self.get_circular_buffer()
        conversation_history = {
            'user_input': user_input,
            'entities': entities,
            'circular_buffer': circular_buffer
        }
        return conversation_history

    def construct_prompt(self, user_input, weather_dict, conversation_history):
        prompt = f"User Input: {user_input}\n"

        prompt += f"Weather Summary: {weather_dict['weather_summary']}\n"
        prompt += f"High Temperature (Afternoon): {weather_dict['high_temp_pm']}°C\n"
        prompt += f"High Temperature (Morning): {weather_dict['high_temp_am']}°C\n"
        prompt += f"High Temperature (Night): {weather_dict['high_temp_night']}°C\n"
        prompt += f"Low Temperature (Morning): {weather_dict['low_temp_am']}°C\n"
        prompt += f"Low Temperature (Afternoon): {weather_dict['low_temp_pm']}°C\n"
        prompt += f"Low Temperature (Night): {weather_dict['low_temp_night']}°C\n"
        prompt += f"Humidity (Afternoon): {weather_dict['humidity_pm']}%\n"
        prompt += f"Humidity (Morning): {weather_dict['humidity_am']}%\n"
        prompt += f"Humidity (Night): {weather_dict['humidity_night']}%\n"
        prompt += f"Weather Description: {weather_dict['weather_description']}\n"

        if conversation_history:
            prompt += "Conversation History:\n"
            prompt += f"Previous User Input: {conversation_history['user_input']}\n"
            prompt += f"Entities: {', '.join(conversation_history['entities'])}\n"

            circular_buffer = conversation_history['circular_buffer']
            for index, conversation in enumerate(circular_buffer):
                prompt += f"Previous Conversation {index+1}:\n"
                prompt += f"User Input: {conversation['user_input']}\n"
                prompt += f"Bot Response: {conversation['bot_response']}\n"

        prompt += "\nPlease provide recommendations for clothing suitable for this weather. Do I need to bring an umbrella? Please provide details about the temperature and humidity. Additionally, suggest some fun things to do around the location mentioned above."

        return prompt


    def perform_sentiment_analysis(self, text):
        sentiment_score = self.analyze_sentiment(text)
        if sentiment_score > 0.3:
            return 'positive'
        elif sentiment_score < -0.3:
            return 'negative'
        else:
            return 'neutral'

    def analyze_sentiment(self, text):
        blob = TextBlob(text)
        sentiment_score = blob.sentiment.polarity
        return sentiment_score

    def generate_emotional_response(self, response, sentiment):
        if sentiment == 'positive':
            emotional_response = "That's great to hear! " + response
        elif sentiment == 'negative':
            emotional_response = "I'm sorry to hear that. " + response
        else:
            emotional_response = response
        return emotional_response


# Example usage:
if __name__=='__main__':
    manager = ConversationManager()

    user_input = "What is the weather like today?"
    entities = []

    weather_dict = {
        'weather_summary': 'Sunny',
        'weather_description': 'The weather is clear with no clouds.',
        'high_temp_pm': 25,
        'high_temp_am': 20,
        'high_temp_night': 18,
        'low_temp_pm': 15,
        'low_temp_am': 12,
        'low_temp_night': 10,
        'humidity_pm': 50,
        'humidity_am': 55,
        'humidity_night': 60
    }

    conversation_history = manager.get_conversation_history(user_input, entities)
    prompt = manager.construct_prompt(user_input, weather_dict, conversation_history)

    print(prompt)