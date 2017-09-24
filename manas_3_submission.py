#!/bin/python

import sys

if __name__ == "__main__":
    THRESHOLD = 1
    pedestrian_filter = [[1, 1], 
                         [1, 1]]
    car_filter = [[1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1], 
                  [1, 1, 1, 1, 1]]
    bike_filter = [[1, 1, 1],
                   [1, 1, 1], 
                   [1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]]
    c1, c2, c3 = raw_input().strip().split(' ')
    c1, c2, c3 = [int(c1), int(c2), int(c3)]
    road = []
    for road_i in xrange(36):
        road_temp = map(int,raw_input().strip().split(' '))
        road.append(road_temp)
    lane = road[:]
    for i,row in enumerate(lane):
        for j,el in enumerate(row):
            if(lane[i][j]==0):
                lane[i][j]=1
            else:
                lane[i][j]=0
    cars= [0,0]
    bikes =[0,0]
    pedestrians = [0,0]
    def cost(obstacles, costs):
        total_cost = 0
        total_cost = total_cost + obstacles[0]*costs[0]
        total_cost = total_cost + obstacles[1]*costs[1]
        total_cost = total_cost + obstacles[2]*costs[2]
        return total_cost
    #Operations on Matrices 
    def sum(arr):
        total  = 0
        for row in arr:
            for el in row:
                total+=el
        return total
    def multiply(arr1, arr2):
        arr3 = []
        for i,row1 in enumerate(arr1):
            rowmul = []
            for j,el1 in enumerate(row1):
                rowmul.append(el1*(arr2[i][j]))
            arr3.append(rowmul)
        return arr3
    
    #Find Cars 
    def filter_car(lane):
        global cars
        width = 5
        for i in range(len(lane)-7+1):
            for j in range(len(lane[0])-5+1):
                #sub_array = lane[i:i+7, j:j+5]
                sub_array = []
                for p in range(7):
                    sub_array.append(lane[i+p][j:j+5])
                out = sum(multiply(sub_array,car_filter))
                #print out , 'car TOTAL'
                out = float(out)/35
                if out>=THRESHOLD:
                    #print 'bike:', j
                    if j>6-width and j<6:
                        #MIDDLE
                        cars[0]+=1
                        cars[1]+=1
                    elif j<6:
                        #LEFT
                        cars[0]+=1
                    else:
                        #RIGHT
                        cars[1]+=1
                    for p in range(7):
                        for q in range(5):
                            lane[i+p][j+q] = 0
        return lane
    
    #Method to find bikes
    def filter_bike(lane):
        global bikes
        width = 3
        for i in range(len(lane)-6+1):
            for j in range(len(lane[0])-3+1):
                #sub_array = lane[i:i+6,j:j+3]
                sub_array = []
                for p in range(6):
                    sub_array.append(lane[i+p][j:j+3])
                #print sub_array
                out = sum(multiply(sub_array,bike_filter))
                #print out , 'bike TOTAL'
                out = float(out)/18
                if out>=THRESHOLD:
                    #print 'bike:', j
                    if j>6-width and j<6:
                        #MIDDLE
                        bikes[0]+=1
                        bikes[1]+=1
                    elif j<6:
                        #LEFT
                        bikes[0]+=1
                    else:
                        #RIGHT
                        bikes[1]+=1
                    for p in range(6):
                        for q in range(3):
                            lane[i+p][j+q] = 0
                    #lane[i:i+6, j:j+3] = np.zeros((6,3))
        return lane
    
    #Find Pedestrians 
    def filter_pedestrians(lane):
        global pedestrians
        width = 2
        for i in range(len(lane)-2+1):
            for j in range(len(lane[0])-2+1):
                #sub_array =lane[i:i+2,j:j+2]
                sub_array = []
                for p in range(2):
                    sub_array.append(lane[i+p][j:j+2])
                #print sub_array
                out = sum(multiply(sub_array,pedestrian_filter))
                #print out , 'TOTAL'
                out =float(out)/4
                #print out
                
                if out>=THRESHOLD*0.75:
                    #print 'ped:', j
                    if j>6-width and j<6:
                        #MIDDLE
                        pedestrians[0]+=1
                        pedestrians[1]+=1
                    elif j<6:
                        #LEFT
                        pedestrians[0]+=1
                    else:
                        #RIGHT
                        pedestrians[1]+=1
                    #lane[i:i+2, j:j+2] = np.zeros(sub_array.shape)
                    for p in range(2):
                        for q in range(2):
                            lane[i+p][j+q] = 0
        return lane
    lane = filter_car(lane)
    lane = filter_bike(lane)
    lane = filter_pedestrians(lane)
    cost0 = cost((pedestrians[0], bikes[0], cars[0]), (c1, c2, c3))
    cost1 = cost((pedestrians[1], bikes[1], cars[1]), (c1, c2, c3))
    if(cost0>cost1):
        print cost1
    else:
        print cost0
    