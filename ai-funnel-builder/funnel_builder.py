"""Command-line assistant for designing and analysing marketing funnels with Claude."""
import json
from datetime import datetime

from anthropic import Anthropic

MODEL = "claude-sonnet-5-5"

class AIFunnelCreator:
    def __init__(self, client=None):
        self.client = client or Anthropic()
        self.conversation_history = []
        self.funnels = {}
        self.funnel_stages = {
            "awareness": ["Landing Page", "Ad Campaign", "Social Media"],
            "interest": ["Email Signup", "Webinar", "Content Download"],
            "consideration": ["Product Demo", "Consultation", "Comparison"],
            "conversion": ["Purchase", "Checkout", "Payment"],
            "retention": ["Follow-up Email", "Support", "Upsell"]
        }
        self.funnel_types = ["ecommerce", "saas", "lead_generation", "webinar", "membership"]
    
    def chat_with_ai(self, user_message: str) -> str:
        """Send message to Claude and get response."""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        system_prompt = """You are an expert AI Funnel Strategist specializing in Shopify e-commerce optimization. 
You help create, analyze, and improve sales funnels. 
Provide actionable insights, identify bottlenecks, and suggest improvements.
When analyzing funnels, focus on conversion rates, drop-off points, and optimization strategies."""
        
        response = self.client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history
        )
        
        assistant_message = response.content[0].text
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def create_funnel(self, funnel_name: str, funnel_type: str, stages_data: dict) -> dict:
        """Create a new funnel with tracking data."""
        funnel = {
            "id": len(self.funnels) + 1,
            "name": funnel_name,
            "type": funnel_type,
            "created_at": datetime.now().isoformat(),
            "stages": stages_data,
            "conversion_rate": self.calculate_conversion_rate(stages_data),
            "metrics": self.calculate_metrics(stages_data)
        }
        self.funnels[funnel_name] = funnel
        return funnel
    
    def calculate_conversion_rate(self, stages_data: dict) -> float:
        """Calculate overall conversion rate."""
        if not stages_data:
            return 0.0
        visitors = stages_data.get("awareness", {}).get("visitors", 1)
        conversions = stages_data.get("conversion", {}).get("visitors", 0)
        return round((conversions / visitors * 100), 2) if visitors > 0 else 0.0
    
    def calculate_metrics(self, stages_data: dict) -> dict:
        """Calculate key metrics for each stage."""
        metrics = {}
        previous_visitors = None
        
        for stage, data in stages_data.items():
            visitors = data.get("visitors", 0)
            drop_off = 0
            
            if previous_visitors:
                drop_off = round((1 - (visitors / previous_visitors)) * 100, 2)
            
            metrics[stage] = {
                "visitors": visitors,
                "drop_off_percentage": drop_off,
                "status": "healthy" if drop_off < 20 else "needs_attention" if drop_off < 40 else "critical"
            }
            previous_visitors = visitors
        
        return metrics
    
    def analyze_funnel(self, funnel_name: str) -> str:
        """Analyze funnel performance and identify issues."""
        if funnel_name not in self.funnels:
            return f"Funnel '{funnel_name}' not found."
        
        funnel = self.funnels[funnel_name]
        analysis_prompt = f"""Analyze this Shopify sales funnel and provide insights:
        
Funnel: {funnel['name']} (Type: {funnel['type']})
Conversion Rate: {funnel['conversion_rate']}%

Stage Metrics:
{json.dumps(funnel['metrics'], indent=2)}

Please identify:
1. Critical bottlenecks
2. Stages with high drop-off
3. Specific optimization recommendations
4. Estimated impact of improvements"""
        
        return self.chat_with_ai(analysis_prompt)
    
    def list_funnels(self) -> str:
        """List all created funnels."""
        if not self.funnels:
            return "No funnels created yet."
        
        result = "Created Funnels:\n"
        for name, funnel in self.funnels.items():
            result += f"\n- {name} ({funnel['type']}) - Conversion Rate: {funnel['conversion_rate']}%"
        return result
    
    def run_interactive_session(self):
        """Run interactive Q&A session."""
        print("🎯 AI Funnel Creator for Shopify")
        print("=" * 50)
        print("Commands: create | analyze | list | ask | exit\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() == "exit":
                print("Goodbye!")
                break
            
            elif user_input.lower() == "create":
                name = input("Funnel name: ").strip()
                print(f"Types: {', '.join(self.funnel_types)}")
                ftype = input("Funnel type: ").strip()
                
                stages_data = {}
                for stage in self.funnel_stages.keys():
                    visitors = input(f"Visitors for {stage} stage: ").strip()
                    stages_data[stage] = {"visitors": int(visitors) if visitors.isdigit() else 0}
                
                funnel = self.create_funnel(name, ftype, stages_data)
                print(f"\n✅ Funnel created! Conversion Rate: {funnel['conversion_rate']}%\n")
            
            elif user_input.lower() == "analyze":
                name = input("Funnel name to analyze: ").strip()
                analysis = self.analyze_funnel(name)
                print(f"\nAnalysis:\n{analysis}\n")
            
            elif user_input.lower() == "list":
                print(f"\n{self.list_funnels()}\n")
            
            elif user_input.lower() == "ask":
                question = input("Your question: ").strip()
                response = self.chat_with_ai(question)
                print(f"\nAI Response:\n{response}\n")
            
            else:
                response = self.chat_with_ai(user_input)
                print(f"\nAI: {response}\n")

def main():
    app = AIFunnelCreator()
    app.run_interactive_session()

if __name__ == "__main__":
    main()