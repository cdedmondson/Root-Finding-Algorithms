import math
import sys


def secant(f, a, b, maxIter, epsilon):
    fa = f(a)
    fb = f(b)

    for iteration in range(maxIter):

        if abs(fa) > abs(fb):
            temp = a
            a = b
            b = temp
            temp = fa
            fa = fb
            fb = temp

        d = (b - a) / (fb - fa)
        b = a
        fb = fa
        d = d * fa

        if abs(d) < epsilon:
            print(f"Algorithm has converged after {iteration} iterations!")
            return a

        a = a - d
        fa = f(a)

    print("Maximum number of iterations reached!")
    return a


def newton(f, derF, x, maxIter, epsilon, delta):
    fx = f(x)

    for iterator in range(maxIter):
        fd = derF(x)

        if abs(fd) < delta:
            print("Small slope!")
            return x

        d = fx / fd
        x = x - d
        fx = f(x)

        if abs(d) < epsilon:
            print(f"Algorithm has converged after {iterator} iterations!")
            return x

    print("Max iterations reached without convergence...")
    return x


def bisection(f, a, b, maxIter, epsilon):
    fa = f(a)
    fb = f(b)

    if fa * fb >= 0:
        print("Inadequate values for a and b.")
        return -1
    error = b - a
    for iteration in range(maxIter):
        error = error / 2
        c = a + error
        fc = f(c)

        if abs(error) < epsilon or fc == 0:
            print(f"Algorithm has converged after {iteration} iterations!")
            return c

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    print("Max iterations reached without convergence....")
    return c


def hybrid(f, derF, a, b, maxIter, epsilon):
    fa = f(a)
    fb = f(b)

    if fa * fb >= 0:
        print("Inadequate values for a and b.")
        return -1
    error = b - a
    for iteration in range(maxIter):
        error = error / 2
        c = a + error
        fc = f(c)

        if abs(error) < epsilon or fc == 0:
            print(f"Algorithm has converged after {iteration} iterations!")
            return c

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

        x = fc - (f(c) / derF(c))
        if abs(f(x)) < epsilon:
            return c

        c = x

    print("Max iterations reached without convergence....")
    return c


def read_input_data(inputfile):
    with open(inputfile, 'r') as file:
        contents = file.read()
    degree, c3, c2, c1, c = [int(num) for num in contents.split()]
    return degree, c3, c2, c1, c


def functions(degree, coeff3, coeff2, coeff1, constant, selection):
    if selection == "-newt":
        if degree == 3:
            if coeff2 == 0 and coeff1 != 0 and constant != 0:
                fn = lambda x: coeff3 * x ** 3 + coeff1 * x + constant
                derF = lambda x: coeff3 * (degree - 1) * x ** 2 + coeff1
                return fn, derF
            elif constant == 0 and coeff2 == 0:
                fn = lambda x: coeff3 * x ** 3 + coeff1 * math.sin(x)
                derF = lambda x: coeff3 * (degree - 1) * x ** 2 + coeff1 * math.cos(x)
                return fn, derF
            else:
                fn = lambda x: coeff3 * x ** 3 + coeff2 * x ** 2 + coeff1 * x + constant
                derF = lambda x: 3 * coeff3 * x ** (degree - 1) + 2 * coeff2 * x + coeff1
                return fn, derF
        if degree == 1:
            fn = lambda x: coeff1 * x + 10 - coeff1 * x * math.cosh(50 / x)
            derF = lambda x: (50 * math.sinh(50 / x)) / x - (math.cosh(50 / x) + 1)
            return fn, derF

    elif degree == 3:
        if coeff2 == 0 and coeff1 != 0 and constant != 0:
            fn = lambda x: coeff3 * x ** 3 + coeff1 * x + constant
            return fn
        elif constant == 0 and coeff2 == 0:
            fn = lambda x: coeff3 * x ** 3 + coeff1 * math.sin(x)
            return fn
        else:
            fn = lambda x: coeff3 * x ** 3 + coeff2 * x ** 2 + coeff1 * x + constant
            return fn

    if degree == 1:
        fn = lambda x: coeff1 * x + 10 - coeff1 * x * math.cosh(50 / x)
        return fn


def main():
    maxIter = 10000

    option = str(sys.argv[1])

    if option == "-newt":
        x = int(sys.argv[2])
        inputfile = sys.argv[3]
        degree, coeff3, coeff2, coeff1, constant = read_input_data(inputfile)
        fn, derF = functions(degree, coeff3, coeff2, coeff1, constant, "-newt")
        answer = newton(fn, derF, x, maxIter, 1e-10, 20)
        print(answer)
    elif option == "-sec":
        option2 = str(sys.argv[2])
        if option2 == "-maxIter":
            maxIter = int(sys.argv[3])
            a = float(sys.argv[4])
            b = float(sys.argv[5])
            inputfile = str(sys.argv[6])
            degree, coeff3, coeff2, coeff1, constant = read_input_data(inputfile)
            fn = functions(degree, coeff3, coeff2, coeff1, constant, "-sec")
            answer = secant(fn, a, b, maxIter, 1e-10)
            print(answer)
        else:
            a = float(sys.argv[2])
            b = float(sys.argv[3])
            inputfile = str(sys.argv[4])
            degree, coeff3, coeff2, coeff1, constant = read_input_data(inputfile)
            fn = functions(degree, coeff3, coeff2, coeff1, constant, "-sec")
            answer = secant(fn, a, b, maxIter, 1e-10)
            print(answer)
    elif option == "-hybrid":
        if str(sys.argv[2]) == "-maxIter":
            maxIter = int(sys.argv[3])
            a = float(sys.argv[4])
            b = float(sys.argv[5])
            inputfile = str(sys.argv[6])
            degree, coeff3, coeff2, coeff1, constant = read_input_data(inputfile)
            fn, derF = functions(degree, coeff3, coeff2, coeff1, constant, "-newt")
            answer = hybrid(fn, derF, a, b, maxIter, 1e-10)
            print(answer)
        else:
            a = float(sys.argv[2])
            b = float(sys.argv[3])
            inputfile = str(sys.argv[4])
            degree, coeff3, coeff2, coeff1, constant = read_input_data(inputfile)
            fn, derF = functions(degree, coeff3, coeff2, coeff1, constant, "-newt")
            answer = hybrid(fn, derF, a, b, maxIter, 1e-10)
            print(answer)
    else:
        if option == "-maxIter":
            maxIter = int(sys.argv[2])
            a = float(sys.argv[3])
            b = float(sys.argv[4])
            inputfile = str(sys.argv[5])
            degree, coeff3, coeff2, coeff1, constant = read_input_data(inputfile)
            fn = functions(degree, coeff3, coeff2, coeff1, constant, "-bisec")
            answer = bisection(fn, a, b, maxIter, 1e-10)
            print(answer)
        else:
            a = float(sys.argv[1])
            b = float(sys.argv[2])
            inputfile = str(sys.argv[3])
            degree, coeff3, coeff2, coeff1, constant = read_input_data(inputfile)
            fn = functions(degree, coeff3, coeff2, coeff1, constant, "-bisec")
            answer = bisection(fn, a, b, maxIter, 1e-10)
            print(answer)


if __name__ == '__main__':
    main()
