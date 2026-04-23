from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, TextAreaField, SelectField, DateField, TimeField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional
from datetime import datetime, timedelta, date, time
import os
from dotenv import load_dotenv
import json
import markupsafe
from bson.objectid import ObjectId
from bson.errors import InvalidId

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# MongoDB Configuration
app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/fitpulse')
mongo = PyMongo(app, serverSelectionTimeoutMS=10000)
db = mongo.db

csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Google Sheets functionality removed

# Database Models (MongoDB)
class User(UserMixin):
    def __init__(self, data):
        self._data = data
        self.id = str(data['_id'])
        self.email = data['email']
        self.name = data['name']
        self.password = data.get('password')
        self.is_admin = data.get('is_admin', False)
        self.created_at = data.get('created_at', datetime.utcnow())
        self.profile_data = data.get('profile_data')
    
    def get_id(self):
        return self.id

def get_user_by_id(user_id):
    try:
        user_data = db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
    except:
        pass
    return None

def get_user_by_email(email):
    user_data = db.users.find_one({'email': email.lower()})
    if user_data:
        return User(user_data)
    return None

# Forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class ResetPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    new_password = StringField('New Password', validators=[DataRequired()])
    confirm_password = StringField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    event_type = SelectField('Event Type', choices=[
        ('gym', 'Gym Session'),
        ('challenge', 'Challenge'),
        ('badminton', 'Badminton'),
        ('run', 'Run'),
        ('football', 'Football'),
        ('cricket', 'Cricket'),
        ('yoga', 'Yoga'),
        ('other', 'Other')
    ])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    location = StringField('Location')
    emoji = StringField('Emoji', default=' Workout')
    is_recurring = SelectField('Recurring', choices=[('False', 'No'), ('True', 'Yes')], default='False')
    submit = SubmitField('Create Event')

class ChallengeForm(FlaskForm):
    name = StringField('Challenge Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    challenge_type = SelectField('Challenge Type', choices=[
        ('reps', 'Max Reps'),
        ('steps', 'Step Count'),
        ('distance', 'Distance (km)'),
        ('time', 'Time (seconds)'),
        ('custom', 'Custom Score')
    ])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Create Challenge')

class ScoreForm(FlaskForm):
    challenge_id = SelectField('Challenge', coerce=int)
    user_email = StringField('User Email', validators=[DataRequired(), Email()])
    value = FloatField('Score', validators=[DataRequired()])
    submit = SubmitField('Log Score')

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Publish Post')

@login_manager.user_loader
def load_user(user_id):
    try:
        return get_user_by_id(user_id)
    except InvalidId:
        # Clear session if user_id is not a valid ObjectId (old SQLite session)
        session.clear()
        return None

# Jinja2 custom filters
@app.template_filter('nl2br')
def nl2br_filter(s):
    if not s:
        return s
    return markupsafe.Markup(s.replace('\n', '<br>\n'))

@app.template_filter('maxval')
def maxval_filter(seq):
    lst = list(seq)
    return max(lst) if lst else 0

@app.template_filter('minval')
def minval_filter(seq, cap=None):
    lst = list(seq)
    val = min(lst) if lst else 0
    if cap is not None:
        return min(val, cap)
    return val

# Routes
@app.route('/health')
def health():
    return "OK", 200

@app.route('/')
def index():
    try:
        week_offset = request.args.get('week_offset', 0, type=int)
        today = datetime.now().date()
        base_monday = today - timedelta(days=today.weekday())
        week_start = base_monday + timedelta(weeks=week_offset)
        week_end = week_start + timedelta(days=4)
        
        # Query events from MongoDB
        events = list(db.events.find({
            'date': {'$gte': datetime.combine(week_start, time(0, 0)), '$lte': datetime.combine(week_end, time(23, 59))}
        }).sort([('date', 1), ('time', 1)]))
        
        # Group events by day
        week_events = {}
        for i in range(5):
            day = week_start + timedelta(days=i)
            week_events[day] = []
        
        for event in events:
            event_date = event['date'].date() if isinstance(event['date'], datetime) else event['date']
            if event_date in week_events:
                # Load participations for this event
                event['participations'] = list(db.participations.find({'event_id': str(event['_id'])}))
                # Convert _id to string for template compatibility
                event['id'] = str(event['_id'])
                week_events[event_date].append(event)
        
        today_events = week_events.get(today, [])
        active_challenges = list(db.challenges.find({'end_date': {'$gte': datetime.combine(today, time(0, 0))}}))
        week_total = sum(len(evts) for evts in week_events.values())
        
        return render_template('index.html',
            week_events=week_events,
            week_start=week_start,
            today_events=today_events,
            active_challenges=active_challenges,
            week_total=week_total,
            datetime=datetime,
            timedelta=timedelta
        )
    except Exception as e:
        print(f"Error in index route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        
        # Validate email domains
        allowed_domains = ['@cars24.com', '@cariotauto.com']
        if not any(email.endswith(domain) for domain in allowed_domains):
            flash('Only @cars24.com or @cariotauto.com emails are allowed', 'error')
            return render_template('login.html', form=form)
        
        # Check MongoDB
        user = get_user_by_email(email)
        
        if user:
            # User exists in MongoDB
            if user.password and user.password == password:
                login_user(user, remember=True)
                flash(f'Welcome, {user.name}!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid password', 'error')
                return render_template('login.html', form=form)
        
        # New user - create account
        name = email.split('@')[0].replace('.', ' ').replace('_', ' ').title()
        is_admin = email == 'admin@cars24.com'
        user_data = {
            'email': email,
            'name': name,
            'password': password,
            'is_admin': is_admin,
            'created_at': datetime.utcnow()
        }
        db.users.insert_one(user_data)
        
        user = get_user_by_email(email)
        login_user(user, remember=True)
        flash(f'Account created! Welcome, {user.name}!', 'success')
        return redirect(url_for('index'))
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        
        # Check if user exists in local database
        local_user = db.users.find_one({'email': email})
        
        if local_user:
            # User exists, redirect to reset password
            session['reset_email'] = email
            flash('User found. Please set your new password.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('No account found with this email.', 'error')
    
    return render_template('forgot_password.html', form=form)

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        flash('Please enter your email first.', 'error')
        return redirect(url_for('forgot_password'))
    
    email = session['reset_email']
    form = ResetPasswordForm()
    form.email.data = email  # Pre-fill email
    
    if form.validate_on_submit():
        if form.email.data.lower() != email:
            flash('Email mismatch. Please start over.', 'error')
            return redirect(url_for('forgot_password'))
        
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        
        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('reset_password.html', form=form)
        
        # Update password in MongoDB
        user = get_user_by_email(email)
        if user:
            db.users.update_one(
                {'email': email},
                {'$set': {'password': new_password}}
            )
        
        # Clear session
        session.pop('reset_email', None)
        
        flash('Password updated successfully! Please login with your new password.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html', form=form)

@app.route('/event/<event_id>')
def event_detail(event_id):
    event = db.events.find_one({'_id': ObjectId(event_id)})
    if not event:
        return redirect(url_for('index'))
    
    # Convert _id to string for template compatibility
    event['id'] = str(event['_id'])
    
    participations = list(db.participations.find({'event_id': event_id}))
    # Load user information for each participation
    for p in participations:
        user = db.users.find_one({'_id': ObjectId(p['user_id'])})
        p['user'] = user
    user_participation = None
    if current_user.is_authenticated:
        user_participation = db.participations.find_one({
            'user_id': current_user.id,
            'event_id': event_id
        })
    
    return render_template('event_detail.html', event=event, participations=participations, user_participation=user_participation)

@app.route('/participate/<event_id>', methods=['POST'])
@login_required
def participate(event_id):
    event = db.events.find_one({'_id': ObjectId(event_id)})
    if not event:
        return redirect(url_for('index'))
    
    existing = db.participations.find_one({
        'user_id': current_user.id,
        'event_id': event_id
    })
    
    is_ajax = request.headers.get('Content-Type', '').startswith('application/json')
    
    if existing:
        # Toggle off: remove participation
        db.participations.delete_one({'_id': existing['_id']})
        if is_ajax:
            return jsonify({'success': True, 'message': 'RSVP removed', 'going': False})
        flash('RSVP removed', 'info')
    else:
        participation_data = {
            'user_id': current_user.id,
            'event_id': event_id,
            'registered_at': datetime.utcnow(),
            'attended': False
        }
        db.participations.insert_one(participation_data)
        if is_ajax:
            return jsonify({'success': True, 'message': f'Registered for {event["title"]}!', 'going': True})
        flash(f'Successfully registered for {event["title"]}!', 'success')
    
    return redirect(url_for('event_detail', event_id=event_id))

@app.route('/leaderboard')
def leaderboard():
    today = datetime.now().date()
    challenges = list(db.challenges.find().sort('created_at', -1))
    
    # Compute overall top scores grouped by user
    all_scores = list(db.scores.find())
    user_totals = {}
    for s in all_scores:
        user_id = s['user_id']
        if user_id not in user_totals:
            user_data = db.users.find_one({'_id': ObjectId(user_id)})
            user_totals[user_id] = {'user': user_data, 'total': 0}
        user_totals[user_id]['total'] += s['value']
    top_scores = sorted(user_totals.values(), key=lambda x: x['total'], reverse=True)[:10]
    
    # Event participation rankings — who attends the most
    all_participations = list(db.participations.find())
    user_events = {}
    for p in all_participations:
        user_id = p['user_id']
        if user_id not in user_events:
            user_data = db.users.find_one({'_id': ObjectId(user_id)})
            user_events[user_id] = {'user': user_data, 'count': 0, 'attended': 0}
        user_events[user_id]['count'] += 1
        if p['attended']:
            user_events[user_id]['attended'] += 1
    event_rankings = sorted(user_events.values(), key=lambda x: x['count'], reverse=True)[:10]
    
    # Past events calendar — last 8 weeks of events
    cal_start = datetime.combine(today - timedelta(weeks=8), time(0, 0))
    cal_end = datetime.combine(today, time(23, 59))
    past_events = list(db.events.find({
        'date': {'$gte': cal_start, '$lte': cal_end}
    }).sort('date', -1))
    # Convert _id to string for template compatibility
    for event in past_events:
        event['id'] = str(event['_id'])
    
    # Weekly participation chart data (last 8 weeks)
    weekly_labels = []
    weekly_data = []
    for w in range(7, -1, -1):
        wk_start = today - timedelta(weeks=w, days=today.weekday())
        wk_end = wk_start + timedelta(days=6)
        label = wk_start.strftime('%b %d')
        week_events = list(db.events.find({
            'date': {'$gte': datetime.combine(wk_start, time(0, 0)), '$lte': datetime.combine(wk_end, time(23, 59))}
        }))
        event_ids = [e['_id'] for e in week_events]
        count = db.participations.count_documents({
            'event_id': {'$in': event_ids}
        })
        weekly_labels.append(label)
        weekly_data.append(count)
    
    # Monthly event count (last 6 months)
    monthly_labels = []
    monthly_events = []
    monthly_participants = []
    for m in range(5, -1, -1):
        first = (today.replace(day=1) - timedelta(days=m * 30)).replace(day=1)
        if m > 0:
            last = (first + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        else:
            last = today
        label = first.strftime('%b %Y')
        evt_count = db.events.count_documents({'date': {'$gte': datetime.combine(first, time(0, 0)), '$lte': datetime.combine(last, time(23, 59))}})
        month_events = list(db.events.find({
            'date': {'$gte': datetime.combine(first, time(0, 0)), '$lte': datetime.combine(last, time(23, 59))}
        }))
        # Convert _id to string for template compatibility
        for event in month_events:
            event['id'] = str(event['_id'])
        event_ids = [e['_id'] for e in month_events]
        part_count = db.participations.count_documents({
            'event_id': {'$in': event_ids}
        })
        monthly_labels.append(label)
        monthly_events.append(evt_count)
        monthly_participants.append(part_count)
    
    return render_template('leaderboard.html',
        challenges=challenges,
        top_scores=top_scores,
        event_rankings=event_rankings,
        past_events=past_events,
        weekly_labels=json.dumps(weekly_labels),
        weekly_data=json.dumps(weekly_data),
        monthly_labels=json.dumps(monthly_labels),
        monthly_events=json.dumps(monthly_events),
        monthly_participants=json.dumps(monthly_participants),
    )

@app.route('/challenge/<challenge_id>')
def challenge_detail(challenge_id):
    challenge = db.challenges.find_one({'_id': ObjectId(challenge_id)})
    if not challenge:
        return redirect(url_for('index'))
    scores = list(db.scores.find({'challenge_id': challenge_id}).sort('value', -1))
    # Load user information for each score
    for score in scores:
        user = db.users.find_one({'_id': ObjectId(score['user_id'])})
        score['user'] = user
    return render_template('challenge_detail.html', challenge=challenge, scores=scores)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('index'))
    
    events = list(db.events.find().sort('date', -1).limit(10))
    # Convert _id to string for template compatibility
    for event in events:
        event['id'] = str(event['_id'])
    challenges = list(db.challenges.find().sort('created_at', -1).limit(10))
    users = list(db.users.find().sort('created_at', -1).limit(10))
    
    return render_template('admin.html', events=events, challenges=challenges, users=users)

@app.route('/admin/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('index'))
    
    form = EventForm()
    if form.validate_on_submit():
        event_data = {
            'title': form.title.data,
            'description': form.description.data,
            'event_type': form.event_type.data,
            'date': datetime.combine(form.date.data, form.time.data),
            'time': form.time.data.strftime('%H:%M:%S'),
            'location': form.location.data,
            'emoji': form.emoji.data or ' Workout',
            'is_recurring': form.is_recurring.data == 'True',
            'created_by': current_user.id,
            'created_at': datetime.utcnow()
        }
        result = db.events.insert_one(event_data)
        event_id = str(result.inserted_id)
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('create_event.html', form=form)

@app.route('/admin/delete_event/<event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('index'))
    
    event = db.events.find_one({'_id': ObjectId(event_id)})
    if not event:
        flash('Event not found', 'error')
        return redirect(url_for('admin'))
    
    # Delete all participations for this event
    db.participations.delete_many({'event_id': event_id})
    
    # Delete the event
    db.events.delete_one({'_id': ObjectId(event_id)})
    
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/create_challenge', methods=['GET', 'POST'])
@login_required
def create_challenge():
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('index'))
    
    form = ChallengeForm()
    if form.validate_on_submit():
        challenge_data = {
            'name': form.name.data,
            'description': form.description.data,
            'challenge_type': form.challenge_type.data,
            'unit': get_unit_for_type(form.challenge_type.data),
            'start_date': datetime.combine(form.start_date.data, time(0, 0)),
            'end_date': datetime.combine(form.end_date.data, time(0, 0)),
            'created_by': current_user.id,
            'created_at': datetime.utcnow()
        }
        result = db.challenges.insert_one(challenge_data)
        challenge_id = str(result.inserted_id)
        
        flash('Challenge created successfully!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('create_challenge.html', form=form)

@app.route('/admin/log_score', methods=['GET', 'POST'])
@login_required
def log_score():
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('index'))
    
    form = ScoreForm()
    form.challenge_id.choices = [(str(c['_id']), c['name']) for c in db.challenges.find()]
    
    if form.validate_on_submit():
        user = get_user_by_email(form.user_email.data.lower())
        if not user:
            flash('User not found', 'error')
            return render_template('log_score.html', form=form)
        
        score_data = {
            'user_id': user.id,
            'challenge_id': form.challenge_id.data,
            'value': form.value.data,
            'recorded_by': current_user.id,
            'recorded_at': datetime.utcnow()
        }
        result = db.scores.insert_one(score_data)
        score_id = str(result.inserted_id)
        
        flash('Score logged successfully!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('log_score.html', form=form)

@app.route('/admin/blog', methods=['GET', 'POST'])
@login_required
def admin_blog():
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('index'))
    
    form = BlogForm()
    if form.validate_on_submit():
        post_data = {
            'title': form.title.data,
            'content': form.content.data,
            'author_id': current_user.id,
            'created_at': datetime.utcnow(),
            'is_published': True
        }
        db.blog_posts.insert_one(post_data)
        
        flash('Blog post published!', 'success')
        return redirect(url_for('blog'))
    
    posts = list(db.blog_posts.find().sort('created_at', -1))
    # Load author information for each post
    for post in posts:
        author = db.users.find_one({'_id': ObjectId(post['author_id'])})
        post['author'] = author
    return render_template('admin_blog.html', form=form, posts=posts)

@app.route('/admin/delete_blog/<post_id>', methods=['POST'])
@login_required
def delete_blog(post_id):
    if not current_user.is_admin:
        flash('Admin access required', 'error')
        return redirect(url_for('index'))
    
    db.blog_posts.delete_one({'_id': ObjectId(post_id)})
    flash('Blog post deleted!', 'success')
    return redirect(url_for('admin_blog'))

@app.route('/blog')
def blog():
    posts = list(db.blog_posts.find({'is_published': True}).sort('created_at', -1))
    # Load author information for each post
    for post in posts:
        author = db.users.find_one({'_id': ObjectId(post['author_id'])})
        post['author'] = author
    return render_template('blog.html', posts=posts)

@app.route('/profile')
@login_required
def profile():
    participations = list(db.participations.find({'user_id': current_user.id}).sort('registered_at', -1).limit(10))
    # Load event information for each participation
    for p in participations:
        event = db.events.find_one({'_id': ObjectId(p['event_id'])})
        p['event'] = event
    scores = list(db.scores.find({'user_id': current_user.id}).sort('recorded_at', -1).limit(10))
    
    return render_template('profile.html', participations=participations, scores=scores)

def get_unit_for_type(challenge_type):
    units = {
        'reps': 'reps',
        'steps': 'steps/day',
        'distance': 'km',
        'time': 'seconds',
        'custom': 'points'
    }
    return units.get(challenge_type, 'points')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    app.run(debug=False, host='0.0.0.0', port=port)
