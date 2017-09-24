from __future__ import print_function
import sys
n = int(raw_input())
customers = []
for i in range(n):
    customer_temp = map(int, raw_input().strip().split(" "))
    customer = [i]+[customer_temp[0]]+[(customer_temp[1], customer_temp[2]), (customer_temp[3], customer_temp[4])]
    customers.append(customer)
    #print( customer, end ='')
cx, cy = (0, 0)
cur_time = 0
serviced = []
def sign(x):
	if(x<0):
		return -1
	elif(x>0):
		return 1
	else:
		return 0
def mod(x):
	return sign(x)*x
def pp():
	global cx, cy
	print((cx, cy))
#(0		1	 	   2			   3      )
#(ID, TIME, (PickX, PickY) ,(DropX ,DropY))
def move_to(pt1, pt2):
	global cx, cy, cur_time
	dy = pt2[0]-pt1[0]	
	dx = pt2[1]-pt1[1]
	#print( mod(dx), end ='')
	if dx==0 and dy==0:
		print( '0', end ='')
		#pp()
		cur_time += 1
		return
	for i in range(mod(dx)):
		cy += sign(dx)
		if sign(dx)==-1:
			#LEFT
			print( '4', end ='')
			#pp()
		else:
			#RIGHT
			print( '2', end ='')
			#pp()
		cur_time += 1				
	for i in range(mod(dy)):
		cx += sign(dy)
		if sign(dy)==-1:
			#UP
			print( '1', end ='')
			#pp()
		else:
			#DOWN
			print( '3', end ='')
			#pp()
		cur_time += 1
def man_dist(pt1, pt2):
	dy = pt2[0]-pt1[0]
	dx = pt2[1]-pt1[1]
	return mod(dx) + mod(dy)
def l2_dist(pt1, pt2):
	dy = pt2[0]-pt1[0]
	dx = pt2[1]-pt1[1]
	return float((dy**2)+(dx**2)) **(0.5)
def is_servicable(customer):
	global cur_time
	global cx, cy
	pickup_time =  man_dist((cx, cy), customer[2])
	req_time = customer[1]
	if (cur_time+pickup_time) > req_time:
		return True
	else:
		return False

def pick_best(customers):
	global cx, cy
	global cur_time
	max_fare = -20
	max_id = -1
	max_customer = customers[0]
	for customer in customers:
		pickup_dist = man_dist((cx, cy), customer[2])
		drop_dist = l2_dist(customer[2], customer[3])
		req_time = customer[1]
		potential_fare = drop_dist/(cur_time + pickup_dist - req_time)
		if potential_fare > max_fare: 
			max_fare = potential_fare
			max_id = customer[0]
			max_customer = customer
	return customer
def get_servicable(customers):
	servicable_customers = []
	for customer in customers:
		if(is_servicable(customer)):
			servicable_customers.append(customer)
	return servicable_customers

def get_remaining_customers(customers):
	global serviced
	remaining_customers = []
	for customer in customers:
		if(customer[0] not in serviced):
			remaining_customers.append(customer)
	return remaining_customers

def get_closest_customer(customers):
	closest_customer = customers[0]
	least_dist = man_dist((cx, cy), customer[2])
	for customers in customer:
		dist_to_customer = man_dist((cx, cy), customer[2])
		if dist_to_customer < least_dist:
			closest_customer = customer
	return closest_customer

while(len(get_remaining_customers(customers)) != 0):
	remaining_customers = get_remaining_customers(customers)
	# print('Remaining - ', remaining_customers)
	# print('Servicable - ',get_servicable(remaining_customers))
	# print('Current Pos- ', (cx, cy))
	if(len(get_servicable(remaining_customers))==0):
		next_customer = get_closest_customer(remaining_customers)
		pickup = next_customer[2]
		drop = next_customer[3]
		move_to((cx, cy), pickup)
	else:
		next_customer = pick_best(get_servicable(remaining_customers))
		pickup = next_customer[2]
		drop = next_customer[3]
		move_to((cx, cy), pickup)
		move_to(pickup, drop)
		serviced.append(next_customer[0])