
from datetime import datetime
from fastapi import FastAPI, HTTPException  # type: ignore #type : ignore
from pydantic import BaseModel
from typing import Dict, Any
from app.extractor import extract_responses
from app.mock_profiles import mock_users
import httpx  # for webhook sending

app = FastAPI()

class CallPayload(BaseModel):
    # _id: str
    # receivedAt: datetime
    payload: Dict[str, Any]

def calculate_similarity(user: Dict, candidate: Dict) -> int:
    keys_to_compare = [
        "schedule", "tidiness", "environment", "cooking", "work_mode", "stress",
        "personality", "conversation", "conflict", "celebration", "floor", "spot", "sunlight"
    ]
    return sum(1 for key in keys_to_compare if user.get(key) == candidate.get(key))

@app.post("/process-call")
async def process_call_data(data: CallPayload):
    try:
        interactions = data.payload.get("call_report", {}).get("interactions", [])
        user_email = data.payload.get("user_email", "Unknown")

        conversation = [
            {"question": item.get("bot_response", ""), "answer": item.get("user_query", "")}
            for item in interactions if item.get("user_query", "").strip()
        ]

        if not conversation:
            raise ValueError("No valid user responses found.")

        extracted_user = extract_responses(user_email, conversation)

        scored = [
            {"username": candidate["username"], "score": calculate_similarity(extracted_user, candidate)}
            for candidate in mock_users
        ]

        top_5_usernames = sorted(scored, key=lambda x: x["score"], reverse=True)[:5]
        top_usernames = [user["username"] for user in top_5_usernames]

        # 🔗 Webhook URL
        webhook_url = "https://webhook-qx2q.onrender.com/webhook"

        # 📤 Send to webhook
        async with httpx.AsyncClient() as client:
            response = await client.post(webhook_url, json={"top_matches": top_usernames})
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail=f"Webhook failed: {response.text}")

        # ✅ Return locally also if needed
        return {"sent_to_webhook": True, "top_matches": top_usernames}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
