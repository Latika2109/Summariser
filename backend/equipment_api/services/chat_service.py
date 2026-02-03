import os
import requests
import json
from .analytics_service import AnalyticsService
from dotenv import load_dotenv

load_dotenv()

class ChatService:
    """Service to handle AI Chat interactions via OpenRouter"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.analytics = AnalyticsService()

    def get_response(self, user_message, dataset):
        """
        Generate a response based on dataset context and user message.
        """
        # 1. Gather Context
        context = self._build_context(dataset)
        
        # 2. Build System Prompt with Navigation Instructions
        system_prompt = f"""
You are an intelligent assistant for a Chemical Equipment Visualizer app.
You have access to the current dataset statistics.

DATASET CONTEXT:
{context}

NAVIGATION COMMANDS:
If the user asks to see a specific view, append one of these tags to the end of your response (invisible to user):
- To go to Dashboard: <<NAV:DASHBOARD>>
- To go to Alerts/Thresholds: <<NAV:ALERTS>>
- To go to History: <<NAV:HISTORY>>
- To go to Health/Efficiency/Root Cause: <<NAV:HEALTH>>

Example:
User: "Show me the alerts."
AI: "Certainly! Taking you to the alerts view. <<NAV:ALERTS>>"

Keep responses concise and helpful. formatting: Markdown.
"""

        # 3. Call OpenRouter
        try:
            payload = {
                "model": "openai/gpt-oss-120b:free", 
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "ChemicalVisualizer"
            }
            
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            completion = response.json()
            return completion['choices'][0]['message']['content']
            
        except Exception as e:
            print(f"OpenRouter Error: {e}")
            return "I'm sorry, I couldn't connect to the AI brain right now. " + self._mock_response(user_message)

    def _build_context(self, dataset):
        """Summarize dataset for the LLM"""
        # Use stored stats from the dataset model
        total = dataset.total_equipment
        avg_p = dataset.avg_pressure
        avg_t = dataset.avg_temperature
        
        # Check for active alerts using database query if possible, or simple fallback
        # records = dataset.records.all() # Optimization: don't load all if not needed
        # But we need alerts count.
        
        try:
            alerts_count = dataset.records.filter(has_alert=True).count()
        except:
             # Fallback if has_alert doesn't exist
            alerts_count = 0
            for r in dataset.records.all():
                 if r.pressure > 20 or r.temperature > 80:
                     alerts_count += 1
                
        return f"""
        - Dataset: {dataset.filename}
        - Total Equipment: {total}
        - Avg Pressure: {avg_p}
        - Avg Temperature: {avg_t}
        - Active Alerts: {alerts_count} equipment items flagged.
        """

    def _mock_response(self, message):
        """Fallback rule-based logic"""
        msg = message.lower()
        if 'alert' in msg:
            return "I can help you visualize alerts. Switching view now. <<NAV:ALERTS>>"
        if 'health' in msg or 'root' in msg:
            return "Let's look at the health analysis. <<NAV:HEALTH>>"
        if 'history' in msg:
            return "Here is your upload history. <<NAV:HISTORY>>"
        if 'dashboard' in msg or 'home' in msg:
             return "Back to the dashboard. <<NAV:DASHBOARD>>"
             
        return "I am a simulated AI assistant. To enable full intelligence, please configure the OpenRouter API Key in the backend."
