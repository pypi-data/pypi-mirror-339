import os
import json
import time
import re
import numpy as np
import random
from typing import Tuple, Dict
from dotenv import load_dotenv
from importlib import resources

load_dotenv()

def load_model_config():
    load_dotenv()
    file_path = os.getenv("FILE_PATH")

    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)

    try:
        # Load from the packaged resource
        with resources.open_text("Techv_ai", "models.json") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading model config from packaged file: {e}")
        return {}

class query_complexity_score:
    def __init__(self, client, model: str = "llama-3.3-70b-versatile"):
        self.client = client
        self.model = model

    def get_scores(self, question: str) -> Tuple[float, float, float]:
        prompt = f"""You are an AI system trained to assess the complexity of a given question. 
                    Evaluate the following question and distribute a probability score across three categories: 
                    Simple, Moderate, and Complex.
                    Question: {question}
                    Scoring Guidelines:
                    - Assign values between 0 and 1 to each category.
                    - Ensure the sum of all values is exactly 1.
                    - Respond strictly in the format: Simple: <number>, Moderate: <number>, Complex: <number>."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=50
            )

            model_response = chat_completion.choices[0].message.content
            scores = re.findall(r"(?:Simple|Moderate|Complex):\s*(\d*\.?\d+)", model_response)
            if len(scores) != 3:
                raise ValueError(f"Invalid Groq response format: {model_response}")

            return tuple(float(score) for score in scores)

        except Exception as e:
            print(f"[ERROR] Error during scoring: {e}")
            return (0.0, 0.0, 1.0)

class router:
    def __init__(self, client):
        self.client = client
        self.models = load_model_config()
        self.chat_histories = {}
        self.complexity_scorer = query_complexity_score(client)

    def softmax(self, x: np.ndarray) -> np.ndarray:
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()

    def generate_answer(self, question: str, model: str, user_id: str = "session_1") -> Dict:
        try:
            start_time = time.time()
            if user_id not in self.chat_histories:
                self.chat_histories[user_id] = []

            chat_history = self.chat_histories[user_id]
            chat_history.append({"role": "user", "content": question})

            chat_completion = self.client.chat.completions.create(
                messages=chat_history,
                model=model,
                temperature=0.6,
                max_tokens=4096
            )

            response_text = chat_completion.choices[0].message.content.strip() if chat_completion.choices else ""

            if not response_text:
                return {"error": "Empty response from model."}

            chat_history.append({"role": "assistant", "content": response_text})
            self.chat_histories[user_id] = chat_history

            end_time = time.time()
            response_time = round(end_time - start_time, 3)
            usage = getattr(chat_completion, "usage", {})
            total_tokens = getattr(usage, 'total_tokens', 0)
            prompt_tokens = getattr(usage, 'prompt_tokens', 0)
            completion_tokens = getattr(usage, 'completion_tokens', 0)
            tps = total_tokens / response_time if response_time > 0 else 0

            return {
                "model": model,
                "response": response_text,
                "tokens_used": total_tokens,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "response_time": response_time,
                "tokens_per_second": round(tps, 2),
                "chat_history": chat_history
            }

        except Exception as e:
            return {"error": f"Error generating response: {str(e)}"}

    def select_best_model(self, scores: tuple, allowed_categories: list, k=3) -> str:
        simple_score, moderate_score, complex_score = scores

        if "simple" in allowed_categories and simple_score > max(moderate_score, complex_score):
            category = "simple"
            speed_weight, cost_weight = 0.5, 0.5
        elif "moderate" in allowed_categories and moderate_score > max(simple_score, complex_score):
            category = "moderate"
            speed_weight, cost_weight = 0.4, 0.6
        else:
            category = "complex"
            speed_weight, cost_weight = 0.25, 0.75

        models = self.models.get(category, {})
        model_names = list(models.keys())

        if not model_names:
            raise ValueError("No models found in config for selected category.")

        speeds = np.array([models[m]["tokens_per_second"] for m in model_names])
        costs = np.array([models[m]["input_cost_per_million"] for m in model_names])
        speed_probs = self.softmax(speeds)
        cost_probs = self.softmax(-costs)

        final_probs = speed_weight * speed_probs + cost_weight * cost_probs
        final_probs /= final_probs.sum()

        selected_model = random.choices(model_names, weights=final_probs, k=1)[0]
        print(f"[INFO] Selected Model: {selected_model}")
        return selected_model

    def route_query(self, question: str) -> Dict:
        scores = self.complexity_scorer.get_scores(question)
        allowed_categories = ["simple" if scores[0] > max(scores[1:]) else 
                              "moderate" if scores[1] > max(scores[0], scores[2]) 
                              else "complex"]
        selected_model = self.select_best_model(scores, allowed_categories)
        response = self.generate_answer(question, selected_model)
        response.update({
            "allowed_categories": allowed_categories,
            "complexity_scores": scores,
            "selected_model": selected_model
        })
        return response
