# Momentum - AI-Powered Productivity & Wellness App

An intelligent productivity and wellness application that combines task management with AI-driven personalized coaching using Google's Gemini AI. Momentum helps you achieve your goals through personalized objective setting, mood tracking, and adaptive task recommendations.

## Features

- **Progressive Onboarding**: Minimal initial setup - just username, email, password, and your primary goal
- **Empathetic AI Coach**: Daily plans that adapt to your mood and energy levels
- **Integrated Context**: AI considers your goals, projects, hobbies, and recent performance
- **Hybrid Performance**: Uses AI for complex personalization, database for quick retrieval
- **Mood Tracking**: End-of-day check-ins inform tomorrow's plan
- **Smart Task Management**: Breaks down tasks when you're stressed or tired
- **Personalized Suggestions**: Hobby recommendations and workout plans based on your state

## Tech Stack

### Backend
- Django 5.2 + Django REST Framework
- Token-based authentication
- Google Gemini AI (gemini-2.5-flash)
- PostgreSQL/SQLite database
- CORS enabled for mobile app

### Frontend
- React Native with Expo
- React Navigation for screen flow
- Zustand for state management
- Axios for API calls
- NativeWind (Tailwind CSS for React Native)

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ZenonWrites/Momentum.git
cd Momentum
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or if using the Replit environment, dependencies are already installed.

#### Set Environment Variables

Create a `.env` file in the `backend` directory or set environment variables:

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
export SECRET_KEY="your-django-secret-key-here"
```

**Important**: You must have a Gemini API key for the AI features to work.

#### Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Create a Superuser (Optional - for Django Admin)

```bash
python manage.py createsuperuser
```

#### Seed Initial Data (Optional)

You can add some initial tips via Django admin or Django shell:

```bash
python manage.py shell
```

```python
from api.models import Tip

Tip.objects.create(
    category='Quote',
    source='James Clear',
    content='You do not rise to the level of your goals. You fall to the level of your systems.'
)

Tip.objects.create(
    category='Productivity',
    source='Atomic Habits',
    content='The most effective way to change your habits is to focus not on what you want to achieve, but on who you wish to become.'
)
```

#### Start the Backend Server

```bash
python manage.py runserver 0.0.0.0:5000
```

The backend API will be available at `http://localhost:5000/api/`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Configure API URL

The API URL is configured in `frontend/src/api/client.js`. For local development, it's set to `http://localhost:5000/api`. 

If running on a device or different environment, update this URL accordingly.

#### Start the Expo Development Server

```bash
npm start
```

This will start the Expo development server. You can:
- Press `a` to open on Android emulator
- Press `i` to open on iOS simulator
- Press `w` to open in web browser
- Scan the QR code with Expo Go app on your physical device

## Running the Project

### Quick Start (Replit)

If you're on Replit, the backend workflow is already configured:

1. **Add your Gemini API Key**: Click the Secrets (🔒) icon and add `GEMINI_API_KEY`
2. **Backend is auto-running**: The workflow starts automatically on port 5000
3. **Start the frontend**:
   ```bash
   cd frontend
   npm start
   ```

### Local Development

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver 0.0.0.0:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## API Endpoints

### Authentication
- `POST /api/onboarding/` - Create new user account
- `POST /api/login/` - User login

### User Profile
- `GET /api/profile/` - Get user profile
- `PATCH /api/profile/update/` - Update profile

### Objectives
- `GET /api/daily-plan/` - Get AI-generated daily plan
- `GET /api/objectives/` - List objectives (optional ?date=YYYY-MM-DD)
- `PATCH /api/objectives/{id}/` - Update objective completion

### Check-ins & Wellness
- `POST /api/daily-checkin/` - Submit end-of-day mood
- `GET /api/tips/random/` - Get random productivity tip
- `GET /api/suggestions/hobby/` - Get AI hobby suggestion
- `GET /api/suggestions/workout/` - Get AI workout plan

### Projects & Hobbies
- `GET /api/projects/` - List user projects
- `POST /api/projects/` - Create project
- `GET /api/hobbies/` - List user hobbies
- `POST /api/hobbies/` - Add hobby

## Project Structure

```
momentum/
├── backend/
│   ├── api/
│   │   ├── models.py           # Database models
│   │   ├── serializers.py      # DRF serializers
│   │   ├── views.py            # API endpoints
│   │   ├── llm_service.py      # Gemini AI integration
│   │   └── urls.py             # API routing
│   ├── momentum_backend/
│   │   ├── settings.py         # Django settings
│   │   └── urls.py             # Main URL config
│   └── manage.py
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js       # Axios API client
│   │   ├── screens/
│   │   │   ├── OnboardingScreen.js
│   │   │   └── DashboardScreen.js
│   │   └── store/
│   │       └── useStore.js     # Zustand state management
│   ├── App.js                  # Main app component
│   └── package.json
│
└── README.md
```

## How It Works

### 1. Onboarding Flow
- User creates account with minimal info (username, email, password, goal)
- Token is generated for authentication
- User is redirected to dashboard

### 2. Daily Plan Generation
- AI analyzes user's primary goal, active projects, and hobbies
- Reviews previous day's completed/incomplete tasks
- Considers user's reported mood from yesterday's check-in
- Generates 3-5 contextual objectives for today
- If user was stressed/tired, tasks are broken into smaller steps

### 3. Task Management
- User views daily objectives as checkboxes
- Tap to mark complete/incomplete
- View random productivity tips

### 4. End-of-Day Check-in
- User reports their mood (Productive, Tired, Stressful, etc.)
- This informs tomorrow's AI-generated plan
- Creates empathetic, adaptive coaching experience

## Database Models

- **UserProfile**: Extended user data with goal, scheduling method, health metrics
- **Project**: Larger work initiatives (active/inactive)
- **Objective**: Daily tasks linked to users/projects
- **DailyCheckIn**: Mood and notes for context-aware plans
- **Tip**: Curated productivity quotes and tips
- **Hobby**: User interests for balanced suggestions

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes (for AI features) |
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Django debug mode | No (default: True) |

## Troubleshooting

### Backend Issues

**"GEMINI_API_KEY not set" error:**
- Make sure you've added the API key to your environment variables
- Restart the backend server after adding the key

**Database errors:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**CORS errors:**
- Check that `django-cors-headers` is installed
- Verify `CORS_ALLOW_ALL_ORIGINS = True` in settings.py

### Frontend Issues

**"Network Error" or "Failed to load":**
- Verify backend is running on port 5000
- Check API_URL in `frontend/src/api/client.js`
- For Expo: Update API_URL to your actual backend URL (not localhost)

**Expo not starting:**
```bash
cd frontend
rm -rf node_modules
npm install
npm start
```

## Future Enhancements

- Push notifications for daily plan reminders
- Calendar integration for project deadlines
- Analytics dashboard for productivity insights
- Social features to share progress
- Voice input for check-ins
- Integration with fitness trackers

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

Built with ❤️ using Django, React Native, and Google Gemini AI
