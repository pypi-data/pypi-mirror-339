variable - v


function - f


staticmethod - sm


classmethod - cm


class - s


object - o


Precision -

1. (v) __DecimalPrecision: variable used for precision


2. (f) setpr(__p): changes the precision
			__pr: the new precision, changes __DecimalPrecision


3. (f) getpr(): get the precision


Note - Precision is integer


Constant - 


1. (v) __Pi: variable that stores the value of pi


2. (v) __EulersNumber: variable that stores the value of e


3. (c) constant: get values of constants


4. (sm) e(pr): get value of e (in constant)

   pr: the precision, not more than 100


5. (sm) pi(pr): get value of pi (in constant)

   pr: the precision, not more than 100


Random -


1. (f) rint(__i, __j, __n, s): generate a random integer
	
   __i: minimum integer
	
   __j: maximum integer
	
   __n: number of numbers
	
   s: seed (positive integer


2. (o) rdeciml(__a, __b, __pr): generate a random decimal
	
   __a,__b: range extremities
	
   __pr: precision


3. (f) random(__n, __s): generate random numbers (in rdeciml)
	
   __n: number of random numbers to generate
	
   __s: seed for generating random numbers if wanted


4. (f) cgpr(__pr): change precision for random numbers (in rdeciml) 
			

Decimal Function -


1. (f) deciml(__a, __pr): return a Decimal object

   __a: number to convert to Decimal object
	
   __pr: desired precision


Arithmatic Operations -


1. (c) algbra: primitive arithmatic operations


2. (sm): add: add given numbers (in algbra)

   *__a: arbitrary number of numbers
	
   pr: desired precision


3. (sm): sub: subtract given numbers (in algbra)

   *__a: arbitrary number of numbers
	
   pr: desired precision


4. (sm): mul: multiply given numbers (in algbra)

   *__a: arbitrary number of numbers
	
   pr: desired precision


5. (sm): div: divide given numbers (in algbra)

   __a: numerator of division
	
   __b: denominator of division
	
   __pr: desired precision


6. (cm): log: logarithmic given numbers (in algbra)

   __a: number to operate
	
   __b: base of the log
	
   __pr: desired precision


7. (cm): pwr: exponent from given numbers (in algbra)

   __a: number to operate
	
   __b: power
	
   __pr: desired precision


8. (c) galgbra: arithmatic operations using lists
