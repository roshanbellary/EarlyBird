from agents import InterestClassifierAgent, HeadlineGeneratorAgent, DeepResearchAgent
from langchain.prompts import PromptTemplate

perplexity_api_key=os.getenv("PERPLEXITY_API_KEY")
openai_api_key=os.getenv("OPENAI_API_KEY")

test_component = 'interest_classifier'

# Interest Classifier
if test_component == 'interest_classifier':
    interest_classifier_prompt = PromptTemplate(
                input_variables=["user_interests"],
                template="""
                Generate a list of 3 topics based on the user's interests below. 
                These topics should be distinct relatively unrelated from eachother:
                {user_interests}
                
                The topics should be outputted as a list of strings.
                """
            )

    user_interests = 
    interest_classifier = InterestClassifierAgent(openai_api_key, interest_classifier_prompt)
    interests = interest_classifier.classify_interests(user_interests)

# Headline Generator
if test_component == 'headline_generator':
    headline_generator_prompt = PromptTemplate(
                input_variables=["news_item"],
                template="""
                Create an engaging headline for the following news item:
                {news_item}
                
                Make it catchy but informative, suitable for a podcast episode.
                """
            )

    news_items = 
    headline_generator = HeadlineGeneratorAgent(openai_api_key, headline_generator_prompt)
    headlines = headline_generator.generate_headlines(news_items)

# Researcher
if test_component == 'researcher':
    researcher_prompt = """
        Conduct deep research on the following news story:
        Headline: {headline}
        Summary: {summary}
        
        Provide:
        1. Historical context
        2. Expert opinions
        3. Related events
        4. Statistical data
        5. Future implications
        
        Format your response with clear sections.
        """
    researcher_generator = DeepResearchAgent(perplexity_api_key, researcher_prompt)