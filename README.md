# Podcast Generation System

## Overview
This project automates the creation of podcasts by collecting data, processing it, and generating content with AI agents. It pulls current event data, formats it, creates a dialogue between an Expert and an MC, and produces a final audio podcast using 11 Labs.

## Features
- **Customer Setup:** Users select their areas of interest.
- **Data Collection:** A Scraper Agent pulls current event data from Perplexity.
- **Data Processing:** A Transcriber Agent converts raw data into an essay format. Questions are generated for the MC Agent.
- **Content Generation:** An Expert Agent and an MC Agent interact to form the podcast content. Voice follow-ups may be added.
- **Final Production:** The final script is sent to 11 Labs to generate audio content.
- **Extensibility:** Potential integration of video generation using Luma Dream Machine.

## Folder Structure
podcast_generation_system/
├── config/
│   └── settings.yaml         # API keys and configuration.
├── data/
│   ├── raw/                  # Raw data from Perplexity.
│   ├── processed/            # Processed data files.
│   └── logs/                 # Debug and log files.
├── agents/
│   ├── scraper/
│   │   ├── scraper_agent.py  # Pulls data from Perplexity.
│   │   └── utils.py          # Helper functions.
│   ├── transcriber/
│   │   └── transcriber_agent.py  # Converts data to essay format.
│   ├── expert/
│   │   └── expert_agent.py   # Provides expert dialogue.
│   └── mc/
│       └── mc_agent.py       # Generates and handles MC dialogue.
├── processors/
│   ├── data_processing.py    # Processes and formats scraped data.
│   └── question_generation.py # Creates questions for the MC Agent.
├── pipeline/
│   └── podcast_workflow.py   # Orchestrates the entire process.
├── audio/
│   ├── final_output/         # Stores the final podcast audio files.
│   └── audio_generation.py   # Converts scripts to audio using 11 Labs.
├── tests/
│   └── test_*.py             # Unit and integration tests.
└── README.md                 # Project overview and instructions.

