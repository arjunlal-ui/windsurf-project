# FitPulse - CARS24 Wellness Platform

A modern gym management system built with Flask for the CARS24 team. Track events, participate in challenges, and climb the leaderboard!

## Features

- **Event Management**: Browse and RSVP to gym sessions, sports events, and challenges
- **Calendar View**: Weekly schedule with intuitive navigation
- **Leaderboard System**: Track performance across various challenges
- **User Profiles**: Personal dashboard showing participation history
- **Admin Panel**: Comprehensive management for events, challenges, and scores
- **Blog System**: Share wellness tips and announcements
- **Google Sheets Integration**: Backup data to spreadsheets
- **Modern UI**: Dark theme with responsive design
- **Email Authentication**: Secure login with @cars24.com domain restriction

## Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite (local), Google Sheets (backup)
- **Authentication**: Flask-Login with email validation
- **Styling**: Custom CSS with CSS variables, Inter font
- **Icons**: Font Awesome

## Quick Start

1. **Clone and setup**:
   ```bash
   cd gym_platform_arjun/CascadeProjects/windsurf-project
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Initialize database**:
   ```bash
   python app.py
   # Database will be created automatically
   ```

4. **Run the application**:
   ```bash
   python app.py
   # Visit http://localhost:5000
   ```

## Google Sheets Setup (Optional)

1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create service account credentials
4. Download JSON file and save as `credentials.json`
5. Share your sheets with the service account email

## Usage

### For Users
1. Sign in with your @cars24.com email
2. Browse the weekly schedule
3. RSVP to events you're interested in
4. Track your performance on the leaderboard
5. View your participation history

### For Admins
1. Sign in as `admin@cars24.com`
2. Access the admin panel
3. Create and manage events
4. Set up challenges and track scores
5. Publish blog posts
6. Monitor user participation

## Project Structure

```
windsurf-project/
    app.py                 # Main Flask application
    requirements.txt       # Python dependencies
    .env.example          # Environment variables template
    templates/            # HTML templates
        base.html         # Base template with navigation
        index.html        # Home page with weekly schedule
        login.html        # Authentication page
        (other templates)
    static/
        css/
            style.css     # Main stylesheet
        js/
            script.js     # JavaScript functionality
    gym_platform.db      # SQLite database (auto-created)
```

## Key Features Explained

### Authentication System
- Only @cars24.com emails can register
- Automatic user creation on first login
- Admin access for `admin@cars24.com`
- Session management with Flask-Login

### Event Management
- Create one-time and recurring events
- Multiple event types (gym, sports, challenges)
- RSVP system with participation tracking
- Calendar view with weekly navigation

### Challenge System
- Various challenge types (reps, steps, distance, time, custom)
- Score tracking and leaderboard
- Historical data preservation
- Progress visualization

### Data Storage
- Primary: SQLite database for fast local access
- Backup: Google Sheets for data persistence
- Automatic sync for critical operations

## Development Notes

- The application uses a dark theme optimized for reduced eye strain
- Responsive design works on desktop, tablet, and mobile
- All interactive elements have hover states and transitions
- Form validation provides immediate feedback
- Loading states improve user experience

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is proprietary to CARS24.

## Support

For technical issues or questions, please contact the development team.
