import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
st.set_page_config(page_title="Orbit Architect", layout="centered")

# --- STYLES ---
st.markdown("""
<style>
    .main-header {font-size: 36px; font-weight: bold; color: #333;}
    .sub-header {font-size: 24px; font-weight: bold; color: #555;}
    .highlight {background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 20px;}
    .success-msg {color: #2e7d32; font-weight: bold; font-size: 18px;}
    .error-msg {color: #d32f2f; font-weight: bold; font-size: 18px;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<div class="main-header">Orbit Architect: Level 2</div>', unsafe_allow_html=True)
st.caption("Based on Lecture 1: Two-Body Orbital Mechanics (Pages 2-3)")
st.divider()

# --- PART 1: THE INVERSE SQUARE LAW ---
st.markdown('<div class="sub-header">Part 1: The Invisible Tether</div>', unsafe_allow_html=True)
st.write("Newton discovered that gravity is a force that acts at a distance. But how does distance change the strength of that pull?")

# Context from lecture
with st.expander("Show Lecture Notes (Page 2)"):
    st.latex(r"\vec{F}_g = -\frac{GMm}{r^2} \hat{u}_r")
    st.write("The force is inversely proportional to the square of the distance ($r^2$).")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Controls")
    # Slider for Distance (r)
    r_val = st.slider("Distance (r)", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
    
    # Calculate Force Magnitude (Arbitrary units for visualization)
    G_sim = 1000
    force_mag = G_sim / (r_val ** 2)
    
    st.metric(label="Gravitational Force", value=f"{force_mag:.2f} N")
    
    st.info(f"""
    **Observation:**
    If you double the distance from 2 to 4, the force drops from **250** to **62.5**.
    
    That's a **4x** decrease!
    """)

with col2:
    # Plotting the visualization
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Sun (M) at origin
    ax.scatter([0], [0], s=500, c='gold', edgecolors='orange', label='Sun (M)', zorder=2)
    
    # Planet (m) at distance r
    ax.scatter([r_val], [0], s=100, c='dodgerblue', label='Planet (m)', zorder=2)
    
    # Force Vector Arrow
    # Arrow starts at planet and points towards sun (negative direction)
    # Length scales with force_mag
    arrow_len = force_mag / 50 # Scaling for display
    ax.arrow(r_val, 0, -arrow_len, 0, head_width=0.3, head_length=0.3, fc='red', ec='red', width=0.1, zorder=1)
    
    # Annotations
    ax.text(r_val, 0.5, "You are here", ha='center')
    if arrow_len > 0.5:
        ax.text(r_val - arrow_len/2, -1, r"$\vec{F}_g$", color='red', ha='center')
    
    # Formatting
    ax.set_xlim(-1, 12)
    ax.set_ylim(-3, 3)
    ax.axhline(0, color='gray', linestyle='--', alpha=0.3)
    ax.set_yticks([])
    ax.set_xlabel("Distance (r)")
    ax.set_title(f"Visualizing Gravity: 1/r²")
    ax.legend(loc='upper right')
    
    st.pyplot(fig)

st.divider()

# --- PART 2: THE VECTOR DIRECTOR GAME ---
st.markdown('<div class="sub-header">Part 2: The Direction of the Force</div>', unsafe_allow_html=True)
st.write("""
Gravity is a **vector**. It has a magnitude (which you just saw) and a **direction**.
In the lecture (Page 2), the vector $\\vec{r}$ points *from* the Sun *to* the planet.
The force acts **opposite** to that direction.
""")

st.markdown("""
<div class="highlight">
    <b>Mission:</b> The planet is lost in space. Orient the red force vector so it points correctly toward the Sun.
</div>
""", unsafe_allow_html=True)

# Game State
if 'target_x' not in st.session_state:
    st.session_state.target_x = np.random.uniform(2, 8)
    st.session_state.target_y = np.random.uniform(2, 8)

# Coordinates
sun_pos = np.array([0, 0])
planet_pos = np.array([st.session_state.target_x, st.session_state.target_y])

# Calculate correct angle (from planet pointing to sun)
# Vector from Planet to Sun = Sun - Planet = -Planet
correct_vector = sun_pos - planet_pos
correct_angle_rad = np.arctan2(correct_vector[1], correct_vector[0])
correct_angle_deg = np.degrees(correct_angle_rad)
if correct_angle_deg < 0:
    correct_angle_deg += 360

col_game_1, col_game_2 = st.columns([1, 2])

with col_game_1:
    user_angle = st.number_input("Set Angle (Degrees)", min_value=0, max_value=360, value=0, step=10)
    
    check_btn = st.button("Lock In Vector")
    reset_btn = st.button("New Position")
    
    if reset_btn:
        st.session_state.target_x = np.random.uniform(2, 8)
        st.session_state.target_y = np.random.uniform(-5, 5) # Let's vary Y more
        st.rerun()

with col_game_2:
    fig2, ax2 = plt.subplots(figsize=(5, 5))
    
    # Draw Sun
    ax2.scatter([0], [0], s=300, c='gold', edgecolors='orange', zorder=3)
    ax2.text(0, -1, "Sun", ha='center')
    
    # Draw Planet
    ax2.scatter([planet_pos[0]], [planet_pos[1]], s=100, c='dodgerblue', zorder=3)
    
    # Draw User's Vector
    # Convert user angle to dx, dy
    user_rad = np.radians(user_angle)
    vec_len = 3
    dx = vec_len * np.cos(user_rad)
    dy = vec_len * np.sin(user_rad)
    
    ax2.arrow(planet_pos[0], planet_pos[1], dx, dy, 
              head_width=0.4, head_length=0.5, fc='red', ec='red', width=0.1, label='Your Force')
    
    # Draw "Position Vector" r (dashed line)
    ax2.plot([0, planet_pos[0]], [0, planet_pos[1]], 'k--', alpha=0.3, label='Position Vector r')

    ax2.set_xlim(-10, 10)
    ax2.set_ylim(-10, 10)
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    st.pyplot(fig2)

# Feedback Logic
if check_btn:
    diff = abs(user_angle - correct_angle_deg)
    # Handle wrap around (e.g. 359 vs 1)
    diff = min(diff, 360 - diff)
    
    if diff < 10:
        st.markdown(f'<div class="success-msg">Correct! The force pulls the planet directly toward the Sun.</div>', unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f'<div class="error-msg">Not quite. Gravity is attractive. It should point to the center (0,0).</div>', unsafe_allow_html=True)
        st.write(f"Hint: Try an angle closer to {int(correct_angle_deg)}°")

st.divider()
st.caption("Concept derived from Bate Ch. 1 & Curtis Ch. 2[cite: 2].")