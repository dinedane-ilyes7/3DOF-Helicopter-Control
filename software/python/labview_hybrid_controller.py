# ============================================================
# 3DOF HELICOPTER — HYBRID CONTROLLER (1250 US BASELINE)
# ============================================================
import numpy as np
import math

# LQI Feedback Gains from MATLAB (Calculated for RADIAN states)
Kst = np.array([
    [0.0,     0.0,   165.5589,  28.9140,   0.0,      0.0    ],
    [13.4030, 0.0,     0.0,      0.0,    414.6032, 540.2084 ]
])

Ki = np.array([
    [125.1792,   0.0    ],
    [0.0,      120.3173 ]
])

# MODIFIED: Lowered starting baseline from 1300 to 1250
PWM_BASE = 1250
PWM_MIN  = 1000
PWM_MAX  = 1700

DERIVATIVE_ALPHA = 0.30  # Low-pass filter coefficient for velocity noise
INT_LIM = 1.0            # Integrator clamp limit for travel axis

# System background memory cache
# Layout: [prev_p, prev_e, prev_t, filt_dp, filt_de, filt_dt, I_elev, I_travel]
history = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def reset_system():
    """Call this once at LabVIEW startup to completely clear the cache"""
    global history
    history = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    return "Controller Reset Successful"

def compute_pwm(theta_p_deg, theta_e_deg, theta_t_deg, r_elev_deg, r_travel_deg):
    global history
    dt = 0.01  # 10ms execution time step

    # 1. Convert incoming LabVIEW Degrees to Radians
    theta_p = math.radians(theta_p_deg)
    theta_e = math.radians(theta_e_deg)
    theta_t = math.radians(theta_t_deg)
    r_elev  = math.radians(r_elev_deg)
    r_travel = math.radians(r_travel_deg)

    # Safety Auto-Reset: If reference knobs return to absolute zero, flush tracking states
    if r_elev_deg == 0.0 and r_travel_deg == 0.0:
        history = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    try:
        # Unpack background variables (stored in radians)
        prev_p, prev_e, prev_t, filt_dp, filt_de, filt_dt, I_elev, I_travel = history

        # 2. Calculate Raw Derivatives (Velocities in rad/s)
        raw_dp = (theta_p - prev_p) / dt
        raw_de = (theta_e - prev_e) / dt
        raw_dt = (theta_t - prev_t) / dt

        # 3. Filter derivative velocity noise
        new_filt_dp = (DERIVATIVE_ALPHA * raw_dp) + ((1.0 - DERIVATIVE_ALPHA) * filt_dp)
        new_filt_de = (DERIVATIVE_ALPHA * raw_de) + ((1.0 - DERIVATIVE_ALPHA) * filt_de)
        new_filt_dt = (DERIVATIVE_ALPHA * raw_dt) + ((1.0 - DERIVATIVE_ALPHA) * filt_dt)

        # 4. Process Isolated Elevation Target Tracking Loop (in Radians)
        elev_error = r_elev - theta_e
        new_I_elev = I_elev + (elev_error * dt)
        new_I_elev = float(np.clip(new_I_elev, -2.5, 2.5))  # Anti-windup ceiling

        # Math: Boosted Integral thrust minus velocity dampening
        elevation_u_sum = (new_I_elev * 320.0) - (25.0 * new_filt_de)

        # 5. Process Remaining Pitch/Travel tracking via original LQI math vectors
        x_plant = np.array([theta_p, new_filt_dp, theta_e, new_filt_de, theta_t, new_filt_dt])

        new_I_travel = float(np.clip(I_travel + (r_travel - theta_t) * dt, -INT_LIM, INT_LIM))
        x_int = np.array([0.0, new_I_travel])  # Row 0 (elevation) zeroed out for the LQI matrix

        u_lqi = -Kst @ x_plant + Ki @ x_int
        u_differential = float(np.clip(u_lqi[1], -0.5, 0.5))

        # 6. Actuator Mixing Logic (Map to Microseconds using lower PWM_BASE)
        pwm1 = int(np.clip(PWM_BASE + elevation_u_sum + (u_differential * 300.0), PWM_MIN, PWM_MAX))
        pwm2 = int(np.clip(PWM_BASE + elevation_u_sum - (u_differential * 300.0), PWM_MIN, PWM_MAX))

        # Save history for next loop step
        history = [theta_p, theta_e, theta_t, new_filt_dp, new_filt_de, new_filt_dt, new_I_elev, new_I_travel]

        return f"{pwm1},{pwm2}\n"

    except Exception as e:
        return f"{PWM_BASE},{PWM_BASE}\n"
