from copy import copy

def mcm(first, second):
	ite   = 2;
	accum = 1;
	p1    = first;
	p2    = second;
	flag  = False;
	
	while(p1 != 1 or p2 != 1):
		if(p1 % ite == 0):
			p1  /= ite;
			flag = True;
			
		if(p2 % ite == 0):
			p2  /= ite;
			flag = True;
		
		if(flag):
			accum *= ite;
			flag   = False;
		
		else:
			ite += 1;
	
	return accum;
	
def gcd(first, second):
	ite   = 2;
	accum = 1;
	p1    = first;
	p2    = second;
	
	while(ite <= p1 and ite <= p2):
		if((p1 % ite == 0) and (p2 % ite == 0)):
			p1    /= ite;
			p2    /= ite;
			accum *= ite;
		else:
			ite += 1;
	return accum;
	
def multDivOp(left, op, right):
	ite = copy(left);
	if(op):
		ite[0] *= right[0];
		ite[1] += right[1];
		if(len(ite[1]) > 1):
			print "Error: Multiplying polynomials. Function not available";
			exit();
		ite[2] *= right[2];
	else:
		if(right[0] == 0 or right[2] == 0):
			print "Error: Dividing by zero. Aborting"
			assert(False);
			
		ite[0] *= right[2];
		ite[2] *= right[0];
		if(ite[1] == 'x' and right[1] == 'x'):
			ite[1] = '';
		elif(ite[1] == '' and right[1] == 'x'):
			print "Error: Cannot handle denominators with x";
			exit();
	#print ite;
	common_gcd = gcd(abs(ite[0]), abs(ite[2]));
	ite[0] /= common_gcd;
	ite[2] /= common_gcd;
	if(ite[2] < 0):
		ite[0] *= -1;
		ite[2] *= -1;
	return ite;