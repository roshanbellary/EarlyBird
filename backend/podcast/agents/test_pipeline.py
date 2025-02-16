from interest_classifier import InterestClassifierAgent
from headline_generator import HeadlineGeneratorAgent
from researcher import DeepResearchAgent
from story_drafter import StoryDrafterAgent
from script_generator import PodcastScriptGenerator
from langchain.prompts import PromptTemplate

import os
import re
from dotenv import load_dotenv
load_dotenv()

perplexity_api_key=os.getenv("PERPLEXITY_API_KEY")
openai_api_key=os.getenv("OPENAI_API_KEY")
mistral_api_key=os.getenv("MISTRAL_API_KEY")
test_component = 'script_generator'

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

    user_interests = ["politics", "technology", "business"]
    interest_classifier = InterestClassifierAgent(openai_api_key, interest_classifier_prompt)
    interests = interest_classifier.interest_classify(user_interests)
    print(interests)

# Scraper
if test_component == 'scraper':
    # Change this shit dawg
    headline_generator_prompt = PromptTemplate(
                input_variables=["news_item"],
                template="""
                Create an engaging headline for the following news item:
                {news_item}
                
                Make it catchy but informative, suitable for a podcast episode.
                """
            )

    news_items = '<TOPIC>politics</TOPIC><TOPIC>technology</TOPIC><TOPIC>business</TOPIC>'
    headline_generator = HeadlineGeneratorAgent(openai_api_key, headline_generator_prompt)
    headlines = headline_generator.generate_headlines(news_items)
    print(headlines)

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
    
    headline = "City of Brotherly Love Soars: Philadelphia Honors Eagles After Super Bowl LIX Win"
    # headline = "Justice Served: Arrest made in brutal stabbing of beloved Cherry Hill veterinarian"
    # headline = "Breaking News: Russian Drone Breaches Chernobyl Nuclear Plant\'s Shield"
    # headline = "Breaking News: 3 Hostages Freed from Gaza Captivity - A Miraculous Escape!"
    # headline = "Breaking News: UN Urges Immediate Ceasefire in Gaza to Prevent Humanitarian Crisis"
    researcher = DeepResearchAgent(perplexity_api_key, researcher_prompt)
    researched_stories = researcher.research_stories(headlines)
    print(researched_stories)

# Story Drafter
if test_component == 'story_drafter':
    story_drafter_prompt = PromptTemplate(
            input_variables=["story_data"],
            template="""
            Draft a compelling podcast story based on this research:
            {story_data}
            
            Include:
            1. A hook to grab attention
            2. Clear narrative structure
            3. Key points and analysis
            4. Engaging transitions
            5. Thought-provoking conclusions
            """
        )

    researched_stories = """
    ## Conducting Deep Research on the News Story: "City of Brotherly Love Soars: Philadelphia 
    Honors Eagles After Super Bowl LIX Win"\n\nTo conduct a deep research on this news story, 
    we can break down the task into several key sections:\n\n### 1. Historical Context\n*Philadelphia\'s 
    Nickname: Philadelphia is known as the "City of Brotherly Love," a name derived from the Greek words 
    *phileo (love) and adelphos (brother), chosen by William Penn[1][3]. This nickname reflects the 
    city\'s historical emphasis on brotherly love and civic unity.\n\n### 2. Expert Opinions\n- 
    *Cultural Significance: Experts often highlight Philadelphia\'s rich cultural diversity and 
    historical significance, which contribute to its vibrant community[5].\n- **Sports Culture: 
    The city\'s passionate sports fans, particularly those supporting the Philadelphia Eagles,
     are known for their dedication and enthusiasm[3].\n\n### 3. Related Events\n- **Super Bowl 
     LIX Victory: If the Eagles won Super Bowl LIX, this would be a significant event for Philadelphia, 
     likely prompting widespread celebrations and community gatherings.\n- **Community Response: The 
     victory would likely be celebrated with parades, rallies, and other community events, showcasing 
     the city\'s spirit of brotherly love and civic pride.\n\n### 4. Statistical Data\n- **Economic 
     Impact: Large-scale events like Super Bowl victories can have a substantial economic impact on 
     the city, boosting local businesses and tourism.\n- **Social Impact: Such events often bring the 
     community together, reinforcing social bonds and civic engagement.\n\n### 5. Future Implications\n-
      **Community Engagement: The aftermath of a major sports victory can lead to increased community 
      engagement and civic participation, as residents come together to celebrate and support local 
      initiatives.\n- **Cultural Legacy: The celebration could also highlight Philadelphia\'s cultural 
      legacy, reinforcing its reputation as a city of brotherly love and community spirit.\n\n### Format
       for Response\n\nTo format your response clearly, you can organize it into these sections:\n\n1. 
       **Historical Context\n2. **Expert Opinions\n3. **Related Events\n4. **Statistical Data\n5. 
       **Future Implications\n\nEach section should provide relevant information and insights into 
       how Philadelphia\'s culture and community respond to significant events like a Super Bowl 
       victory."""
    story_drafter = StoryDrafterAgent(openai_api_key, story_drafter_prompt)
    story = story_drafter.draft_stories(researched_stories)
    print(story)

# Script Generator
if test_component == 'script_generator':
    host_prompt = PromptTemplate(
                    input_variables=["combined_input", "chat_history"],
                    template="""
                    You are a charismatic podcast host discussing an interesting story with an expert panelist.
                    
                    {combined_input}
                    
                    Previous Discussion: {chat_history}
                    
                    Your role is to:
                    1. If this is the start, introduce the story engagingly and ask the expert a thought-provoking question
                    2. If responding to the expert, acknowledge their points and ask follow-up questions
                    3. Keep the conversation natural and flowing
                    4. Draw out interesting insights from the expert
                    5. Use conversational language while staying professional
                    
                    Respond in a way that moves the discussion forward naturally.
                    """
                )
    expert_prompt = PromptTemplate(
                    input_variables=["combined_input", "chat_history"],
                    template="""
                    You are a knowledgeable expert panelist on a podcast discussing a story.
                    
                    {combined_input}
                    
                    Previous Discussion: {chat_history}
                    
                    Your role is to:
                    1. Provide deep, insightful analysis of the story
                    2. Draw from relevant expertise and experience
                    3. Respond directly to the host's questions
                    4. Add new perspectives and angles to the discussion
                    5. Use clear, authoritative language while staying accessible
                    
                    Respond to the host's latest point or question while advancing the discussion.
                    """
                )

    drafted_stories = [{"topic" : "SuperBowl", "story": '## Conducting Deep Research on the News Story: "City of Brotherly Love Soars: Philadelphia Honors Eagles After Super Bowl LIX Win"\n\nTo conduct a deep research on this news story, we can break down the task into several key sections:\n\n### 1. Historical Context\n*Philadelphia\'s Nickname: Philadelphia is known as the "City of Brotherly Love," a name derived from the Greek words *phileo (love) and adelphos (brother), chosen by William Penn[1][3]. This nickname reflects the city\'s historical emphasis on brotherly love and civic unity.\n\n### 2. Expert Opinions\n- *Cultural Significance: Experts often highlight Philadelphia\'s rich cultural diversity and historical significance, which contribute to its vibrant community[5].\n- **Sports Culture: The city\'s passionate sports fans, particularly those supporting the Philadelphia Eagles, are known for their dedication and enthusiasm[3].\n\n### 3. Related Events\n- **Super Bowl LIX Victory: If the Eagles won Super Bowl LIX, this would be a significant event for Philadelphia, likely prompting widespread celebrations and community gatherings.\n- **Community Response: The victory would likely be celebrated with parades, rallies, and other community events, showcasing the city\'s spirit of brotherly love and civic pride.\n\n### 4. Statistical Data\n- **Economic Impact: Large-scale events like Super Bowl victories can have a substantial economic impact on the city, boosting local businesses and tourism.\n- **Social Impact: Such events often bring the community together, reinforcing social bonds and civic engagement.\n\n### 5. Future Implications\n- **Community Engagement: The aftermath of a major sports victory can lead to increased community engagement and civic participation, as residents come together to celebrate and support local initiatives.\n- **Cultural Legacy: The celebration could also highlight Philadelphia\'s cultural legacy, reinforcing its reputation as a city of brotherly love and community spirit.\n\n### Format for Response\n\nTo format your response clearly, you can organize it into these sections:\n\n1. **Historical Context\n2. **Expert Opinions\n3. **Related Events\n4. **Statistical Data\n5. **Future Implications\n\nEach section should provide relevant information and insights into how Philadelphia\'s culture and community respond to significant events like a Super Bowl victory.'},
                       {"topic" : "Elon Musk", "story": "<HOST>Welcome to the podcast, everyone! Today, we have an intriguing tale to share. Elon Musk, the renowned entrepreneur, made a $97.4 billion bid for OpenAI, only to be met with a surprising \"No Thanks.\" What led to this unexpected turn of events, and what does it mean for the future of AI innovation? Expert panelist, your thoughts?</HOST>\n\n<EXPERT>The rejection of Musk\'s bid for OpenAI raises questions about OpenAI\'s strategic priorities and their perception of Musk\'s role in the AI industry. It\'s also a reminder of the complexities in tech acquisitions, considering factors like market trends and competition.</EXPERT> <HOST>Host: Interesting insights, expert panelist. With the rejection of Musk\'s bid, how do you see the future of AI collaboration among tech giants and independent research organizations like OpenAI?</HOST><EXPERT>The rejection could potentially lead to a more competitive landscape in AI, with tech giants and independent research organizations seeking collaboration on their own terms. This may drive innovation and foster a more collaborative approach to AI development.</EXPERT><HOST>Host: That\'s an intriguing perspective, expert panelist. How do you envision the impact of this competitive landscape on the advancement of AI and its applications in various sectors?</HOST><EXPERT>The competitive landscape in AI may spur innovation and encourage collaboration, leading to more diverse and inclusive applications in art and beyond.</EXPERT><HOST>Ladies and gentlemen, thank you so much for joining us today on this enlightening podcast. We\'ve had the absolute pleasure of hosting our esteemed guest, [Expert\'s Name], who has shared with us invaluable insights and knowledge in the field of [topic].\n\nWe would like to extend our heartfelt thanks to our guest for their time, expertise, and for gracing us with such a captivating and informative conversation. Your wisdom and passion for [topic] have truly enriched our understanding and we are grateful for the opportunity to learn from you.\n\nTo our loyal audience, thank you for tuning in and for your continued support. Your engagement and feedback are what make these podcasts a success. We hope that you found today\'s discussion as enlightening and informative as we did.\n\nRemember, knowledge is a journey, and we are all lifelong learners. We encourage you to continue exploring this topic and to seek out further resources to deepen your understanding.\n\nUntil next time, keep exploring, keep learning, and keep shining. Goodnight, and thank you once again to our guest and our audience. Stay tuned for our next podcast episode, where we will delve into another exciting topic. Until then, stay curious and keep learning!</HOST>"}]
    script_generator = PodcastScriptGenerator(mistral_api_key)
    script = script_generator.generate_script(drafted_stories)
    print(script)
