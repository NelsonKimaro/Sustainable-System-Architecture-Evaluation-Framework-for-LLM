import numpy as np
from scipy.special import gamma

import numpy as np
from scipy.special import gamma
# from hotspot import get_current_temperatures  


def get_current_temperatures():
    # Simulate temperatures or get from file/model
    return [84.406, 86.728, 85.974, 85.023]  #[40.1, 42.54, 43.23, 40,21] # Degrees Celsius


def eta_from_temperature(T_C, Ea=0.7, A=1e9): # Typically, Ea ranges from 0.3 to 0.9 for electronics       ##########################
    """
    Compute η_j (scale parameter) from temperature using the Arrhenius model.
    """
    k = 8.617e-5  # Boltzmann constant in eV/K
    T_K = np.array(T_C) + 273.15
    lambdas = A * np.exp(-Ea / (k * T_K))
    etas = 1 / lambdas
    return etas


class LifetimeReliability:
    def __init__(self, beta: float, t: np.ndarray, Ea: float = 0.7, A: float = 1e9):                 #################################
        self.beta = beta
        self.t = t
        self.Ea = Ea
        self.A = A
        self.update_etas()  # Automatically fetch and compute η values

    def update_etas(self):
        temperatures = get_current_temperatures()  # Get from HotSpot model
        self.etas = eta_from_temperature(temperatures, self.Ea, self.A)

    def system_reliability(self) -> np.ndarray:
        etas = np.array(self.etas)
        t = np.array(self.t)
        failure_sum = np.sum((t[:, None] / etas)**self.beta, axis=1)
        return np.exp(-failure_sum)

    def MTTF_fast_system(self) -> float:
        eta_term = np.sum(1 / np.array(self.etas) ** self.beta)
        return gamma(1 + 1/self.beta) / (self.beta * (eta_term ** (1 / self.beta)))






if __name__ == "__main__":
    time = np.linspace(0, 24, 300)
    model = LifetimeReliability(beta=1.5, t=time) #etas = [1000, 950, 980, 1010]
    
    R_t = model.system_reliability()
    MTTF = model.MTTF_fast_system()

    print(f"MTTF = {MTTF:.2f} hours")





    # Optional: Plot reliability curve
    import matplotlib.pyplot as plt
    plt.plot(time, R_t*100, label="System Reliability R(t)")
    plt.axvline(MTTF, color='r', linestyle='--', label=f"MTTF ≈ {MTTF:.0f} h")
    plt.xlabel("Time (hours)")
    plt.ylabel("Reliability(%)")
    plt.title("System Reliability over Time")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()











# import matplotlib.pyplot as plt
# import numpy as np

# # Simulate the reliability function R(t) = e^(-t/MTTF)
# MTTF_values = [1000, 5000, 10000, 100000]  # different system MTTFs in hours
# active_lifetime = np.linspace(0, 20000, 500)  # time from 0 to 20,000 hours

# plt.figure(figsize=(10, 6))

# for mttf in MTTF_values:
#     reliability = np.exp(-active_lifetime / mttf)
#     plt.plot(active_lifetime, reliability, label=f"MTTF = {mttf} hours")

# plt.title("System Reliability Over Time")
# plt.xlabel("Time (hours)")
# plt.ylabel("Reliability R(t)")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()



# import numpy as np
# import matplotlib.pyplot as plt

# # Constants
# MTTF = 1000000 # in hours
# alpha_u = 1.5
# alpha_T = 0.07
# T_ref = 50  # degrees Celsius

# # Simulated time (e.g., in hours)
# t = np.arange(0, 43800, 100)  # simulate over 20,000 hours

# # Simulated usage patterns
# utilization = np.linspace(0.3, 1.0, len(t))  # growing load
# temperature = 50 + 10 * np.sin(2 * np.pi * t / 10000)  # temp fluctuates between 50–60°C

# # Reliability components
# R_base = np.exp(-t / MTTF)
# f_util = np.exp(-alpha_u * utilization)
# f_temp = np.exp(-alpha_T * (temperature - T_ref))

# # Combined reliability
# R_total = R_base * f_util * f_temp

# # Plot
# plt.figure(figsize=(10, 5))
# plt.plot(t, R_total, label="Combined Reliability R(t)", color='green')
# plt.plot(t, R_base, label="Baseline MTTF Decay", linestyle='--')
# plt.title("System Reliability Over Time")
# plt.xlabel("Time (hours)")
# plt.ylabel("Reliability R(t)")
# plt.ylim(0, 1.05)
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()



# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import weibull_min

# k = 0.8  # shape
# lam = 1  # scale

# x = np.linspace(0, 5, 100)
# pdf = weibull_min.pdf(x, k, scale=lam)

# plt.plot(x, pdf, label=f'k={k}, λ={lam}')
# plt.title("Weibull Distribution PDF")
# plt.xlabel("x")
# plt.ylabel("Probability Density")
# plt.legend()
# plt.grid(True)
# plt.show()










# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.special import gamma

# # === Weibull system parameters ===
# beta = 1.5  # Shape parameter
# etas = [1000, 950, 980, 1010]  # Scale parameters η_j for each component

# # === Time vector (e.g., up to 3000 hours) ===
# t = np.linspace(0, 3000, 300)

# # === Compute R_system(t) ===
# def reliability_fast_system(t, beta, etas):
#     etas = np.array(etas)
#     failure_sum = np.sum((t[:, None] / etas) ** beta, axis=1)
#     return np.exp(-failure_sum)

# R_t = reliability_fast_system(t, beta, etas)

# # === Compute MTTF from formula ===
# def mttf_fast_system(beta, etas):
#     eta_term = np.sum(1 / np.array(etas) ** beta)
#     return gamma(1 + 1 / beta) / (beta * (eta_term ** (1 / beta)))

# mttf = mttf_fast_system(beta, etas)
# print(f"MTTF (Fast System): {mttf:.2f} hours")

# # === Plot ===
# plt.figure(figsize=(8, 5))
# plt.plot(t, R_t, label='Reliability R(t)', color='blue', lw=2)
# plt.axvline(mttf, color='red', linestyle='--', label=f'MTTF ≈ {mttf:.0f} h')
# plt.title("System Reliability over Time (Fast System Model)")
# plt.xlabel("Time (hours)")
# plt.ylabel("Reliability R(t)")
# plt.ylim(0, 1.05)
# plt.grid(True)
# plt.legend()
# plt.tight_layout()
# plt.show()


