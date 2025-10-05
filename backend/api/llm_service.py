import json
import os
from datetime import datetime, timedelta
from google import genai
from google.genai import types


def get_gemini_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set")
    return genai.Client(api_key=api_key)


def generate_daily_plan(user, user_profile, yesterday_date):
    active_projects = user.projects.filter(is_active=True)
    hobbies = user.hobbies.all()
    
    yesterday_objectives = user.objectives.filter(date=yesterday_date)
    completed_yesterday = yesterday_objectives.filter(is_completed=True)
    incomplete_yesterday = yesterday_objectives.filter(is_completed=False)
    
    latest_checkin = user.daily_checkins.order_by('-date').first()
    
    yesterday_mood = latest_checkin.mood if latest_checkin else "Unknown"
    yesterday_notes = latest_checkin.notes if latest_checkin else ""
    
    prompt = f"""You are an expert productivity and wellness coach named 'Momentum'. Your tone is encouraging, empathetic, and concise.

## USER CONTEXT
- Name: {user.first_name or user.username}
- Primary Goal: {user_profile.goal}
- Preferred Method: {user_profile.scheduling_method}
- Active Projects: {', '.join([p.name for p in active_projects]) if active_projects.exists() else 'None'}
- Known Hobbies: {', '.join([h.name for h in hobbies]) if hobbies.exists() else 'None'}

## RECENT PERFORMANCE
- Yesterday's completed tasks: {', '.join([obj.description for obj in completed_yesterday]) if completed_yesterday.exists() else 'None'}
- Yesterday's incomplete tasks: {', '.join([obj.description for obj in incomplete_yesterday]) if incomplete_yesterday.exists() else 'None'}

## USER'S REPORTED STATE
- Yesterday's Mood: {yesterday_mood}
- Notes: {yesterday_notes if yesterday_notes else 'None'}

## YOUR TASK
Based on all the context above, generate a list of 3-5 objectives for today.
1. Re-prioritize and include any incomplete tasks from yesterday. If the user was 'Stressful' or 'Tired', break the incomplete task into a smaller, more manageable first step.
2. Align new tasks with the user's primary goal and active projects.
3. Use the principles of the '{user_profile.scheduling_method}' method to frame the tasks.
4. Provide one short, encouraging sentence at the start, acknowledging their reported mood from yesterday.
5. Format the output as a JSON array of strings ONLY. Do not include any other text or markdown. Example: ["Finish the intro to the report.", "Go for a 20-minute walk.", "Read 10 pages of 'Atomic Habits'."]"""

    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        objectives = json.loads(response_text)
        
        if not isinstance(objectives, list):
            raise ValueError("Response is not a list")
        
        return objectives
    
    except Exception as e:
        return [
            "Review yesterday's incomplete tasks and prioritize one to complete today",
            "Take a 15-minute break to stretch or walk",
            f"Work on your goal: {user_profile.goal}"
        ]


def generate_hobby_suggestion(user, user_profile):
    active_projects = user.projects.filter(is_active=True)
    hobbies = user.hobbies.all()
    latest_checkin = user.daily_checkins.order_by('-date').first()
    
    current_mood = latest_checkin.mood if latest_checkin else "Unknown"
    
    prompt = f"""You are an expert wellness coach named 'Momentum'. Your tone is encouraging and empathetic.

## USER CONTEXT
- Name: {user.first_name or user.username}
- Primary Goal: {user_profile.goal}
- Active Projects: {', '.join([p.name for p in active_projects]) if active_projects.exists() else 'None'}
- Current Hobbies: {', '.join([h.name for h in hobbies]) if hobbies.exists() else 'None'}
- Current Mood: {current_mood}

## YOUR TASK
Based on the user's current state and existing hobbies, suggest ONE new hobby that would complement their lifestyle and help them achieve balance.

Consider:
1. Their current stress level (mood: {current_mood})
2. Their active projects and primary goal
3. Hobbies they already enjoy
4. Suggest something that provides balance or complements their existing activities

Provide your suggestion in the following JSON format ONLY:
{{
    "hobby_name": "The name of the hobby",
    "description": "A brief, encouraging description (2-3 sentences) of why this hobby would benefit them",
    "getting_started": "One simple, actionable first step to try this hobby"
}}

Do not include any other text or markdown."""

    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        suggestion = json.loads(response_text)
        
        return suggestion
    
    except Exception as e:
        return {
            "hobby_name": "Mindful Walking",
            "description": "A simple practice that combines physical activity with mental clarity. Perfect for balancing busy schedules with moments of peace.",
            "getting_started": "Tomorrow, take a 10-minute walk without your phone and focus on your breathing and surroundings."
        }


def generate_workout_plan(user, user_profile):
    latest_checkin = user.daily_checkins.order_by('-date').first()
    current_mood = latest_checkin.mood if latest_checkin else "Unknown"
    
    height_cm = user_profile.height_cm or "Not specified"
    weight_kg = user_profile.weight_kg or "Not specified"
    body_fat = user_profile.body_fat_percentage or "Not specified"
    
    prompt = f"""You are an expert fitness coach named 'Momentum'. Your tone is encouraging, safe, and adaptive.

## USER CONTEXT
- Name: {user.first_name or user.username}
- Primary Goal: {user_profile.goal}
- Height: {height_cm} cm
- Weight: {weight_kg} kg
- Body Fat: {body_fat}%
- Current Mood: {current_mood}

## YOUR TASK
Generate a personalized workout plan for today that adapts to their current mood and fitness level.

Consider:
1. If they're feeling 'Tired' or 'Overwhelmed', suggest a lighter, restorative workout
2. If they're feeling 'Energetic' or 'Focused', suggest a more challenging routine
3. Keep the workout realistic and achievable (20-45 minutes)
4. Include warm-up, main exercises, and cool-down

Provide your workout in the following JSON format ONLY:
{{
    "workout_type": "Type of workout (e.g., Strength, Cardio, Yoga, HIIT)",
    "duration_minutes": 30,
    "encouragement": "A brief, motivating message based on their mood",
    "exercises": [
        {{"name": "Exercise name", "duration": "Duration or reps", "notes": "Helpful tips"}},
        {{"name": "Exercise name", "duration": "Duration or reps", "notes": "Helpful tips"}}
    ]
}}

Do not include any other text or markdown."""

    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        response_text = response.text.strip()
        
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        workout = json.loads(response_text)
        
        return workout
    
    except Exception as e:
        return {
            "workout_type": "Light Activity",
            "duration_minutes": 20,
            "encouragement": "Start with something simple today. Movement is progress!",
            "exercises": [
                {"name": "Gentle stretching", "duration": "5 minutes", "notes": "Focus on areas that feel tight"},
                {"name": "Brisk walking", "duration": "10 minutes", "notes": "Go at your own pace"},
                {"name": "Cool down stretches", "duration": "5 minutes", "notes": "Deep breathing while stretching"}
            ]
        }
