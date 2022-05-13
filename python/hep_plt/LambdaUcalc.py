def L(du, y):
	return (1/y)**(1/(du-1))

def xsec(du, LU):
	return (1/LU)**(2*(du-1))

def xsecRatio(du, LU1, LU2):
	return xsec(du, LU1)/xsec(du, LU2)

