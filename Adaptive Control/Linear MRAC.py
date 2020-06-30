import numpy as np 
import scipy as sp 
from matplotlib import pyplot as plt 
from scipy.integrate import odeint

def rk4(x0, u, f, h = 0.01):
    k1 = f(x0, u)
    k2 = f(x0 + h*(k1/2), u)
    k3 = f(x0 + h*(k2/2), u)
    k4 = f(x0 + h*k3, u)

    return h*((k1 + 2*k2 + 2*k3 + k4)/6)

def fx_model(x1 ,r):
    x_dot1 = -1*x1 + r
    return x_dot1

def fx_plant(x1, u):
    x_dot1 = x1 + b*u + b*(theta_c*x1)
    return x_dot1

def euler_int(x0,dx,h):
    x0 = x0+dx*h
    return x0

current_time = 0
theta_c = 4
a = 1 
b = 1 
a_m = -1 
b_m = 1 
r_t = np.sin(current_time)
theta_i = 0 
x0_model = 2
x0_plant = 2 
N = 10000
gamma = 2 #adaptive rate
adaptive_law = 0

t = np.zeros(N)
theta_list = np.zeros(N)
x_model = np.zeros(N)
x_plant = np.zeros(N)
ref = np.zeros(N)
e = np.zeros(N)

for i in range(N):
    if i > 3000:
        theta_c = 6
    x0_model = x0_model + rk4(x0_model, r_t, fx_model)
    u = -2*x_plant[i] + r_t - theta_i*x_plant[i]
    x0_plant = x0_plant + rk4(x0_plant, u, fx_plant)
    error = x0_model - x0_plant
    adaptive_law = -gamma*x0_plant*error
    theta_i = euler_int(theta_i, adaptive_law, 0.01)
    current_time = current_time + 0.01
    r_t = np.sin(current_time)
    try:
        x_model[i+1] = x0_model
        x_plant[i+1] = x0_plant
        t[i+1] = current_time
        ref[i+1] = r_t
        e[i+1] = error
        theta_list[i+1] = theta_i
    except: 
        pass

plt.plot(t, x_plant, label = "Plant with Uncertainty")
plt.plot(t, x_model, label = "Reference Model")
plt.legend()
plt.show()

plt.plot(t, e, label = "Error")
plt.legend()
plt.show()

plt.plot(t, theta_list, label = 'Uncertainty Parameter')
plt.legend()
plt.show()