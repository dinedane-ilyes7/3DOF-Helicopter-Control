# ============================================================
# 3DOF HELICOPTER — LQI CONTROLLER
# For LabVIEW Python Node
# Returns float values (DBL) for LabVIEW compatibility
# ============================================================

import numpy as np
import time

# ============================================================
# LQI GAINS — from MATLAB lqrd
# ============================================================
Kst = np.array([
    [0.0,     0.0,   165.5589,  28.9140,   0.0,      0.0    ],
    [13.4030, 0.0,     0.0,      0.0,    414.6032, 540.2084 ]
])

Ki = np.array([
    [125.1792,   0.0    ],
    [0.0,      120.3173 ]
])

# ============================================================
# PWM SETTINGS
# ============================================================
PWM_BASE = 1300
PWM_MIN  = 1100
PWM_MAX  = 1500

# ============================================================
# FILTER SETTINGS
# ============================================================
DERIVATIVE_ALPHA = 0.85

# ============================================================
# INTEGRATOR LIMITS
# ============================================================
INT_LIM = 2.0

# ============================================================
# PERSISTENT STATES
# ============================================================
prev_theta_p = 0.0
prev_theta_e = 0.0
prev_theta_t = 0.0

d_theta_p_f  = 0.0
d_theta_e_f  = 0.0
d_theta_t_f  = 0.0

I_elev   = 0.0
I_travel = 0.0

prev_time  = None
first_call = True

# ============================================================
# MAIN FUNCTION
# ============================================================
def compute_pwm(theta_p, theta_e, theta_t, r_elev, r_travel):

    global prev_theta_p, prev_theta_e, prev_theta_t
    global d_theta_p_f,  d_theta_e_f,  d_theta_t_f
    global I_elev, I_travel
    global prev_time, first_call

    # --------------------------------------------------------
    # 1. TIME STEP
    # --------------------------------------------------------
    current_time = time.time()

    if first_call:
        prev_time = current_time

    dt = current_time - prev_time

    if dt <= 0.0:
        dt = 0.01
    if dt > 0.05:
        dt = 0.01

    prev_time = current_time

    # --------------------------------------------------------
    # 2. FIRST CALL INITIALISATION
    # --------------------------------------------------------
    if first_call:
        prev_theta_p = float(theta_p)
        prev_theta_e = float(theta_e)
        prev_theta_t = float(theta_t)
        first_call   = False
        return float(PWM_BASE), float(PWM_BASE)

    # --------------------------------------------------------
    # 3. RAW DERIVATIVES
    # --------------------------------------------------------
    raw_d_p = (float(theta_p) - prev_theta_p) / dt
    raw_d_e = (float(theta_e) - prev_theta_e) / dt
    raw_d_t = (float(theta_t) - prev_theta_t) / dt

    prev_theta_p = float(theta_p)
    prev_theta_e = float(theta_e)
    prev_theta_t = float(theta_t)

    # --------------------------------------------------------
    # 4. LOW PASS FILTER ON DERIVATIVES
    # --------------------------------------------------------
    a = DERIVATIVE_ALPHA

    d_theta_p_f = a * d_theta_p_f + (1.0 - a) * raw_d_p
    d_theta_e_f = a * d_theta_e_f + (1.0 - a) * raw_d_e
    d_theta_t_f = a * d_theta_t_f + (1.0 - a) * raw_d_t

    # --------------------------------------------------------
    # 5. TRACKING ERRORS
    # --------------------------------------------------------
    e_elev   = float(r_elev)   - float(theta_e)
    e_travel = float(r_travel) - float(theta_t)

    # --------------------------------------------------------
    # 6. INTEGRATORS WITH ANTI-WINDUP
    # --------------------------------------------------------
    I_elev   += e_elev   * dt
    I_travel += e_travel * dt

    I_elev   = float(np.clip(I_elev,   -INT_LIM, INT_LIM))
    I_travel = float(np.clip(I_travel, -INT_LIM, INT_LIM))

    # --------------------------------------------------------
    # 7. STATE VECTOR
    # --------------------------------------------------------
    x_plant = np.array([
        float(theta_p),
        d_theta_p_f,
        float(theta_e),
        d_theta_e_f,
        float(theta_t),
        d_theta_t_f
    ])

    x_int = np.array([I_elev, I_travel])

    # --------------------------------------------------------
    # 8. LQI CONTROL LAW
    # --------------------------------------------------------
    u     = -Kst @ x_plant + Ki @ x_int
    Usum  = float(u[0])
    Udiff = float(u[1])

    # --------------------------------------------------------
    # 9. SATURATION
    # --------------------------------------------------------
    # Softer controller output
    Usum  = float(np.clip(Usum,  -0.2, 0.2))
    Udiff = float(np.clip(Udiff, -0.1, 0.1))
    # --------------------------------------------------------
    # 10. PWM MIXING
    # --------------------------------------------------------
    # Smaller PWM conversion
    pwm1 = float(int(PWM_BASE + Usum*100 + Udiff*100))
    pwm2 = float(int(PWM_BASE + Usum*100 - Udiff*100))

    pwm1 = float(np.clip(pwm1, PWM_MIN, PWM_MAX))
    pwm2 = float(np.clip(pwm2, PWM_MIN, PWM_MAX))

    return float(pwm1), float(pwm2)

# ============================================================
# RESET FUNCTION — call from LabVIEW stop button
# ============================================================
def reset_controller():

    global prev_theta_p, prev_theta_e, prev_theta_t
    global d_theta_p_f,  d_theta_e_f,  d_theta_t_f
    global I_elev, I_travel
    global prev_time, first_call

    prev_theta_p = 0.0
    prev_theta_e = 0.0
    prev_theta_t = 0.0

    d_theta_p_f  = 0.0
    d_theta_e_f  = 0.0
    d_theta_t_f  = 0.0

    I_elev   = 0.0
    I_travel = 0.0

    prev_time  = None
    first_call = True