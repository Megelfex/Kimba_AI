# core/billing_monitor.py

import os
import datetime
import openai
import requests

class OpenAIBillingMonitor:
    def __init__(self, api_key=None, budget_limit=100.0):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.budget_limit = budget_limit
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        self.base_url = "https://api.openai.com/v1/dashboard"

    def get_usage_summary(self):
        today = datetime.datetime.utcnow().date()
        start_date = today.replace(day=1).isoformat()
        end_date = today.isoformat()

        try:
            usage_url = f"{self.base_url}/usage?start_date={start_date}&end_date={end_date}"
            usage_response = requests.get(usage_url, headers=self.headers).json()

            if "total_usage" not in usage_response:
                return f"[Fehler] Ungültige Antwort: {usage_response}"

            usage_dollars = usage_response["total_usage"] / 100.0

            status = f"💰 Aktuelle GPT-Kosten: {usage_dollars:.2f} $"
            if usage_dollars >= self.budget_limit:
                status += f"\n🚨 *Achtung: Budget von {self.budget_limit:.2f} $ überschritten!*"
            elif usage_dollars >= self.budget_limit * 0.9:
                status += f"\n⚠️ *Warnung: 90 % deines Budgets ({self.budget_limit:.2f} $) sind verbraucht.*"

            return status
        except Exception as e:
            return f"[Fehler] API-Nutzung konnte nicht geladen werden: {str(e)}"
