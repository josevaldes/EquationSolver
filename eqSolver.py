from supportOperations import *
def evalExpr_L3(expr):
	if(expr == [] or type(expr[0]) == type([]) or type(expr[0]) == type(0)):
		return expr;
	else:
		tmp  = ''.join(expr);
		mult = 1;
		if(tmp[0] == '-'):
			mult = -1;
			tmp  = tmp[1:];
		
		if(tmp.isdigit()):
			return [[eval(tmp) * mult, '', 1]];
		elif(len(tmp) == 1 and tmp.isalpha()):
			return [[mult, tmp, 1]];
		elif(tmp[-1].isalpha()):
			return [[eval(tmp[0:len(tmp)-1]) * mult, tmp[-1], 1]];
		else:
			print tmp + " is not a valid term. Aborting";
			exit();
			
def simplify_L2(terms):
	prev      = []
	mult_flag = False;
	div_flag  = False;
	for i in xrange(len(terms)):
		if(terms[i] == '*' and not mult_flag):
			assert(i != 0);
			mult_flag = True;
		elif(terms[i] == '/' and not div_flag):
			assert(i != 0);
			div_flag = True;
		elif(type(terms[i]) == type([])):
			assert(mult_flag != div_flag or mult_flag == div_flag == False);
			if(mult_flag or div_flag):
				if(type(prev[0]) == type(terms[i][0]) == type([])):
					print "Error: Operations polynomial to polynomial is not available";
					exit();
				
				elif(type(prev[0]) == type(terms[i][0]) == type(0)):
					prev = multDivOp(prev, mult_flag, terms[i]);
				
				elif(type(prev[0]) == type([])):
					for j in xrange(len(prev)):
						prev[j] = multDivOp(prev[j], mult_flag, terms[i]);
				
				elif(type(terms[i][0]) == type([])):
					for j in xrange(len(terms[i])):
						#print terms[i][j];
						terms[i][j] = multDivOp(prev, mult_flag, terms[i][j]);
					prev = terms[i];
				
				mult_flag = False;
				div_flag  = False;
			else:
				prev = terms[i];
		else:
			print "Error: " + str(terms[i]) + " not recognized";
			assert(False);
	ans = [];
	if(type(prev[0]) == type([])):
		for elem in prev:
			if(elem[0] != 0):
				ans.append(elem);
	elif(prev[0] != 0):
		ans = prev;
			
	return ans; 

def evalExpr_L2(expr):
	terms = [];
	temps = [];
	if(expr == []):
		return expr;
	for i in xrange(len(expr)):
		if(expr[i] == '*' or expr[i] == '/'):
			terms += evalExpr_L3(temps);
			terms.append(expr[i]);
			temps = [];
		else:
			temps.append(expr[i]);
	
	terms += evalExpr_L3(temps);
	
	#print terms;
	terms  = simplify_L2(terms);
	if(terms == []):
		return terms;
	if(type(terms[0]) == type(0)):
		return [terms];
	else:
		return terms;

def simplify_L1(terms):
	variables  = {};
	minus_flag = False;
	for elem in terms:
		ite = elem;
		if(elem == '-'):
			minus_flag = True;
		elif(type(elem) == type([])):
			assert(type(elem[0]) == type(0));
			if(minus_flag):
				ite[0]    *= -1;
				minus_flag = False;
			if(ite[1] not in variables):
				variables[ite[1]] = ite;
			else:
				second      = variables[ite[1]];
				common_mult = mcm(abs(ite[2]), abs(second[2]));
				first_term  = common_mult / ite[2] * ite[0];
				second_term = common_mult / second[2] * second[0];
				variables[second[1]] = [first_term + second_term, second[1], common_mult];
	
	simplification = [];
	for elem in variables:
		simplification.append(variables[elem]);
	
	return simplification;

def evalExpr_L1(expr):
	eq = ''.join(expr.split());
	terms        = [];
	temps        = [];
	parenthesis  = "";
	open_bracket = 0;
	for i in xrange(len(eq)):
		if(open_bracket > 0):
			if(eq[i] == '('):
				open_bracket += 1;
			elif(eq[i] == ')'):
				open_bracket -= 1;
			if(open_bracket == 0):
				temps.append(evalExpr_L1(parenthesis));
				parenthesis = "";
			else:
				parenthesis += eq[i];
		elif(eq[i] == '+' or eq[i] == '-'):
			if(i > 0 and (eq[i-1] != '*' and eq[i-1] != '/')):
				terms +=(evalExpr_L2(temps));
				terms.append(eq[i]);
				temps = [];
			else:
				temps.append(eq[i]);
		elif(eq[i] == '('):
			open_bracket += 1;
			if(i > 0 and (eq[i-1].isdigit() or eq[i-1].isalpha())):
				temps.append('*');
		else:
			temps.append(eq[i]);
	terms +=(evalExpr_L2(temps));
	terms = simplify_L1(terms);
	return terms;

def eqSolver(expr):
	sides      = expr.split('=');
	left_side  = evalExpr_L1(sides[0]);
	right_side = evalExpr_L1(sides[1]);
	
	left  = [];
	right = [];
	for elem in left_side:
		if(elem[1] == 'x'):
			left.append(elem);
		else:
			tmp     = elem;
			tmp[0] *= -1;
			right.append(tmp);
	for elem in right_side:
		if(elem[1] == 'x'):
			tmp     = elem;
			tmp[0] *= -1
			left.append(tmp);
		else:
			right.append(elem);
	
	left  = simplify_L1(left);
	right = simplify_L1(right);
	
	var_x = left[0];
	if(var_x[2] != 1 or var_x[0] != 1):
		right.append('*');
		right.append([var_x[2], '', var_x[0]]);
		#print right;
		right = simplify_L2(right);
		var_x[0] = 1;
		var_x[2] = 1;
	
	result = None;
	if(type(right[0]) == type([])):
		result = right[0];
	else:
		result     = right;
	str_result = str(result[0]);
	if(result[2] > 1):
		str_result = '(' + str_result + '/' + str(result[2]) + ')';
	str_result += result[1];
	
	print "x = " + str_result;
	return result;
	
#print "Linear Equation Solver";
#myEq = raw_input("Enter the equation you want to solve ");
#eqSolver(myEq);
eqSolver("2(x - 1) + 8 = 4x - 20");

