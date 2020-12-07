from curves import regs_supress_40, regs_supress_60, regs_unmitigated 

#Define a class for projected models
class Model():
	
	def __init__(self, model, name):
		self.n_sym_d = model[0]
		self.n_hos_d = model[1] 
		self.p_cases_s = model[2]
		self.p_cases_o = model[3]
		self.p_cases_o_plus = model[4]
		self.p_cases_v = model[5]
		self.p_cases_allhosp = model[6]
		self.p_cases_allsettings = model[7]
		self.p_recovered = model[8]
		self.n_deaths = model[9]
		self.p_deaths = model[10]
		self.name = name	
			
	def __repr__(self):
		return self.name	
		
#Function to find regrestion form list of orders for a given curve	
def regress(terms,  day, scale = 1):
	t = 1
	r = 0
	for c in terms:
		r += c * t
		t *= day
	if r > 0.1:
		return r * scale
	else:
		return 0.1
		
#Create instace for each model loading its curves
supress_40 = Model(regs_supress_40, "Supress 40")
supress_60 = Model(regs_supress_60, "Supress 60")
unmitigated = Model(regs_unmitigated, "Unmitigated")

#Add model to list of models
models = [supress_40, unmitigated, supress_60]

#Uncomment for trouleshooting
#print('Imported ' + str([model.name for model in models]))

def deltas_n_hos_d(day, value):
	deltas = {}
	global models
	for model in models:
		pridiction = regress(model.n_hos_d, day)
		deltas[model] = (value/pridiction), abs(pridiction-value)/pridiction
	return deltas
	
def deltas_p_cases_allhosp(day, value):
	deltas = {}
	global models
	for model in models:
		pridiction = regress(model.p_cases_allhosp, day)
		deltas[model] = (value/pridiction), abs(pridiction-value)/pridiction
	return deltas


def deltas_p_cases_v(day, value):
	deltas = {}
	global models
	for model in models:
		pridiction = regress(model.p_cases_v, day)
		deltas[model] = (value/pridiction), abs(pridiction-value)/pridiction
	return deltas

def deltas_n_deaths(day, value):
	deltas = {}
	global models
	for model in models:
		pridiction = regress(model.n_deaths, day)
		deltas[model] = (value/pridiction), abs(pridiction-value)/pridiction
	return deltas
	
def deltas_p_deaths(day, value):
	deltas = {}
	global models
	for model in models:
		pridiction = regress(model.p_deaths, day)
		deltas[model] = (value/pridiction), abs(pridiction-value)/pridiction
	return deltas


def project(user_input):
	day = user_input[0]
	n_hos_d = user_input[1]
	p_cases_allhosp = user_input[2]
	p_cases_v = user_input[3]
	n_deaths = user_input[4]
	p_deaths = user_input[5]
		
	#finds best fit model from known data
	a = deltas_n_hos_d(day, n_hos_d)
	b = deltas_p_cases_allhosp(day, p_cases_allhosp)
	c = deltas_p_cases_v(day, p_cases_v)
	d = deltas_n_deaths(day, n_deaths)
	e = deltas_p_deaths(day, p_deaths)
	inputs = [a, b, c, d, e]
	
	
	avg_error = {}
	for model in models:
		
		avg_error[model] = ((a[model][0] + b[model][0] + c[model][0] + d[model][0] + e[model][0]) /5), ((a[model][1] + b[model][1] + c[model][1] + d[model][1] + e[model][1])/5)
	
	#Uncomment below for trouble shooting.		
	#print(avg_error)
	
	key_min = min(avg_error.keys(), key=(lambda k: avg_error[k][1]))
	
	
	#calculates unknown vales from key_min's avg_error
	n_sym_d = (regress(key_min.n_sym_d, day)) * (avg_error[key_min][0])
	p_cases_s = (regress(key_min.p_cases_s, day)) * (avg_error[key_min][0])
	p_cases_o = (regress(key_min.p_cases_o, day)) * (avg_error[key_min][0])
	p_cases_o_plus = (regress(key_min.p_cases_o_plus, day)) * (avg_error[key_min][0])
	p_cases_allsettings = (regress(key_min.p_cases_allsettings, day)) * (avg_error[key_min][0])
	p_recovered = (regress(key_min.p_recovered, day)) * (avg_error[key_min][0])
	
	return [key_min, avg_error, day, n_hos_d, p_cases_allhosp, p_cases_v, n_deaths, p_deaths, n_sym_d, p_cases_s, p_cases_o, p_cases_o_plus, p_cases_allsettings, p_recovered]

def print_statment(data):
	key_min = data[0]
	avg_error = data[1]
	day = data[2]
	n_hos_d = data[3]
	p_cases_allhosp = data[4]
	p_cases_v = data[5]
	n_deaths = data [6]
	p_deaths = data [7]
	n_sym_d = data [8]
	p_cases_s = data [9]
	p_cases_o = data[10]
	p_cases_o_plus = data[11]
	p_cases_allsettings = data[12]
	p_recovered = data[13]
	
	print( """
	
The model with the best fit is {}, with a scaling of {}. 
	
Known values are:
	
	day = {}
	n_hos_d = {}
	p_cases_allhosp = {}
	p_cases_v = {}
	n_deaths = {}
	p_deaths = {}
	
Estimated values are: 
	
	n_sym_d = {}
	p_cases_s = {}
	p_cases_o = {}
	p_cases_o_plus = {}
	p_cases_allsettings = {}
	p_recovered = {}
	""".format(key_min, avg_error[key_min][0], day, n_hos_d, p_cases_allhosp, p_cases_v, n_deaths, p_deaths, round(n_sym_d,0), round(p_cases_s,0), round(p_cases_o,0), round(p_cases_o_plus,0), round(p_cases_allsettings,0), round(p_recovered,0)))
			
#	plt.plot(range(100), [regress(key_min.p_cases_allhosp, i) for i in range(100)], label = '{} p_cases_all'.format(key_min))
#	plt.plot(range(100), [regress(key_min.p_cases_v, i) for i in range(100)], label = '{} p_cases_v'.format(key_min))
#	plt.plot(day, p_cases_allhosp, label = 'Actual p_cases_allhosp', marker='x')
#	plt.plot(day, p_cases_v, label = 'Actual p_cases_v', marker='x')
#	plt.legend()
#	plt.show()


def get_input():	
	day = float(input("what day is it? (Day 1 = 15/01/2020)  10 - 147:  "))
	
	n_hos_d = float(input("How many new C+ admissions toady?  "))
	p_cases_allhosp = float(input("How many C+ cases in hospital as at toady?  "))
	p_cases_v = float(input("How many ICU cases as at toady?  "))
	n_deaths = float(input("How many new deaths toady?  "))
	p_deaths = float(input("How many total deaths as at toady?  "))
	return [day, n_hos_d, p_cases_allhosp, p_cases_v, n_deaths, p_deaths]
	



#print_statment(project(get_input()))