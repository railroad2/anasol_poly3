nerror = 0
npos = 0
nzero = 0
nneg = 0
nother = 0
ntotal = 0

flag_cout = False

def check_sol(a, b, c, d, xp):
    ps = [a*xp**3, b*xp**2, c*xp, d]
    ps2 = [abs(i) for i in ps]
    tol = max([1e-8 * sum(ps2) *1000 , 1e-8])
    zero = abs(sum(ps))
    #print (zero)
    if abs(zero) < tol or abs(zero) == 0:
        return 0
    else:
        global nerror
        nerror += 1
        print (ps2)
        print (tol)
        print ("zero = ", abs(zero))
        return -1

def print_eqn(a, b, c, d):
    if not flag_cout: return

    print ("-"*50)
    eqn = ""
    eqn += f" {a} x^3" if a else ""
    eqn += f" {b:+} x^2" if b else ""
    eqn += f" {c:+} x" if c else ""
    eqn += f" {d:+}" if d else ""
    eqn += " = 0"
    print (eqn)
    print ("-"*50)

def print_sol(x):
    if not flag_cout: return
    tol = 1e-8
    sol = ""
    sol += f"{x.real:+.8}" if (x.real)**2 > tol**2 else ""
    sol += f"{x.imag:+.8}j" if (x.imag)**2 > tol**2 else ""
    if sol == "":
        sol += "0"
    print ("x=")
    print (sol)

def solve_poly1(a, b):
    if a == 0:
        return 0
    print_eqn(0, 0, a, b)
    tmp = -b/a
    print_sol(tmp)
    return tmp 

def solve_poly2(a, b, c):
    if a == 0:
        return solve_poly1(b, c)

    print_eqn(0, a, b, c)

    x = []
    D = b**2 - 4*a*c
    x.append(-b/2/a + D**0.5/2/a)  
    print_sol(x[-1])
    x.append(-b/2/a - D**0.5/2/a)  
    print_sol(x[-1])
    return x

def solve_poly3(a, b, c, d):
    ## analytically find roots for a polynomial 
    ## ax^3 + bx^2 + cx + d = 0
    global npos, nzero, nneg, nother, ntotal
    ntotal += 1
    if a == 0:
        nother += 1
        return solve_poly2(b, c, d)

    p = c/a - b**2/3./a**2
    q = d/a - b*c/3./a**2 + 2/27.*b**3/a**3

    print_eqn(a, b, c, d)

    D = (q/2.)**2 + (p/3.)**3
    Dstr = "D={D}"

    if D > 0:
        Dstr += " > 0"
        npos += 1
    elif D == 0:
        Dstr += " = 0"
        nzero += 1
    elif D < 0:
        Dstr += " < 0"
        nneg += 1
    else:
        raise

    if flag_cout: print (Dstr)

    p += 0j
    q += 0j
    m3 = (-q/2. + ((q/2.)**2 + (p/3.)**3)**0.5)#**(1/3.)
    n3 = (-q/2. - ((q/2.)**2 + (p/3.)**3)**0.5)#**(1/3.)

    if D > 0:
        m = abs(m3) ** (1/3)
        n = abs(n3) ** (1/3)
        if m3.real < 0:
            m *= -1
        if n3.real < 0:
            n *= -1
    else:
        m = m3**(1/3.)
        n = n3**(1/3.)

    #print (f"p={p}")
    #print (f"q={q}")
    #print (f"m^3={m3}")
    #print (f"n^3={n3}")
    #print (f"m={m}")
    #print (f"n={n}")

    w = 0.5*(-1+(3**0.5)*1j)


    tol = 1e-9

    x = []
    for k in range(3):
        tmp = w**k * m + w**(3.-k) * n - b/3./a
        #print (w**k, w**(3.-k))
        x.append(tmp)
        print_sol(tmp)
        print(f"\t(incorrect)\n" if check_sol(a, b, c, d, tmp) else "", end="")

    return x


if __name__=="__main__":
    #x = solve_poly3(1, 0, 0, -1)

    #x = solve_poly3(1, 0, -15, -4)

    #x = solve_poly3(1, 2, 3, 4)

    import numpy as np
    for i in range(1000000):
        #coe = [np.random.uniform(-1, 1) * i for j in range(4)]
        #solve_poly3(*coe)
        coe = [np.random.randint(-1000, 1000) for j in range(4)]
        solve_poly3(*coe)

    print (f"nerror = {nerror:10d}")
    print (f"npos   = {npos:10d}")
    print (f"nzero  = {nzero:10d}")
    print (f"nneg   = {nneg:10d}")
    print (f"nother = {nother:10d}")
    print (f"ntotal = {ntotal:10d}")

