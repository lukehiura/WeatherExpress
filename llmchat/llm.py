import redis
import spacy
from textblob import TextBlob


# Initialize a Redis client
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Maximum size of the circular buffer
MAX_BUFFER_SIZE = 10

# Function to add user input and bot response to the circular buffer in Redis
def add_to_circular_buffer(user_input, bot_response):
    conversation = {
        'user_input': user_input,
        'bot_response': bot_response
    }

    # Add the conversation to the circular buffer
    redis_client.lpush('circular_buffer', conversation)

    # Trim the circular buffer to the maximum size
    redis_client.ltrim('circular_buffer', 0, MAX_BUFFER_SIZE - 1)


def get_conversation_history(user_input, entities):
    # Retrieve the circular buffer from Redis
    circular_buffer = get_circular_buffer()

    # Logic to maintain conversation history and store relevant information
    # This can be stored in a database or a global variable for context retention
    # Example implementation:
    conversation_history = {
        'user_input': user_input,
        'entities': entities,
        'circular_buffer': circular_buffer
    }
    return conversation_history


def construct_prompt(user_input, weather_dict, conversation_history):
    prompt = f"Describe what the weather is like in {user_input}. "
    prompt += f"It is {weather_dict['weather_summary']} with a high of {weather_dict['high_temp_pm']}°C in the afternoon, {weather_dict['high_temp_am']}°C in the morning, and {weather_dict['high_temp_night']}°C at night. "
    prompt += f"The low temperature ranges from {weather_dict['low_temp_am']}°C in the morning, {weather_dict['low_temp_pm']}°C in the afternoon, to {weather_dict['low_temp_night']}°C at night. "
    prompt += f"The humidity is {weather_dict['humidity_pm']}% in the afternoon, {weather_dict['humidity_am']}% in the morning, and {weather_dict['humidity_night']}% at night. "
    prompt += f"{weather_dict['weather_description']}"

    # Add conversation history for context-aware responses
    if conversation_history:
        prompt += f"\n\nPrevious User Input: {conversation_history['user_input']}"
        prompt += f"\nEntities: {', '.join(conversation_history['entities'])}"

        # Add circular buffer to the prompt
        circular_buffer = conversation_history['circular_buffer']
        for index, conversation in enumerate(circular_buffer):
            prompt += f"\n\nPrevious Conversation {index+1}:"
            prompt += f"\nUser Input: {conversation['user_input']}"
            prompt += f"\nBot Response: {conversation['bot_response']}"

    prompt += "\n\nWhat type of clothing would you recommend for this weather? Should I bring an umbrella? Please provide detailed information about the exact temperature and humidity."
    prompt += f"Also, could you suggest some fun things to do around {user_input}? Please describe in detail."

    return prompt


# Function to retrieve the circular buffer (conversation history) from Redis
def get_circular_buffer():
    circular_buffer = redis_client.lrange('circular_buffer', 0, -1)
    return [eval(conversation.decode()) for conversation in circular_buffer]



def perform_sentiment_analysis(text):
    sentiment_score = analyze_sentiment(text)
    if sentiment_score > 0.3:
        return 'positive'
    elif sentiment_score < -0.3:
        return 'negative'
    else:
        return 'neutral'

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score


def generate_emotional_response(response, sentiment):
    if sentiment == 'positive':
        emotional_response = "That's great to hear! " + response
    elif sentiment == 'negative':
        emotional_response = "I'm sorry to hear that. " + response
    else:
        emotional_response = response
    return emotional_response

if __name__=='__main__':
    # Rest of the functions remain unchanged

    # Example usage:
    nlp = spacy.load('en_core_web_sm')

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

    conversation_history = get_conversation_history(user_input, entities)
    prompt = construct_prompt(user_input, weather_dict, conversation_history)

    print(prompt)
