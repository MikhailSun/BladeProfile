import sympy as sp

# (x-x0)**2+(y-y0)**2 = R**2
x, x0, y, y0, R, k, b = sp.symbols("x x0 y y0 R k b")

eq1=R**2-((x-x0)**2+(y-y0)**2)

eq2=eq1.subs(y,(k*x+b))

x_root=sp.solve(eq2,x)
# x1=(-b*k + k*y0 + x0 - sqrt(R**2*k**2 + R**2 - b**2 - 2*b*k*x0 + 2*b*y0 - k**2*x0**2 + 2*k*x0*y0 - y0**2))/(k**2 + 1),
#x2=(-b*k + k*y0 + x0 + sqrt(R**2*k**2 + R**2 - b**2 - 2*b*k*x0 + 2*b*y0 - k**2*x0**2 + 2*k*x0*y0 - y0**2))/(k**2 + 1)

print(eq2)
print(x_root)