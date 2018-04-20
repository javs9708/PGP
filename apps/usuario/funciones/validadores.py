import re
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, time, timedelta

LIMITE = (date.today() - relativedelta(years=100))

patron_nombre_apellido = re.compile('([A-ZÁÉÍÓÚ a-zñáéíóú]{1}[a-zñáéíóú A-ZÁÉÍÓÚ ]+[\s]*)+$')
patron_cc = re.compile('[\d]{10}$')
patron_password = re.compile('[\d][0-9]{8,}$')
#patron_email = re.compile('[\w]+@{1}[\w]+(\.[\w]+)*\.[a-z]{2,3}$')

def validar_nombre(nombre):
	if re.match(patron_nombre_apellido,nombre) is None:
		return True
	else:
		return False

def validar_apellido(apellido):
	if re.match(patron_nombre_apellido,apellido) is None:
		return True
	else:
		return False

def validar_cc(cc):
	if re.match(patron_cc,cc) is None:
		return True
	else:
		return False

def validar_password(password):
	if re.match(patron_password,password) is None:
		return True
	else:
		return False

def validar_fecha(fecha):
	fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
	if (fecha + relativedelta(years=18) > date.today()) or (fecha < LIMITE):
		return True
	else:
		return False

"""def validar_email(email):
	if re.match(patron_email,email) is None:
		return True
	else:
		return False
"""