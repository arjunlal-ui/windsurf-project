"""Seed script — populates the database with sample data."""
from pymongo import MongoClient
from datetime import datetime, timedelta, date, time
import random
from bson.objectid import ObjectId

def seed():
    # Initialize MongoDB connection
    client = MongoClient("mongodb+srv://fitpulse:fitpulse@cluster0.hcahccp.mongodb.net/?retryWrites=true&w=majority")
    db = client.fitpulse
    
    # Clear existing collections
    db.users.delete_many({})
    db.events.delete_many({})
    db.participations.delete_many({})
    db.challenges.delete_many({})
    db.scores.delete_many({})
    db.blog_posts.delete_many({})

    # ── Users ───────────────────────────────────────────────
    users_data = [
        ("admin@cars24.com", "Admin", True),
        ("arjun.sharma@cars24.com", "Arjun Sharma", False),
        ("priya.verma@cars24.com", "Priya Verma", False),
        ("rahul.kumar@cars24.com", "Rahul Kumar", False),
        ("sneha.patel@cars24.com", "Sneha Patel", False),
        ("vikram.singh@cars24.com", "Vikram Singh", False),
        ("ananya.gupta@cars24.com", "Ananya Gupta", False),
        ("rohan.joshi@cars24.com", "Rohan Joshi", False),
        ("meera.nair@cars24.com", "Meera Nair", False),
        ("amit.das@cars24.com", "Amit Das", False),
        ("kavita.reddy@cars24.com", "Kavita Reddy", False),
        ("nikhil.mehta@cars24.com", "Nikhil Mehta", False),
    ]
    users = []
    for email, name, is_admin in users_data:
        user_data = {
            'email': email,
            'name': name,
            'is_admin': is_admin,
            'created_at': datetime.utcnow()
        }
        result = db.users.insert_one(user_data)
        user_data['_id'] = result.inserted_id
        user_data['id'] = str(result.inserted_id)
        users.append(user_data)

    admin = users[0]

    # ── Helper: generate weekly recurring events ────────────
    today = date.today()
    monday = today - timedelta(days=today.weekday())

    # We'll create events for the past 4 weeks + current week + next 2 weeks (7 weeks total)
    weeks = range(-4, 3)

    event_templates = [
            {
                "title": "Coach Assisted Gym Session (Morning)",
                "description": "Start your day with expert guidance! Our certified coaches will help you with proper form, technique, and personalized workout plans. Whether you're a beginner or experienced lifter, get the attention you need to reach your fitness goals.\n\nSession includes:\n• Personalized warm-up routine\n• Technique correction\n• Workout programming\n• Cool-down and stretching\n\nAll equipment provided. Just bring your energy!",
                "event_type": "gym",
                "time": time(7, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "🏋️",
                "day_offset": 0,  # Monday
            },
            {
                "title": "Coach Assisted Gym Session (Morning)",
                "description": "Start your day with expert guidance! Our certified coaches will help you with proper form, technique, and personalized workout plans. Whether you're a beginner or experienced lifter, get the attention you need to reach your fitness goals.\n\nSession includes:\n• Personalized warm-up routine\n• Technique correction\n• Workout programming\n• Cool-down and stretching\n\nAll equipment provided. Just bring your energy!",
                "event_type": "gym",
                "time": time(7, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "🏋️",
                "day_offset": 1,  # Tuesday
            },
            {
                "title": "Coach Assisted Gym Session (Morning)",
                "description": "Start your day with expert guidance! Our certified coaches will help you with proper form, technique, and personalized workout plans. Whether you're a beginner or experienced lifter, get the attention you need to reach your fitness goals.\n\nSession includes:\n• Personalized warm-up routine\n• Technique correction\n• Workout programming\n• Cool-down and stretching\n\nAll equipment provided. Just bring your energy!",
                "event_type": "gym",
                "time": time(7, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "🏋️",
                "day_offset": 2,  # Wednesday
            },
            {
                "title": "Coach Assisted Gym Session (Morning)",
                "description": "Start your day with expert guidance! Our certified coaches will help you with proper form, technique, and personalized workout plans. Whether you're a beginner or experienced lifter, get the attention you need to reach your fitness goals.\n\nSession includes:\n• Personalized warm-up routine\n• Technique correction\n• Workout programming\n• Cool-down and stretching\n\nAll equipment provided. Just bring your energy!",
                "event_type": "gym",
                "time": time(7, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "🏋️",
                "day_offset": 3,  # Thursday
            },
            {
                "title": "Coach Assisted Gym Session (Morning)",
                "description": "Start your day with expert guidance! Our certified coaches will help you with proper form, technique, and personalized workout plans. Whether you're a beginner or experienced lifter, get the attention you need to reach your fitness goals.\n\nSession includes:\n• Personalized warm-up routine\n• Technique correction\n• Workout programming\n• Cool-down and stretching\n\nAll equipment provided. Just bring your energy!",
                "event_type": "gym",
                "time": time(7, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "🏋️",
                "day_offset": 4,  # Friday
            },
            {
                "title": "Coach Assisted Gym Session (Evening)",
                "description": "End your workday with a focused workout under expert supervision! Our coaches provide personalized attention to help you maximize your training session. Perfect for stress relief after a long day.\n\nSession includes:\n• Personalized workout plan\n• Form correction and guidance\n• Progress tracking\n• Recovery tips\n\nAll equipment provided. Show up and let's get stronger!",
                "event_type": "gym",
                "time": time(18, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "💪",
                "day_offset": 0,  # Monday
            },
            {
                "title": "Coach Assisted Gym Session (Evening)",
                "description": "End your workday with a focused workout under expert supervision! Our coaches provide personalized attention to help you maximize your training session. Perfect for stress relief after a long day.\n\nSession includes:\n• Personalized workout plan\n• Form correction and guidance\n• Progress tracking\n• Recovery tips\n\nAll equipment provided. Show up and let's get stronger!",
                "event_type": "gym",
                "time": time(18, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "💪",
                "day_offset": 1,  # Tuesday
            },
            {
                "title": "Coach Assisted Gym Session (Evening)",
                "description": "End your workday with a focused workout under expert supervision! Our coaches provide personalized attention to help you maximize your training session. Perfect for stress relief after a long day.\n\nSession includes:\n• Personalized workout plan\n• Form correction and guidance\n• Progress tracking\n• Recovery tips\n\nAll equipment provided. Show up and let's get stronger!",
                "event_type": "gym",
                "time": time(18, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "💪",
                "day_offset": 2,  # Wednesday
            },
            {
                "title": "Coach Assisted Gym Session (Evening)",
                "description": "End your workday with a focused workout under expert supervision! Our coaches provide personalized attention to help you maximize your training session. Perfect for stress relief after a long day.\n\nSession includes:\n• Personalized workout plan\n• Form correction and guidance\n• Progress tracking\n• Recovery tips\n\nAll equipment provided. Show up and let's get stronger!",
                "event_type": "gym",
                "time": time(18, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "💪",
                "day_offset": 3,  # Thursday
            },
            {
                "title": "Coach Assisted Gym Session (Evening)",
                "description": "End your workday with a focused workout under expert supervision! Our coaches provide personalized attention to help you maximize your training session. Perfect for stress relief after a long day.\n\nSession includes:\n• Personalized workout plan\n• Form correction and guidance\n• Progress tracking\n• Recovery tips\n\nAll equipment provided. Show up and let's get stronger!",
                "event_type": "gym",
                "time": time(18, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "💪",
                "day_offset": 4,  # Friday
            },
            {
                "title": "HYROX Training",
                "description": "High-intensity functional fitness training designed to prepare you for HYROX races. Includes running intervals, sled push/pull, burpee broad jumps, rowing, wall balls, and farmer's carry. All fitness levels welcome — coaches will scale movements.\n\nWhat to bring:\n• Training shoes (cross-trainers preferred)\n• Water bottle & towel\n• Positive energy!",
                "event_type": "gym",
                "time": time(6, 30),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "🏋️",
                "day_offset": 0,  # Monday
            },
            {
                "title": "CrossFit WOD",
                "description": "Workout of the Day — our CrossFit session combines Olympic weightlifting, gymnastics, and metabolic conditioning. Each class includes a warm-up, skill work, the WOD, and cool-down.\n\nToday's focus: Upper body strength + cardio endurance.\n\nEquipment provided. Just show up ready to sweat!",
                "event_type": "gym",
                "time": time(7, 0),
                "location": "CrossFit Box, CARS24 Campus Gym, Building A",
                "emoji": "💪",
                "day_offset": 2,  # Wednesday
            },
            {
                "title": "Zumba Dance Fitness",
                "description": "Dance your way to fitness! Our Zumba session combines Latin and international music with easy-to-follow dance moves. It's a full-body cardio workout that doesn't feel like exercise.\n\nPerfect for beginners and experienced dancers alike. No dance experience needed — just follow along and have fun!\n\nBenefits: Burns 400-600 calories, improves coordination, and boosts mood.",
                "event_type": "other",
                "time": time(17, 30),
                "location": "Multipurpose Hall, CARS24 Office, 3rd Floor",
                "emoji": "💃",
                "day_offset": 1,  # Tuesday
            },
            {
                "title": "Bollywood Dance Session",
                "description": "Learn choreography to the latest Bollywood hits! This high-energy dance class is perfect for stress relief and cardio. Each week we learn a new routine.\n\nThis week: Choreography to 'Naatu Naatu' — get ready for some killer footwork!\n\nNo experience needed. Come as you are, leave as a star!",
                "event_type": "other",
                "time": time(18, 0),
                "location": "Multipurpose Hall, CARS24 Office, 3rd Floor",
                "emoji": "🕺",
                "day_offset": 3,  # Thursday
            },
            {
                "title": "Morning Run Club",
                "description": "Join the CARS24 Run Club for our weekly group run! We have three pace groups:\n\n🟢 Easy (6:30-7:00 min/km) — Beginners welcome\n🟡 Moderate (5:30-6:00 min/km) — Regular runners\n🔴 Fast (4:30-5:00 min/km) — Competitive pace\n\nRoute: Sector 44 → Leisure Valley → Sector 29 loop (5km / 8km options)\n\nPost-run stretching and chai provided!",
                "event_type": "run",
                "time": time(6, 0),
                "location": "Main Gate, CARS24 Office, Sector 44",
                "emoji": "🏃",
                "day_offset": 4,  # Friday
            },
            {
                "title": "Cricket Practice Match",
                "description": "Weekly cricket practice match — teams shuffled every week for fairness. 15-over format.\n\nTeam selection happens 30 mins before. Bring your own kit if you have one, otherwise bats and balls are provided.\n\nPost-match refreshments courtesy of the wellness committee!",
                "event_type": "cricket",
                "time": time(16, 0),
                "location": "CARS24 Cricket Ground, Sector 44 Sports Complex",
                "emoji": "🏏",
                "day_offset": 5,  # Saturday
            },
            {
                "title": "HYROX Race Prep",
                "description": "Advanced HYROX race preparation session. Simulates actual race conditions with timed stations:\n\n1. 1km Run\n2. Ski Erg (1000m)\n3. Sled Push (50m)\n4. Sled Pull (50m)\n5. Burpee Broad Jumps (80m)\n6. Rowing (1000m)\n7. Farmer's Carry (200m)\n8. Wall Balls (100 reps)\n\nOnly for those who have attended at least 3 regular HYROX Training sessions.",
                "event_type": "gym",
                "time": time(7, 0),
                "location": "CARS24 Fitness Center, Ground Floor, Sector 44",
                "emoji": "🔥",
                "day_offset": 4,  # Friday
            },
            {
                "title": "Yoga & Mindfulness",
                "description": "Start your week with balance and calm. This gentle yoga session focuses on flexibility, breathing techniques, and mental clarity.\n\nIncludes:\n• Sun salutations\n• Standing poses for strength\n• Floor stretches for flexibility\n• 10-minute guided meditation\n\nMats provided. Wear comfortable clothing.",
                "event_type": "yoga",
                "time": time(7, 30),
                "location": "Terrace Garden, CARS24 Office, Rooftop",
                "emoji": "🧘",
                "day_offset": 0,  # Monday
            },
            {
                "title": "Badminton Tournament",
                "description": "Weekly doubles badminton tournament! Register as a pair or get matched with a partner.\n\nFormat: Round-robin group stage → Knockout semifinals and final.\n\nCurrent champions: Vikram & Priya (3-week streak!)\n\nCome and dethrone them! 🏆",
                "event_type": "badminton",
                "time": time(18, 30),
                "location": "Indoor Badminton Courts, Sports Complex, Sector 44",
                "emoji": "🏸",
                "day_offset": 2,  # Wednesday
            },
        ]

    all_events = []
    for week_num in weeks:
        week_monday = monday + timedelta(weeks=week_num)
        for tmpl in event_templates:
            evt_date = week_monday + timedelta(days=tmpl["day_offset"])
            evt_data = {
                'title': tmpl["title"],
                'description': tmpl["description"],
                'event_type': tmpl["event_type"],
                'date': datetime.combine(evt_date, time(0, 0)),
                'time': tmpl["time"].strftime('%H:%M:%S'),
                'location': tmpl["location"],
                'emoji': tmpl["emoji"],
                'is_recurring': True,
                'created_by': admin['id'],
                'created_at': datetime.utcnow()
            }
            result = db.events.insert_one(evt_data)
            evt_data['_id'] = result.inserted_id
            evt_data['id'] = str(result.inserted_id)
            evt_data['date'] = evt_date  # Keep original date for comparison
            all_events.append(evt_data)

    # ── Participations (past events get random attendees) ───
    for evt in all_events:
        if evt['date'] <= today:
            # Past/today events: random 4-10 people participated
            participants = random.sample(users[1:], k=random.randint(4, min(10, len(users)-1)))
            # Admin also joins sometimes
            if random.random() > 0.3:
                participants.append(admin)
            for u in participants:
                p_data = {
                    'user_id': u['id'],
                    'event_id': evt['id'],
                    'attended': evt['date'] < today,
                    'registered_at': datetime.combine(evt['date'], time(0, 0)) - timedelta(hours=random.randint(1, 48)),
                }
                db.participations.insert_one(p_data)
        elif evt['date'] <= today + timedelta(days=7):
            # Upcoming week: some early RSVPs
            participants = random.sample(users[1:], k=random.randint(2, 6))
            for u in participants:
                p_data = {
                    'user_id': u['id'],
                    'event_id': evt['id'],
                    'attended': False,
                    'registered_at': datetime.utcnow()
                }
                db.participations.insert_one(p_data)

    # ── Challenges ──────────────────────────────────────────
    challenges_data = [
        {
            "name": "30-Day Push-Up Challenge",
            "description": "Can you do 100 push-ups in a single set by day 30? Start wherever you are and build up daily. Log your max reps each week.\n\nWeek 1: Find your baseline\nWeek 2: +20% from baseline\nWeek 3: +40% from baseline\nWeek 4: Go for 100!",
            "challenge_type": "reps",
            "unit": "reps",
            "start_date": datetime.combine(today - timedelta(days=20), time(0, 0)),
            "end_date": datetime.combine(today + timedelta(days=10), time(0, 0)),
        },
        {
            "name": "10K Steps Daily Challenge",
            "description": "Walk 10,000 steps every single day for a month. Track with your phone or smartwatch. Weekly average will be used for ranking.\n\nBonus points for anyone who hits 15K+ on any day!",
            "challenge_type": "steps",
            "unit": "steps/day",
            "start_date": datetime.combine(today - timedelta(days=15), time(0, 0)),
            "end_date": datetime.combine(today + timedelta(days=15), time(0, 0)),
        },
        {
            "name": "HYROX Simulator Time Trial",
            "description": "Complete the full HYROX simulation course and log your total time. Lowest time wins!\n\nCourse: 8×1km runs + 8 functional stations.\n\nElite target: Under 65 minutes\nGood target: Under 80 minutes\nCompletion target: Under 100 minutes",
            "challenge_type": "time",
            "unit": "minutes",
            "start_date": datetime.combine(today - timedelta(days=30), time(0, 0)),
            "end_date": datetime.combine(today - timedelta(days=2), time(0, 0)),
        },
        {
            "name": "Plank Hold Challenge",
            "description": "How long can you hold a plank? Submit your longest hold time in seconds. Proper form required — no sagging or piking!\n\nTargets:\n🥉 Bronze: 60 seconds\n🥈 Silver: 120 seconds\n🥇 Gold: 180+ seconds",
            "challenge_type": "time",
            "unit": "seconds",
            "start_date": datetime.combine(today - timedelta(days=10), time(0, 0)),
            "end_date": datetime.combine(today + timedelta(days=20), time(0, 0)),
        },
    ]

    challenges = []
    for cd in challenges_data:
        c_data = {
            'name': cd["name"],
            'description': cd["description"],
            'challenge_type': cd["challenge_type"],
            'unit': cd["unit"],
            'start_date': cd["start_date"],
            'end_date': cd["end_date"],
            'created_by': admin['id'],
            'created_at': datetime.utcnow()
        }
        result = db.challenges.insert_one(c_data)
        c_data['_id'] = result.inserted_id
        c_data['id'] = str(result.inserted_id)
        challenges.append(c_data)

    # ── Scores for challenges ───────────────────────────────
    # Push-up challenge scores
    pushup_scores = [
        (users[1], 75), (users[2], 62), (users[3], 88), (users[4], 45),
        (users[5], 92), (users[6], 55), (users[7], 70), (users[8], 38),
        (users[9], 81), (users[10], 67), (users[11], 50), (admin, 72),
    ]
    for u, val in pushup_scores:
        s_data = {
            'user_id': u['id'],
            'challenge_id': challenges[0]['id'],
            'value': val,
            'recorded_by': admin['id'],
            'recorded_at': datetime.now() - timedelta(days=random.randint(1, 15)),
        }
        db.scores.insert_one(s_data)

    # 10K steps challenge
    steps_scores = [
        (users[1], 12450), (users[2], 11200), (users[3], 14800), (users[4], 9800),
        (users[5], 13600), (users[6], 10500), (users[7], 11800), (users[8], 8900),
        (users[9], 15200), (users[10], 10100), (admin, 11000),
    ]
    for u, val in steps_scores:
        s_data = {
            'user_id': u['id'],
            'challenge_id': challenges[1]['id'],
            'value': val,
            'recorded_by': admin['id'],
            'recorded_at': datetime.now() - timedelta(days=random.randint(1, 10)),
        }
        db.scores.insert_one(s_data)

    # HYROX time trial (past challenge — lower is better)
    hyrox_scores = [
        (users[1], 72.5), (users[3], 65.2), (users[5], 68.8),
        (users[7], 78.3), (users[9], 63.1), (users[10], 85.4),
        (users[2], 74.6), (admin, 70.0),
    ]
    for u, val in hyrox_scores:
        s_data = {
            'user_id': u['id'],
            'challenge_id': challenges[2]['id'],
            'value': val,
            'recorded_by': admin['id'],
            'recorded_at': datetime.now() - timedelta(days=random.randint(3, 25)),
        }
        db.scores.insert_one(s_data)

    # Plank hold
    plank_scores = [
        (users[1], 145), (users[2], 90), (users[3], 180), (users[4], 75),
        (users[5], 210), (users[6], 120), (users[7], 95), (users[8], 60),
        (users[9], 165), (admin, 130),
    ]
    for u, val in plank_scores:
        s_data = {
            'user_id': u['id'],
            'challenge_id': challenges[3]['id'],
            'value': val,
            'recorded_by': admin['id'],
            'recorded_at': datetime.now() - timedelta(days=random.randint(1, 8)),
        }
        db.scores.insert_one(s_data)

    # ── Blog Posts ──────────────────────────────────────────
    blogs = [
        {
            "title": "Why HYROX Is the Ultimate Fitness Challenge for Office Athletes",
            "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1200&q=80",
            "content": """HYROX has taken the fitness world by storm, and it's the perfect challenge for busy professionals who want to test their limits. Here's why we've made it a cornerstone of the CARS24 wellness program.

What is HYROX?

HYROX is a global fitness race that combines running with functional workout stations. The format is simple: 8 rounds of 1km runs, each followed by a different functional exercise. It's designed to test your complete fitness — endurance, strength, and mental toughness.

Why It Works for Us

Unlike traditional marathons or powerlifting meets, HYROX requires well-rounded fitness. You can't just be a runner or just be strong. This mirrors what we need in our daily lives — balance, versatility, and the ability to push through when things get tough.

The 8 Stations

1. Ski Erg (1000m) — Builds powerful shoulders and cardio
2. Sled Push (50m) — Raw leg strength and determination
3. Sled Pull (50m) — Grip strength and full-body engagement
4. Burpee Broad Jumps (80m) — Explosive power meets endurance
5. Rowing (1000m) — Controlled power output
6. Farmer's Carry (200m) — Functional strength at its finest
7. Sandbag Lunges (200m) — Leg endurance under load
8. Wall Balls (75-100 reps) — The ultimate finisher

How to Train

Our Monday and Friday HYROX Training sessions at the CARS24 Fitness Center are specifically designed to prepare you for race day. We break down each station, build your running base, and develop the mental resilience you need.

The CARS24 HYROX Team

We're building a team for the upcoming HYROX Bengaluru event in March. Whether you want to compete in the Singles, Doubles, or Relay category, there's a place for you.

Current Training Schedule:
• Monday 6:30 AM — HYROX Fundamentals
• Friday 7:00 AM — HYROX Race Prep (advanced)

Join us. Push your limits. Represent CARS24. 💪""",
            },
            {
                "title": "The Complete Guide to Protein Intake & Recovery Nutrition",
                "image_url": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=1200&q=80",
                "content": """Getting your nutrition right is just as important as showing up to workouts. Here's our comprehensive guide to protein intake and recovery nutrition for active professionals.

How Much Protein Do You Need?

The standard recommendation of 0.8g per kg of bodyweight is for sedentary individuals. If you're training regularly (which you should be!), here's what research suggests:

• Light exercise (2-3x/week): 1.2-1.4g per kg
• Regular training (4-5x/week): 1.4-1.8g per kg
• Intense training / muscle building: 1.8-2.2g per kg

For a 70kg person training 4x/week, that's 98-126g of protein daily.

Best Protein Sources (Indian Diet Friendly)

🥚 Eggs — 6g per egg (cheapest and most bioavailable)
🍗 Chicken breast — 31g per 100g
🐟 Fish (rohu/pomfret) — 20g per 100g
🫘 Rajma (kidney beans) — 24g per 100g (dry)
🥛 Paneer — 18g per 100g
🫙 Greek yogurt — 10g per 100g
🌱 Dal (moong/masoor) — 24g per 100g (dry)
🥜 Peanuts — 26g per 100g

Timing Matters

Pre-workout (1-2 hours before):
Light meal with carbs + moderate protein. Example: banana + peanut butter toast, or poha with sprouts.

Post-workout (within 60 minutes):
This is your recovery window. Aim for 20-30g protein + carbs. Example: protein shake with banana, or chicken rice bowl.

Before bed:
Slow-digesting protein helps overnight recovery. Example: glass of milk with turmeric (golden milk), or a small bowl of paneer.

Supplement Guide

Whey Protein: Convenient post-workout option. Look for brands with minimal additives. 1 scoop ≈ 24g protein.

Creatine Monohydrate: The most researched supplement. 3-5g daily improves strength and recovery. Safe for long-term use.

BCAA: Generally unnecessary if you're getting enough protein from food. Save your money.

Hydration

Don't forget water! Aim for:
• 3-4 liters daily (more if training)
• 500ml 30 mins before workout
• Sip during workout
• 500ml+ after workout

Add electrolytes (salt + lemon) if sweating heavily.

Sample Recovery Day Meal Plan

Breakfast: 3 eggs + 2 toast + banana (24g protein)
Mid-morning: Greek yogurt + almonds (15g protein)
Lunch: Chicken curry + rice + dal (35g protein)
Snack: Protein shake (24g protein)
Dinner: Paneer tikka + roti + salad (22g protein)
Before bed: Warm milk (8g protein)

Total: ~128g protein ✅

Remember: Consistency beats perfection. Start tracking your protein for one week and you'll be surprised how easy it becomes to hit your goals.

Questions? Ping the wellness team on Slack! 🥗""",
            },
            {
                "title": "CrossFit for Beginners: Everything You Need to Know Before Your First Class",
                "image_url": "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=1200&q=80",
                "content": """Thinking about joining our Wednesday CrossFit sessions but feeling intimidated? Don't be. Here's everything you need to know before walking into the box (that's CrossFit-speak for gym).

What is CrossFit?

CrossFit is a strength and conditioning program that combines elements from multiple disciplines — Olympic weightlifting, gymnastics, rowing, running, and more. Every session includes a WOD (Workout of the Day) that's different each time, so you never get bored.

The Truth About CrossFit

Let's address the elephant in the room: "Isn't CrossFit dangerous?"

No, not when done properly. Our sessions are coached by certified trainers who:
• Scale every movement to your fitness level
• Teach proper form before adding weight
• Monitor everyone during the workout
• Never push you beyond safe limits

Common Myths Debunked

❌ "You need to be fit to start CrossFit"
✅ CrossFit is designed to be scalable. Can't do a pull-up? We'll start with ring rows. Can't run 400m? Walk it.

❌ "You'll get bulky"
✅ CrossFit builds functional, lean muscle. You'll look athletic, not like a bodybuilder.

❌ "It's too expensive"
✅ Our CARS24 sessions are FREE for all employees!

What to Expect in Your First Class

1. Warm-up (10 min) — Dynamic stretching, light cardio, mobility work
2. Skill/Strength (15 min) — Learning or practicing a specific movement
3. WOD (15-20 min) — The main workout. You go at YOUR pace.
4. Cool-down (5 min) — Stretching and recovery

Essential CrossFit Terms

• WOD — Workout of the Day
• AMRAP — As Many Rounds As Possible (in a given time)
• EMOM — Every Minute On the Minute
• RX — Doing the workout as prescribed (at full difficulty)
• Scaled — Modified to your level (no shame in this!)
• PR — Personal Record (your new best!)
• Box — CrossFit gym

What to Wear & Bring

✅ Cross-training shoes (flat sole preferred over running shoes)
✅ Comfortable workout clothes
✅ Water bottle
✅ Small towel
✅ Positive attitude

❌ Don't wear: loose jewelry, open-toed shoes, or your ego

Our Schedule

📅 Every Wednesday, 7:00 AM
📍 CrossFit Box, CARS24 Campus Gym, Building A
👤 Coach: Vikram (CrossFit L2 certified)

Just show up 10 minutes early for your first class. We'll take care of the rest.

See you Wednesday! 🏋️""",
        },
    ]

    for i, b in enumerate(blogs):
        post_data = {
            'title': b["title"],
            'content': b["content"],
            'image_url': b["image_url"],
            'author_id': admin['id'],
            'is_published': True,
            'created_at': datetime.now() - timedelta(days=(len(blogs) - i) * 5),
        }
        db.blog_posts.insert_one(post_data)

    # ── Summary ─────────────────────────────────────────────
    print(f"✅ Seeded:")
    print(f"   {db.users.count_documents({})} users")
    print(f"   {db.events.count_documents({})} events ({len(weeks)} weeks × {len(event_templates)} templates)")
    print(f"   {db.participations.count_documents({})} participations")
    print(f"   {db.challenges.count_documents({})} challenges")
    print(f"   {db.scores.count_documents({})} scores")
    print(f"   {db.blog_posts.count_documents({})} blog posts")


if __name__ == "__main__":
    seed()
