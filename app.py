import streamlit as st
import random
import datetime
import matplotlib  # noqa: F401
import matplotlib.pyplot as plt
import pandas as pd  # noqa: F401
from PIL import Image  # noqa: F401
import time  # noqa: F401

# Page Configuration
st.set_page_config(page_title="Growth Mindset Challenge", page_icon="🌟", layout="wide")

# Initialize session state variables if they don't exist
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "reflections" not in st.session_state:
    st.session_state.reflections = []
if "goals" not in st.session_state:
    st.session_state.goals = []
if "achievements" not in st.session_state:
    st.session_state.achievements = {
        "first_challenge": False,
        "three_day_streak": False,
        "five_reflections": False,
        "three_goals": False,
        "mood_tracker": False
    }
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []
if "theme" not in st.session_state:
    st.session_state.theme = "light"
# Add selected_mood to session state
if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

# Motivational Quotes
quotes = [
    "Your potential is endless. Keep pushing forward!",
    "Every mistake is a step toward success.",
    "Growth begins where comfort ends.",
    "Believe in yourself and anything is possible.",
    "Challenges are opportunities in disguise!",
    "The only limit to your growth is your commitment.",
    "Small progress is still progress.",
    "Your attitude determines your direction.",
    "Success is falling nine times and getting up ten.",
    "The harder you work for something, the greater you'll feel when you achieve it."
]

# Helper functions
def increase_streak():
    st.session_state.streak += 1
    check_achievements()

def reset_streak():
    st.session_state.streak = 0

def add_reflection(challenge, reflection, mood):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    st.session_state.reflections.append({
        "date": today,
        "challenge": challenge,
        "reflection": reflection,
        "mood": mood
    })
    st.session_state.mood_history.append(mood)
    check_achievements()

def add_goal(goal):
    st.session_state.goals.append({"text": goal, "completed": False})
    check_achievements()

def toggle_goal(index):
    st.session_state.goals[index]["completed"] = not st.session_state.goals[index]["completed"]

def check_achievements():
    # First challenge achievement
    if len(st.session_state.reflections) >= 1:
        st.session_state.achievements["first_challenge"] = True
    
    # 3-day streak achievement
    if st.session_state.streak >= 3:
        st.session_state.achievements["three_day_streak"] = True
    
    # 5 reflections achievement
    if len(st.session_state.reflections) >= 5:
        st.session_state.achievements["five_reflections"] = True
    
    # 3 goals achievement
    if len(st.session_state.goals) >= 3:
        st.session_state.achievements["three_goals"] = True
    
    # Mood tracker achievement
    if len(st.session_state.mood_history) >= 7:
        st.session_state.achievements["mood_tracker"] = True

def show_progress_chart():
    # Generate data for the chart (in a real app, this would be actual user data)
    if len(st.session_state.reflections) > 0:
        data = [reflection.get("mood_score", random.randint(1, 10)) for reflection in st.session_state.reflections[-7:]]
        dates = [reflection.get("date", f"Day {i+1}") for i, reflection in enumerate(st.session_state.reflections[-7:])]
    else:
        # Sample data if no reflections yet
        data = [random.randint(1, 10) for _ in range(7)]
        today = datetime.datetime.now()
        dates = [(today - datetime.timedelta(days=i)).strftime("%a") for i in range(6, -1, -1)]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(dates, data, marker='o', linestyle='-', color='#22C55E')
    ax.set_title("Your Growth Journey Progress")
    ax.set_ylabel("Reflection Score")
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig

def show_mood_chart():
    if len(st.session_state.mood_history) > 0:
        # Convert mood strings to numeric values
        mood_map = {"terrible": 1, "bad": 2, "neutral": 3, "good": 4, "excellent": 5}
        mood_values = [mood_map.get(mood, 3) for mood in st.session_state.mood_history[-14:]]
        
        # Create dates for the x-axis
        num_days = len(mood_values)
        today = datetime.datetime.now()
        dates = [(today - datetime.timedelta(days=i)).strftime("%b %d") for i in range(num_days-1, -1, -1)]
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(dates, mood_values, marker='o', linestyle='-', color='#3B82F6')
        ax.set_title("Your Mood Tracker")
        ax.set_ylabel("Mood Level")
        ax.set_ylim(0.5, 5.5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(["Terrible", "Bad", "Neutral", "Good", "Excellent"])
        ax.grid(True, linestyle='--', alpha=0.7)
        
        return fig
    return None

# Main app
def main():
    # Sidebar for app navigation and settings
    with st.sidebar:
        st.title("🌟 Growth Mindset")
        
        # Theme selector
        theme_option = st.radio("App Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "light" else 1)
        st.session_state.theme = "light" if theme_option == "Light" else "dark"
        
        # Apply theme
        if st.session_state.theme == "dark":
            st.markdown("""
            <style>
            .stApp {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            .stButton button {
                background-color: #3B82F6;
                color: white;
            }
            .stTextInput input, .stTextArea textarea, .stSelectbox, .stMultiselect {
                background-color: #2D3748;
                color: white;
                border-color: #4A5568;
            }
            </style>
            """, unsafe_allow_html=True)
        
        # Navigation
        page = st.radio("Navigate", ["Daily Challenge", "Progress Tracker", "Goals", "Achievements", "Resources"])
        
        # Display streak
        st.metric("🔥 Current Streak", f"{st.session_state.streak} days")
        
        # Reset streak button
        if st.button("Reset Streak"):
            reset_streak()
            st.success("Streak reset! Start fresh and keep going!")
    
    # Main content area
    st.title("🌟 Growth Mindset Challenge")
    st.markdown(f"### *{random.choice(quotes)}*")
    
    # Daily Challenge page
    if page == "Daily Challenge":
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Today's Challenge")
            
            # Challenge Selection
            challenges = [
                "Reflect on a recent mistake and what you learned",
                "Encourage a friend to keep trying",
                "Try a new skill outside your comfort zone",
                "Replace negative thoughts with positive ones",
                "Write down 3 things you're grateful for",
                "Step out of your comfort zone today",
                "Practice active listening in a conversation",
                "Ask for feedback on something you're working on",
                "Learn something new for 30 minutes",
                "Meditate for 10 minutes focusing on growth"
            ]
            
            selected_challenge = st.selectbox("Pick a challenge for today:", challenges)
            
            if st.button("🚀 Accept the Challenge!"):
                increase_streak()
                st.success(f"🎯 Your Challenge: {selected_challenge}")
                st.balloons()
        
        with col2:
            st.subheader("📚 Daily Reflection")
            reflection = st.text_area("What did you learn today? Write your thoughts below:")
            
            # Mood selection
            st.write("How are you feeling today?")
            cols = st.columns(5)
            mood_options = ["terrible", "bad", "neutral", "good", "excellent"]
            mood_emojis = ["😫", "😔", "😐", "😊", "😁"]
            
            for i, (mood, emoji) in enumerate(zip(mood_options, mood_emojis)):
                with cols[i]:
                    if st.button(f"{emoji} {mood.capitalize()}", key=f"mood_{mood}"):
                        st.session_state.selected_mood = mood
            
            # Display selected mood
            if st.session_state.selected_mood:
                st.info(f"You selected: {st.session_state.selected_mood.capitalize()}")
            
            # Submit Reflection
            if st.button("📩 Submit Reflection"):
                if reflection and selected_challenge and st.session_state.selected_mood:
                    add_reflection(selected_challenge, reflection, st.session_state.selected_mood)
                    st.success("Reflection submitted successfully!")
                    # Clear mood selection after submission
                    st.session_state.selected_mood = None
                else:
                    st.error("Please select a challenge, write a reflection, and choose your mood.")
    
    # Progress Tracker page
    elif page == "Progress Tracker":
        st.subheader("📊 Your Growth Journey")
        
        # Progress chart
        progress_fig = show_progress_chart()
        st.pyplot(progress_fig)
        
        # Mood chart
        st.subheader("😊 Mood Tracker")
        mood_fig = show_mood_chart()
        if mood_fig:
            st.pyplot(mood_fig)
        else:
            st.info("Start tracking your mood to see your emotional journey!")
        
        # Reflection history
        st.subheader("📜 Reflection History")
        if st.session_state.reflections:
            for i, reflection in enumerate(reversed(st.session_state.reflections)):
                with st.expander(f"{reflection['date']} - {reflection['challenge'][:30]}..."):
                    st.write(f"**Challenge:** {reflection['challenge']}")
                    st.write(f"**Reflection:** {reflection['reflection']}")
                    st.write(f"**Mood:** {reflection['mood'].capitalize()}")
        else:
            st.info("No reflections yet. Start your journey by completing a daily challenge!")
    
    # Goals page
    elif page == "Goals":
        st.subheader("🎯 Personal Growth Goals")
        
        # Add new goal
        new_goal = st.text_input("Add a new goal:")
        if st.button("Add Goal"):
            if new_goal:
                add_goal(new_goal)
                st.success(f"Goal added: {new_goal}")
            else:
                st.warning("Please enter a goal.")
        
        # Display existing goals
        if st.session_state.goals:
            st.write("Your current goals:")
            for i, goal in enumerate(st.session_state.goals):
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    if goal["completed"]:
                        st.markdown(f"- ~~{goal['text']}~~ ✅")
                    else:
                        st.markdown(f"- {goal['text']}")
                with col2:
                    if st.button("✓" if not goal["completed"] else "↺", key=f"goal_{i}"):
                        toggle_goal(i)
        else:
            st.info("No goals set yet. Add your first goal above!")
    
    # Achievements page
    elif page == "Achievements":
        st.subheader("🏆 Your Achievements")
        
        achievements_data = [
            {"name": "First Challenge", "description": "Complete your first challenge", "unlocked": st.session_state.achievements["first_challenge"]},
            {"name": "3-Day Streak", "description": "Maintain a 3-day streak", "unlocked": st.session_state.achievements["three_day_streak"]},
            {"name": "Reflection Master", "description": "Complete 5 reflections", "unlocked": st.session_state.achievements["five_reflections"]},
            {"name": "Goal Setter", "description": "Set 3 personal goals", "unlocked": st.session_state.achievements["three_goals"]},
            {"name": "Mood Tracker", "description": "Track your mood for 7 days", "unlocked": st.session_state.achievements["mood_tracker"]}
        ]
        
        # Display achievements in a grid
        cols = st.columns(3)
        for i, achievement in enumerate(achievements_data):
            with cols[i % 3]:
                if achievement["unlocked"]:
                    st.success(f"🏆 {achievement['name']}")
                    st.write(achievement["description"])
                else:
                    st.info(f"🔒 {achievement['name']}")
                    st.write(achievement["description"])
    
    # Resources page
    elif page == "Resources":
        st.subheader("📚 Growth Mindset Resources")
        
        # Tabs for different resource types
        resource_tabs = st.tabs(["Videos", "Books", "Articles", "Tools"])
        
        with resource_tabs[0]:
            st.write("### Recommended Videos")
            video_col1, video_col2 = st.columns(2)
            
            with video_col1:
                st.write("**The Power of Yet**")
                st.write("Carol Dweck explains the power of 'not yet' in developing a growth mindset.")
                st.write("[Watch on YouTube](https://www.youtube.com/watch?v=J-swZaKN2Ic)")
            
            with video_col2:
                st.write("**Growth Mindset vs. Fixed Mindset**")
                st.write("Learn the difference" )
                st.write("**Growth Mindset vs. Fixed Mindset**")
                st.write("Learn the difference between growth and fixed mindsets.")
                st.write("[Watch on YouTube](https://www.youtube.com/watch?v=KUWn_TJTrnU)")
        
    
        with resource_tabs[1]:
            st.write("### Recommended Books")
            book_col1, book_col2 = st.columns(2)
            
            with book_col1:
                st.write("**Mindset: The New Psychology of Success**")
                st.write("By Carol Dweck")
                st.write("The groundbreaking book that introduced the concept of growth mindset.")
            
            with book_col2:
                st.write("**Grit: The Power of Passion and Perseverance**")
                st.write("By Angela Duckworth")
                st.write("Explores how passion and perseverance are more important than talent.")
        
        with resource_tabs[2]:
            st.write("### Helpful Articles")
            st.write("- [Developing a Growth Mindset with Carol Dweck](https://www.mindsetworks.com/science/)")
            st.write("- [The Learning Myth: Why I'll Never Tell My Son He's Smart](https://www.khanacademy.org/college-careers-more/talks-and-interviews/talks-and-interviews-unit/conversations-with-sal/a/the-learning-myth-why-ill-never-tell-my-son-hes-smart)")
            st.write("- [How to Develop a Growth Mindset](https://hbr.org/2016/01/what-having-a-growth-mindset-actually-means)")
        
        with resource_tabs[3]:
            st.write("### Useful Tools")
            st.write("- **Habit Tracker Apps**: Track your daily growth habits")
            st.write("- **Journaling Templates**: Structure your reflections")
            st.write("- **Meditation Apps**: Practice mindfulness to support growth")
            st.write("- **Learning Platforms**: Continuously develop new skills")

# Run the app
if __name__ == "__main__":
    main()