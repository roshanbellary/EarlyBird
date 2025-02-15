# Interest Classifier
self.prompt = PromptTemplate(
                input_variables=["user_interests"],
                template="""
                Generate a list of 3 topics based on the user's interests below. 
                These topics should be distinct relatively unrelated from eachother:
                {user_interests}
                
                The topics should be outputted as a list of strings.
                """
            )

# Headline Generator
headline_generator_prompt = PromptTemplate(
                input_variables=["news_item"],
                template="""
                Create an engaging headline for the following news item:
                {news_item}
                
                Make it catchy but informative, suitable for a podcast episode.
                """
            )
headline_generator = HeadlineGeneratorAgent(openai_api_key, headline_generator_prompt)
headlines = headline_generator.generate_headlines(news_items)