import numpy as np
import matplotlib.pyplot as plt

def cubicspline(x,y):
    x = np.array(x)
    y = np.array(y)
    n = len(x) - 1  # We have n + 1 points
    A = np.zeros((4*n, 4*n))
    b = np.zeros(4*n)
    
    j = np.arange(0, 4*n, 4)  #  Columns related to x**3
    i = np.arange(0, 4*n, 2)  #  Even lines
    i = i[:len(j)]  # Adjusting to use both indexes at the same time

    # Calculating x³, x², x and 1 for the left point
    A[i, j] = x[:-1]**3  
    A[i, j+1] = x[:-1]**2
    A[i, j+2] = x[:-1]
    A[i, j+3] = 1

    # Calculating x³, x², x and 1 for the right point
    A[i+1, j] = x[1:]**3
    A[i+1, j+1] = x[1:]**2
    A[i+1, j+2] = x[1:]
    A[i+1, j+3] = 1 

    # y values
    k = np.arange(0, 4*n, 2)[:len(j)]
    b[k] = y[:-1]
    b[k+1] = y[1:]

    # Same first derivative in each point for all polynomials
    i = np.arange(2*n, 4*n)[:len(j)-1]
    j = j[:-1]
    A[i, j] = 3*x[1:-1]**2
    A[i, j+1] = 2*x[1:-1]
    A[i, j+2] = 1
    A[i, j+4] = -3*x[1:-1]**2
    A[i, j+5] = -2*x[1:-1]
    A[i, j+6] = -1

    # Same second derivative in each point for all polynomials
    i = i + n - 1
    A[i, j] = 6*x[1:-1]
    A[i, j+1] = 2
    A[i, j+4] = -6*x[1:-1]
    A[i, j+5] = -2

    # Natural spline equations
    A[4*n-2, 0] = 6*x[0]
    A[4*n-2, 1] = 2
    A[4*n-1, 4*n-4] = 6*x[-1]
    A[4*n-1, 4*n-3] = 2

    # Solve the linear system
    coefs = np.linalg.solve(A,b)    
    return np.array([coefs[::4], coefs[1::4], coefs[2::4], coefs[3::4]])


def print_fixed_n(n):  # Fixed length for numbers
    print("{:10.4f}".format(n), end='') # or print "{:10.4f}".format(x


def print_fixed_s(s, length):  # Fixed lenght for strings
    # The function prints a string with fixed length
    half_len_diff = (length - len(s))/2
    if half_len_diff%1 != 1:
        left = int(np.ceil(half_len_diff))
    else:
        left = int(half_len_diff)
    right = int(np.floor(half_len_diff))

    for i in range(left):
         print(' ', end='')
    print(s, end='')
    for i in range(right):
        print(' ', end='')


def calc_third_poly(a, b, c, d, x):
    return a*x**3 + b*x**2 + c*x + d

def print_spline_coefs(spline_coefs):
    for charac in ['j', 'ai', 'bi', 'ci', 'di']:
        print_fixed_s(charac, 10)
    print()
    for j in range(len(spline_coefs[0])):
        print_fixed_s(f'{j} - {j+1}', 10)
        for coef in spline_coefs[:,j]:
            print_fixed_n(coef)
        print()


def plot_splines(spline_coefs, xj, yj):
    fig, axs = plt.subplots(figsize=(16, 9))
    x = []
    y = []
    for j in range(len(spline_coefs[0])):
        x_between_points = np.linspace(xj[j], xj[j+1], 50)
        y_between_points = calc_third_poly(spline_coefs[0,j], spline_coefs[1,j], spline_coefs[2,j], spline_coefs[3,j], x_between_points)
        x.append(x_between_points)
        y.append(y_between_points)
        axs.plot(x_between_points, y_between_points)
        axs.scatter(xj[j], yj[j])
    axs.scatter(xj[-1], yj[-1])
    axs.set_title('tj vs xj')
    axs.set_ylabel('x')
    axs.set_xlabel('t')
    plt.show()

size = 1000
xj = list(range(size))
yj = np.random.normal(loc=50, scale=10, size=size)

spline_coefs = cubicspline(xj, yj)
print_spline_coefs(spline_coefs)

plot_splines(spline_coefs, xj, yj)