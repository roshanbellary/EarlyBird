from interest_classifier import InterestClassifierAgent
from scraper import NewsScraperAgent
from researcher import DeepResearchAgent
from story_drafter import StoryDrafterAgent
from script_generator import PodcastScriptGenerator
from langchain.prompts import PromptTemplate
import re

import os
import re
from dotenv import load_dotenv
load_dotenv()

perplexity_api_key=os.getenv("PERPLEXITY_API_KEY")
openai_api_key=os.getenv("OPENAI_API_KEY")

test_component = 'story_drafter'

# Interest Classifier
if test_component == 'interest_classifier':
    interest_classifier_prompt = PromptTemplate(
                input_variables=["user_interests"],
                template="""
                Here is a list of user interests: {user_interests}
                Generate a list of 3 broad categories based on the user's interests. These categories should be distinct and relatively unrelated from each other and heavily relate to the user's categories given:
                
                The topics should be outputted as <TOPIC> topic 1 </TOPIC> <TOPIC> topic 2 </TOPIC> <TOPIC> topic 3 </TOPIC>
                INCLUDE THE <TOPIC> TAGS
                """
            )

    user_interests_test_cases = [
    ["Urban Planning", "Beekeeping", "Astrobiology", "Minimalist Living", "Cryptography", "Sumo Wrestling", "Mushroom Foraging", "Antique Restoration"],
    ["Taxidermy", "Historical Conspiracy Theories", "Competitive Eating", "Numismatics (Coin Collecting)", "Renaissance Music", "Desert Survival Skills", "Parapsychology", "Knot Tying"],
    ["Guerilla Gardening", "Traditional Archery", "Sanskrit Studies", "Synesthesia Research", "Urban Legends", "Maritime Navigation", "Sculpting with Ice", "Quantum Computing"],
    ["Whale Watching", "Experimental Theater", "Trainspotting", "Ethical Hacking", "Genealogy", "Steampunk Fashion", "Morse Code Communication", "Silent Film Appreciation"],
    ["Ancient Siege Warfare", "Subterranean Exploration (Caving)", "Kintsugi (Japanese Art of Repairing Pottery)", "Meteorology", "Tuvan Throat Singing", "Alchemical Studies", "Propaganda Analysis", "Competitive Yo-Yoing"]
]

    interest_classifier = InterestClassifierAgent(openai_api_key, interest_classifier_prompt)
    for i in user_interests_test_cases:
        interests = interest_classifier.interest_classify(i)
        print(str(i) + ': ' + interests)

# Scraper
if test_component == 'scraper':
    categories = [
        "<TOPIC> Urban Planning </TOPIC><TOPIC> Beekeeping </TOPIC><TOPIC> Cryptography </TOPIC>",
        "<TOPIC> Taxidermy </TOPIC><TOPIC> Numismatics </TOPIC><TOPIC> Competitive Eating </TOPIC>",
    ]
    seperated_categories = [re.findall(r'<TOPIC>\s*(.*?)\s*</TOPIC>', s) for s in categories]
    print(seperated_categories)
    for i in seperated_categories:
        for j in i:
            scraper = NewsScraperAgent(perplexity_api_key)
            headlines = scraper.get_top_headlines(j)
            print(j + ': ' + headlines['content'])

# Researcher
if test_component == 'researcher':
    headlines = ["City of Brotherly Love Soars: Philadelphia Honors Eagles After Super Bowl LIX Win", 
    "Justice Served: Arrest made in brutal stabbing of beloved Cherry Hill veterinarian", 
    "Breaking News: Russian Drone Breaches Chernobyl Nuclear Plant\'s Shield", 
    "Breaking News: 3 Hostages Freed from Gaza Captivity - A Miraculous Escape!", 
    "Breaking News: UN Urges Immediate Ceasefire in Gaza to Prevent Humanitarian Crisis"
    ]
    for i in headlines:
        researcher = DeepResearchAgent(perplexity_api_key)
        researched_stories = researcher.research_stories(i)
        print(i + ': ' + str(researched_stories[0]["research"]['choices'][0]["message"]["content"]))

# Story Drafter
if test_component == 'story_drafter':
    story_drafter_prompt = PromptTemplate(
            input_variables=["story_data"],
            template="""
            Draft a compelling podcast story based on this research:
            {story_data}
            Include a hook to grab attention, a clear narrative structure, key points and analysis, engaging transitions, and thought-provoking conclusions.
            Ensure all the facts and evidence related to the story from the research are incorporated in a coherent and engaging manner and remain in the story.
            ONLY OUTPUT THE STORY PRODUCED BASED ON THE RESEARCH. DO NOT RETURN ANY OTHER TEXT.
            """
        )

    researched_stories = ["""
        City of Brotherly Love Soars: Philadelphia Honors Eagles After Super Bowl LIX Win: ## Overview of the Event

    The Philadelphia Eagles won Super Bowl LIX by defeating the Kansas City Chiefs 40-22, marking their second Super Bowl victory. This win was celebrated with a grand parade in Philadelphia, where fans and players alike rejoiced in the team's triumph.

    ## Expert Opinions

    - **Coach Nick Sirianni**: Highlighted the team's collective effort, stating, "This is the ultimate team game. You can't be great without the greatness of others. Great performance by everybody — offense, defense, special teams" [5].
    - **Jalen Hurts**: Emphasized the role of defense in their victory, saying, "Defense wins championships. We saw how they played today. We saw the difference they made in the game" [5].

    ## Related Events

    - **Parade Celebration**: The city of Philadelphia held a victory parade on Valentine's Day, where thousands of fans gathered to celebrate the Eagles' win. The parade route stretched from South Philadelphia to the Philadelphia Museum of Art, with fans camping out overnight to secure prime spots [2][4].
    - **Player Interactions**: Players like Saquon Barkley and Cooper DeJean interacted with fans, exchanging high-fives and taking photos. A.J. Brown addressed criticism he faced during the season, proclaiming, "You gonna get all those things wrong about me, but one thing you get right: I'm a f---ing champion!" [2].

    ## Statistical Data

    - **Game Statistics**: The Eagles dominated the game, shutting out the Chiefs in the first half. Jalen Hurts threw for 221 yards and two touchdowns, while also rushing for a score. The Eagles' defense sacked Patrick Mahomes six times, including 2.5 by Josh Sweat [5].
    - **Turnovers**: The Eagles' defense forced three turnovers, including a pick-six by Cooper DeJean on his 22nd birthday [5].     

    ## Future Implications

    - **Team Dynamics**: The victory solidifies the Eagles as a formidable team in the NFL, with a strong defense and offense. This win could set the stage for future success, especially with key players like Jalen Hurts and Saquon Barkley [1][5].
    - **Fan Engagement**: The celebration and parade highlight the strong bond between the team and its fans, which could contribute to sustained fan support and enthusiasm in upcoming seasons [2][4].
    """,
    """
    Justice Served: Arrest made in brutal stabbing of beloved Cherry Hill veterinarian: ## Overview of the Case

    - **Arrest and Charges**: Cristian Custodio-Aquino, a 27-year-old man from Portland, Oregon, was arrested and charged with first-degree murder in connection with the stabbing death of Dr. Michael Anthony, a veterinarian in Cherry Hill, New Jersey. The arrest was made by U.S. Marshals in Fresno, California, on February 11, 2025[1][2].

    - **Victim Profile**: Dr. Michael Anthony, 45, was a well-respected veterinarian who owned Haddon Vet in Haddon Heights and worked at various general and emergency practices in Camden, Gloucester, and Ocean counties. He was found unconscious with multiple stab wounds in front of his home on Sharrowvalle Road in Cherry Hill on December 10, 2024[2].

    ## Investigation Details

    - **Investigation Process**: The Camden County Prosecutor’s Office Homicide Unit and Cherry Hill Police Department conducted a comprehensive investigation. They identified Custodio-Aquino as the suspect after analyzing evidence, including a pair of prescription glasses found near the crime scene that were sold to him in Washington State[1][2].

    - **Security Footage**: A black sedan was captured on security footage leaving the neighborhood around the time of the murder. The vehicle was later tracked to Pennsylvania, Florida, Alabama, and Texas. It had been in New Jersey since October and was in the Haddon Township area until December 8[2].

    ## Expert Opinions and Community Reaction

    - **Community Response**: Cherry Hill Mayor Dave Fleisher expressed relief that a suspect was apprehended, noting the community's ongoing mourning for Dr. Anthony[2].

    - **Lack of Motive Disclosure**: Prosecutors have not disclosed a motive for the murder. The complaint and affidavit indicate that Anthony and Custodio-Aquino were acquaintances, but further details were not provided[2].

    ## Statistical Data and Future Implications

    - **Crime Statistics**: This case highlights the rarity of such violent crimes in Cherry Hill, a generally safe community. The arrest and charges may provide some reassurance to residents.

    - **Future Implications**: The case's resolution could impact community trust in law enforcement and may influence future investigations into similar crimes. The extradition process for Custodio-Aquino is ongoing, with potential legal proceedings to follow in New Jersey[1][2].

    ## Evidence and Facts

    - **Physical Evidence**: The prescription glasses found at the crime scene were a crucial piece of evidence linking Custodio-Aquino to the crime[2].

    - **Extradition Status**: Custodio-Aquino is currently being held at the Fresno County Jail awaiting extradition to New Jersey[1][2].
    """
    ]

    for i in researched_stories:
        story_drafter = StoryDrafterAgent(openai_api_key, story_drafter_prompt)
        story = story_drafter.draft_stories(i)
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
