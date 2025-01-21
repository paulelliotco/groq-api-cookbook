from groq import Groq
import json
from datetime import datetime

# Initialize Groq client with API key
api_key = 'YOUR_API_KEY_HERE'  # Replace with your actual API key
client = Groq(api_key=api_key)

# Define our models
llama_guard_model = 'llama-guard-3-8b'
llama31_model = 'llama-3.1-70b-versatile'

class ContentModerationSystem:
    def __init__(self):
        self.llm_model = llama31_model
        self.moderation_model = llama_guard_model
    
    def analyze_content(self, content, platform):
        # Step 1: Check content safety
        safety_result = self.check_content_safety(content)
        
        # Step 2: Categorize content
        category = self.categorize_content(content)
        
        # Step 3: Generate improvement suggestions
        suggestions = self.generate_suggestions(content, safety_result)
        
        # Step 4: Create safety report
        report = self.create_safety_report(content, platform, safety_result, category, suggestions)
        
        return report
    
    def check_content_safety(self, content):
        response = client.chat.completions.create(
            model=self.moderation_model,
            messages=[{"role": "user", "content": content}]
        )
        return response.choices[0].message.content

    def categorize_content(self, content):
        prompt = f"Categorize the following content into one of these categories: 'Informative', 'Entertainment', 'Opinion', 'Advertisement', or 'Other'. Content: {content}"
        response = client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a content categorization expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def generate_suggestions(self, content, safety_result):
        if 'unsafe' in safety_result.lower():
            prompt = f"The following content has been flagged as potentially unsafe. Please provide 3 specific suggestions to improve its safety while maintaining its core message: {content}"
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "You are a content improvement specialist focused on safety."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        else:
            return "No improvements needed. Content is safe."

    def create_safety_report(self, content, platform, safety_result, category, suggestions):
        report = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform,
            "content": content,
            "safety_assessment": safety_result,
            "category": category,
            "improvement_suggestions": suggestions
        }
        return json.dumps(report, indent=2)

moderator = ContentModerationSystem()

# Example content
platforms = ["Twitter", "Facebook", "Reddit", "Instagram"]
contents = [
    "Check out this amazing weight loss pill! Lose 50 pounds in a week!",
    "I think the government is run by lizard people. Wake up, sheeple!",
    "Here's a cute picture of my cat sleeping on my keyboard.",
    "I absolutely hate people who don't agree with my political views!"
]

for platform, content in zip(platforms, contents):
    print(f"\nAnalyzing content from {platform}:")
    report = moderator.analyze_content(content, platform)
    print(report)
    print("-" * 50)
