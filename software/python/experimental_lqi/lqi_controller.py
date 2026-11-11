# ============================================================
# LQI CONTROLLER — Python Node for LabVIEW
# ============================================================
# Inputs  : theta_p, theta_e, theta_t (rad)
#           r_elev, r_travel (rad) — from LabVIEW front panel
# Outputs : pwm1, pwm2 (integer, 1000-1600)
# ============================================================

import numpy as np

# ============================================================
# GAINS — from your MATLAB LQI design
# ============================================================
Kst = np.array([
    [ 0.0,      0.0,    165.5589,  28.9140,   0.0,      0.0    ],
    [ 13.4030,  0.0,      0.0,      0.0,    414.6032, 540.2084 ]
])

Ki = np.array([
    [125.1792,   0.0     ],
    [  0.0,    120.3173  ]
])

# ============================================================
# CONTROLLER PARAMETERS
# ============================================================
Ts       = 0.01      # 10ms sampling
PWM_BASE = 1300      # base PWM at hover
PWM_MIN  = 1000
PWM_MAX  = 1600

# ============================================================
# PERSISTENT STATE — survives between LabVIEW calls
# ============================================================
prev_theta_p = 0.0
prev_theta_e = 0.0
prev_theta_t = 0.0
I_elev       = 0.0
I_travel     = 0.0
first_call   = True

# ============================================================
# MAIN CONTROL FUNCTION
# Called every 10ms by LabVIEW Python node
# ============================================================
def compute_pwm(theta_p, theta_e, theta_t, r_elev, r_travel):
    global prev_theta_p, prev_theta_e, prev_theta_t
    global I_elev, I_travel, first_call

    # On first call initialise previous values
    if first_call:
        prev_theta_p = theta_p
        prev_theta_e = theta_e
        prev_theta_t = theta_t
        first_call   = False

    # ----------------------------------------------------------
    # 1. DIFFERENTIATE — numerical derivative
    # ----------------------------------------------------------
    d_theta_p = (theta_p - prev_theta_p) / Ts
    d_theta_e = (theta_e - prev_theta_e) / Ts
    d_theta_t = (theta_t - prev_theta_t) / Ts

    prev_theta_p = theta_p
    prev_theta_e = theta_e
    prev_theta_t = theta_t

    # ----------------------------------------------------------
    # 2. UPDATE INTEGRATORS with tracking error
    # ----------------------------------------------------------
    e_elev   = r_elev   - theta_e
    e_travel = r_travel - theta_t

    I_elev   += Ts * e_elev
    I_travel += Ts * e_travel

    # ----------------------------------------------------------
    # 3. ASSEMBLE STATE VECTOR
    # ----------------------------------------------------------
    x_plant = np.array([
        theta_p,
        d_theta_p,
        theta_e,
        d_theta_e,
        theta_t,
        d_theta_t
    ])

    x_int = np.array([I_elev, I_travel])

    # ----------------------------------------------------------
    # 4. CONTROL LAW
    # u = -Kst * x_plant + Ki * x_int
    # ----------------------------------------------------------
    u = -Kst @ x_plant + Ki @ x_int

    Usum  = u[0]
    Udiff = u[1]

    # ----------------------------------------------------------
    # 5. SATURATE
    # ----------------------------------------------------------
    Usum  = float(np.clip(Usum,  -1.0,  1.0))
    Udiff = float(np.clip(Udiff, -0.5,  0.5))

    # ----------------------------------------------------------
    # 6. CONVERT TO PWM
    # PWM_BASE + elevation offset + differential
    # ----------------------------------------------------------
    pwm1 = int(PWM_BASE + Usum * 300 + Udiff * 300)
    pwm2 = int(PWM_BASE + Usum * 300 - Udiff * 300)

    pwm1 = int(np.clip(pwm1, PWM_MIN, PWM_MAX))
    pwm2 = int(np.clip(pwm2, PWM_MIN, PWM_MAX))

    return pwm1, pwm2

# ============================================================
# RESET FUNCTION — call from LabVIEW stop button
# ============================================================
def reset_controller():
    global prev_theta_p, prev_theta_e, prev_theta_t
    global I_elev, I_travel, first_call
    prev_theta_p = 0.0
    prev_theta_e = 0.0
    prev_theta_t = 0.0
    I_elev       = 0.0
    I_travel     = 0.0
    first_call   = True