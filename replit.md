# Momentum - AI-Powered Productivity & Wellness App

## Overview

Momentum is a productivity and wellness application that combines task management with AI-driven personalized coaching. The system uses Google's Gemini AI to generate daily plans based on user context, previous performance, and mood tracking. The application helps users achieve their goals through personalized objective setting, mood check-ins, and adaptive task recommendations.

The system consists of a Django REST API backend and a React Native (Expo) mobile frontend, designed to provide an intelligent, context-aware productivity companion.

## Recent Changes

**October 5, 2025 - Complete Implementation**
- Implemented all Django backend models, views, serializers, and API endpoints
- Created llm_service.py with context-rich prompt templates for Gemini AI integration
- Built React Native frontend with Onboarding and Dashboard screens
- Configured Zustand state management and Axios API client
- Set up Token-based authentication and CORS
- Configured Django backend workflow running on port 5000
- Implemented hybrid performance model (LLM for complex generation, DB for simple retrieval)
- All four core philosophies implemented: Progressive Onboarding, Empathetic AI, Integrated Context, Hybrid Performance

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- React Native with Expo framework for cross-platform mobile development
- React Navigation (Stack Navigator) for screen navigation
- NativeWind + Tailwind CSS for styling
- Zustand for lightweight state management
- Axios for HTTP requests

**Key Design Decisions:**

1. **State Management (Zustand):** Chosen over Redux for simplicity and minimal boilerplate. The global store manages authentication tokens, user data, profile information, and objectives list. The token is stored both in Zustand state and as a global variable for axios interceptor access.

2. **Navigation Pattern:** Stack-based navigation with two main screens (Onboarding and Dashboard). Header is hidden for a clean, immersive UI experience. The app starts with onboarding and navigates to dashboard after successful authentication.

3. **API Client Architecture:** Centralized axios instance with automatic token injection via interceptors. API functions are organized by domain (auth, profile, objectives, check-ins, tips, hobbies) for maintainable code structure.

4. **Styling Approach:** NativeWind provides Tailwind-like utility classes for React Native, enabling consistent styling patterns familiar to web developers while maintaining native performance.

### Backend Architecture

**Technology Stack:**
- Django 5.2 with Django REST Framework
- Token-based authentication (DRF authtoken)
- Google Gemini AI for intelligent plan generation
- CORS headers for cross-origin support
- Python-decouple for environment configuration

**Key Design Decisions:**

1. **Authentication Strategy:** Token-based authentication chosen over JWT for simplicity. Tokens are created/retrieved on login and onboarding, providing stateless authentication suitable for mobile apps. AllowAny permission on auth endpoints, IsAuthenticated on protected resources.

2. **AI Integration Pattern:** The LLM service is isolated in a separate module (`llm_service.py`) using Google's Gemini AI. The system generates context-aware daily plans by analyzing user goals, active projects, past performance, hobbies, and recent mood check-ins. This separation allows for easy model switching or enhancement without affecting core business logic.

3. **Data Model Design:**
   - **UserProfile:** Extends Django User with productivity preferences (goal, scheduling method like Atomic Habits/Pomodoro) and optional health metrics
   - **Project:** Represents larger work initiatives with active/inactive states
   - **Objective:** Daily tasks linked to users and optionally to projects, tracked by completion status
   - **DailyCheckIn:** Mood and notes tracking for context-aware plan generation
   - **Tip:** Curated content (quotes, productivity tips) categorized by type
   - **Hobby:** User interests tracked for balanced activity suggestions

4. **Plan Generation Logic:** The AI prompt engineering incorporates:
   - User context (name, goals, preferred methodology)
   - Historical performance (completed/incomplete tasks)
   - Emotional state (previous day's mood)
   - Active projects and hobbies
   - Adaptive task sizing (breaks tasks down when user reports stress/fatigue)

5. **API Design:** RESTful endpoints organized by resource type with both function-based views (for simple CRUD) and class-based generic views (for standard list/detail patterns). Serializers handle data validation and transformation.

### Data Storage

**Database:** Django ORM with support for multiple backends (SQLite for development, PostgreSQL/MySQL for production). Models use Django's built-in migration system for schema management.

**Key Schema Patterns:**
- One-to-One: User to UserProfile
- One-to-Many: User to Projects, Objectives, DailyCheckIns, Hobbies
- Optional Foreign Key: Objectives to Projects (tasks can exist independently)
- Timestamp tracking: created_at/updated_at fields for audit trails

### Authentication & Authorization

**Mechanism:** Django REST Framework Token Authentication
- Tokens generated on user creation (onboarding) and login
- Stored client-side and sent via Authorization header
- Global axios interceptor automatically attaches tokens to requests
- No token expiration implemented (suitable for MVP, should add refresh logic for production)

### External Dependencies

**Third-Party Services:**
- **Google Gemini AI API:** Core intelligence layer for generating personalized daily plans, hobby suggestions, and workout recommendations. Requires GEMINI_API_KEY environment variable.

**Key Python Packages:**
- `djangorestframework`: REST API framework
- `django-cors-headers`: Cross-origin resource sharing for mobile app
- `python-decouple`: Environment variable management
- `google-genai`: Google Generative AI client library

**Key JavaScript Packages:**
- `expo`: React Native development platform
- `@react-navigation/*`: Navigation library
- `axios`: HTTP client
- `zustand`: State management
- `nativewind`: Tailwind CSS for React Native
- `react-native-safe-area-context` & `react-native-screens`: Navigation dependencies

**Environment Configuration:**
- `SECRET_KEY`: Django security key
- `GEMINI_API_KEY`: Google AI API authentication
- API base URL configured in frontend client (currently localhost:5000)