#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 13:15:24 2018

@author: BleuDChan
"""
from DATParser import DATParser
import random
import operator
import numpy
import copy
import time

class Service(object):
    def __init__(self, index, start, duration, kms, reqpassengers, totalMin, totalKms):
        self.id = index
        self.driver = 0
        self.bus = 0
        self.startingTime = start
        self.durationMin = duration
        self.endTime = self.startingTime + self.durationMin
        self.durationKms = kms
        self.passengers = reqpassengers
        self.orderValue = (self.durationMin * totalMin + self.durationKms * totalKms)/(totalMin + totalKms)
    def __str__(self):
        output = '\n\nService ' + str(self.id) + '\nStart ' + str(self.startingTime) + '\nDuration ' \
        + str(self.durationMin) + '\nEnd ' + str(self.endTime) + '\nDuration Kms ' + str(self.durationKms) \
        + '\nPassengers ' + str(self.passengers) + '\nOrder Value ' + str(self.orderValue) 
        return output
    
class Bus(object):
    def __init__(self,index,maxcapacity,costperKm,costPerMin,totalMin,totalKm):
        self.id = index
        self.capacity = maxcapacity
        self.costKm = costperKm
        self.costMin = costPerMin
        self.orderValue = ((totalMin * self.costMin) + (totalKm * self.costKm))/(totalMin + totalKm)
    def __str__(self):
        output = ('\n\nBus ' + str(self.id) + '\nCapacity ' + str(self.capacity) \
              + '\nCost Km ' + str(self.costKm) + '\nCost Min ' + str(self.costMin) \
              + '\nOrder Value ' + str(self.orderValue))
        return output
        
class Driver(object):
    def __init__(self,index,maxMinutes, baseTime):
        self.id = index
        self.maxDriving = maxMinutes
        self.currentMinutes = 0
        self.availableMinutes = 0
        self.excMin = False
        self.basicTime = baseTime
    def addMinutes(self,workMinutes):
        self.currentMinutes += workMinutes
        self.availableMinutes = self.maxDriving - self.currentMinutes
        self.excMin = True if self.currentMinutes > self.basicTime else False
    def substractMinutes(self,workMinutes):
        self.currentMinutes -= workMinutes
        self.availableMinutes = self.maxDriving - self.currentMinutes
        self.excMin = True if self.currentMinutes > self.basicTime else False
    def __str__(self):
        output = '\n\nDriver ' + str(self.id) + \
        '\nCurrent Minutes ' + str(self.currentMinutes) + \
        '\nAvailable Minutes ' + str(self.availableMinutes) + \
        '\nHas exceeded Basic Time? ' + str(self.excMin)
        return output

class Solution(object):
    def __init__(self, overlaps, buses, drivers, services, baseMin, costBM, costEM, maxbuses):
        self.AssignDrivers = {}
        self.AssignBuses = {}
        self.baseMinutes =  baseMin
        self.costBaseMinute = costBM
        self.costExtraMinute = costEM
        self.overlaps = overlaps
        self.buses = buses
        self.drivers = drivers
        self.services = services
        self.maxBuses = maxbuses
        self.IsFeasible = True
        self.driverDict = {}
        self.busesDict = {}
        self.servicesDict = {}
        for i in range(len(self.drivers)):
            self.driverDict[self.drivers[i].id] = self.drivers[i]
        for j in range(len(self.buses)):
            self.busesDict[self.buses[j].id] = self.buses[j]
        for k in range(len(self.services)):
            self.servicesDict[self.services[k].id] = self.services[k]
        
    def getCurrentAssignmentsDriver(self, driverId):
        output = []
        for key,value in self.AssignDrivers.items():
            if value == driverId:
                output.append(key)
        return output
    def getCurrentAssignmentsBus(self, busId):
        output = []
        for key,value in self.AssignBuses.items():
            if value == busId:
                output.append(key)
        return output
    def getCurrentValue(self):
        costDriver = 0
        for key,value in self.AssignDrivers.items():
            driver = self.driverDict[value]
            if driver.currentMinutes > self.baseMinutes:
                costDriver += (self.baseMinutes * self.costBaseMinute + \
                               (driver.currentMinutes - self.baseMinutes) * self.costExtraMinute)
            else:
                costDriver += driver.currentMinutes * self.costBaseMinute
        costBus = 0
        for key,value in self.AssignBuses.items():
            bus = self.busesDict[value]
            service = self.servicesDict[key]
            costBus += bus.costKm * service.durationKms
            costBus += bus.costMin * service.durationMin
        return costBus + costDriver
    def getServiceById(self, serviceId):
        return self.servicesDict[serviceId]
    def getDriverById(self, driverId):
        return self.driverDict[driverId]
    def getBusById(self, busId):
        return self.busesDict[busId]
    def getCurrentValueDrivers(self):
        costDriver = 0
        for key,value in self.AssignDrivers.items():
            driver = self.drivers[value]
            if driver.currentMinutes > self.baseMinutes:
                costDriver += (self.baseMinutes * self.costBaseMinute + \
                               (driver.currentMinutes - self.baseMinutes) * self.costExtraMinute)
            else:
                costDriver += driver.currentMinutes * self.costBaseMinute
        return costDriver
    def getCurrentValueBuses(self):
        costBus = 0
        for key,value in self.AssignBuses.items():
            bus = self.buses[value]
            service = self.services[key]
            costBus += bus.costKm * service.durationKms
            costBus += bus.costMin * service.durationMin
        return costBus
    def getSortedAssignedDrivers(self):
        sortedDrivers = []
        alreadyIn = []
        ids = []
        for key,value in self.AssignDrivers.items():        
            if value not in alreadyIn:
                sortedDrivers.append(self.getDriverById(value))
                alreadyIn.append(value)
        sortedDrivers = sorted(sortedDrivers, key = operator.attrgetter('currentMinutes'), reverse = True)
        for i in range(len(sortedDrivers)):
            ids.append(sortedDrivers[i].id)
        #print('[%s]' % ', '.join(map(str, sortedDrivers)))
        return ids
    def getSortedAssignedDriversASC(self):
        sortedDrivers = []
        alreadyIn = []
        ids = []
        for key,value in self.AssignDrivers.items():        
            if value not in alreadyIn:
                sortedDrivers.append(self.getDriverById(value))
                alreadyIn.append(value)
        sortedDrivers = sorted(sortedDrivers, key = operator.attrgetter('currentMinutes'))
        for i in range(len(sortedDrivers)):
            ids.append(sortedDrivers[i].id)
        #print('[%s]' % ', '.join(map(str, sortedDrivers)))
        return ids
    def getSortedAssignedBuses(self):
        sortedBuses = []
        alreadyIn = []
        ids = []
        for key,value in self.AssignBuses.items():
            if value not in alreadyIn:
                sortedBuses.append(self.getBusById(value))
                alreadyIn.append(value)
        sortedBuses = sorted(sortedBuses, key = operator.attrgetter('orderValue'), reverse = True)
        for i in range(len(sortedBuses)):
            ids.append(sortedBuses[i].id)        
        #print('[%s]' % ', '.join(map(str, sortedBuses)))        
        return ids
    def getSortedAssignedBusesASC(self):
        sortedBuses = []
        alreadyIn = []
        ids = []
        for key,value in self.AssignBuses.items():
            if value not in alreadyIn:
                sortedBuses.append(self.getBusById(value))
                alreadyIn.append(value)
        sortedBuses = sorted(sortedBuses, key = operator.attrgetter('orderValue'))
        for i in range(len(sortedBuses)):
            ids.append(sortedBuses[i].id)        
        #print('[%s]' % ', '.join(map(str, sortedBuses)))        
        return ids
    def printSolution(self):
        print('Solution Value: ' + str(self.getCurrentValue()))
        print('Dealing with ' + str(len(self.services)) + ' services.')
        print(str(len(self.AssignDrivers)) + ' services assigned to drivers.')
        print(str(len(self.AssignBuses)) + ' services assigned to buses.')
        print('Using at most: ' + str(self.maxBuses) + ' buses.')
        print('List of Assignments')
        for key,value in self.AssignDrivers.items():
            print('For Service ' + str(key) + ' :: Driver ' + str(value) + \
                  ' Current Minutes : ' + str(self.getDriverById(value).currentMinutes) + \
                  ' and Bus ' + str(self.AssignBuses[key]))
            #print('Driver : ' + str(driver.id) + \
            #      ' - Current minutes : ' + str(driver.currentMinutes))
        overlap = "\nOverlaps: "
        for i in range(len(self.services)):
            for j in range(len(self.services)):
                if self.overlaps[i][j] == 1:
                    overlap += "\n" + str(i) + " and " + str(j) + " :: Buses: " + \
                    str(self.AssignBuses[i]) + "(" + str(self.buses[self.AssignBuses[i]].costKm) + \
                    "," + str(self.buses[self.AssignBuses[i]].costMin) + ") : "+ str(self.AssignBuses[j]) + \
                    " :: Drivers: " + str(self.AssignDrivers[i]) + " : " + \
                    str(self.AssignDrivers[j])
        #print(overlap)
        

     
class Problem(object):
    def __init__(self, pathData):
        inputData = DATParser.parse(pathData)
        self.nBuses = inputData.nBuses
        self.nDrivers = inputData.nDrivers
        self.nServices = inputData.nServices
        self.start = list(map(int,inputData.start))
        self.minutes = list(map(int,inputData.minutes))
        self.totalMinutes = sum(self.minutes)
        self.kms = list(map(int,inputData.kms))
        self.totalKms = sum(self.kms)
        self.passengers = list(map(int,inputData.passengers))
        self.capacity = list(map(int,inputData.capacity))
        self.costKm = list(map(float,inputData.costKm))
        self.costMinute = list(map(float,inputData.costMinute))
        self.maxDrivingMinutes =  list(map(int,inputData.maxDrivingMinutes))
        self.maxBuses = inputData.maxBuses
        self.baseMinutes = inputData.baseMinutes
        self.costBaseMinute = inputData.costBaseMinute
        self.costExtraMinute = inputData.costExtraMinute
        self.buses = []
        self.services = []
        self.drivers = []
        self.iterations = 0
        self.elapsedTime = 0
        self.greedyTime = 0
        self.RandomTime = 0
        self.overlaps = numpy.zeros((self.nServices, self.nServices))
        #print(self.capacity[0])
    
    def read(self):
        for i in range(self.nServices):
            newService = Service(i, self.start[i], self.minutes[i], \
                                 self.kms[i], self.passengers[i], \
                                 self.totalMinutes, self.totalKms)
            #print(newService)
            self.services.append(newService)
        for i in range(self.nBuses):
            #print(i)
            newBus = Bus(i, self.capacity[i], self.costKm[i], self.costMinute[i], self.totalMinutes, self.totalKms)
            #print(newBus)
            self.buses.append(newBus)
        
        for i in range(self.nDrivers):
            newDriver = Driver(i, self.maxDrivingMinutes[i], self.baseMinutes)
            #print(newDriver)
            self.drivers.append(newDriver)
            
        for i in range(self.nServices):
            for j in range(self.nServices):
                if (i < j):
                    if((self.services[i].startingTime < self.services[j].endTime) and \
                       (self.services[j].startingTime < self.services[i].endTime)):
                        self.overlaps[i][j] = 1
                        self.overlaps[j][i] = 1
                    
    def localSearch(self, solution, alpha):
        #drivers = solution.AssignDrivers
        #buses = solution.AssignBuses
        bestNeighbor = solution
        #bestNeighborDrivers = bestNeighbor.AssignDrivers
        #bestNeighborBuses = bestNeighbor.AssignBuses
        currentBestValue = bestNeighbor.getCurrentValue()
        #print(currentBestValue)
        keysServicesDrivers = list(bestNeighbor.AssignDrivers)
        RCLcountDrivers = int(len(bestNeighbor.AssignDrivers) * alpha)
        RCLcountBuses = int(len(bestNeighbor.AssignBuses) * alpha)
        driversFromSolution = bestNeighbor.getSortedAssignedDrivers()
        busesFromSolution = bestNeighbor.getSortedAssignedBuses()
        driversFromSolution = driversFromSolution[0:RCLcountDrivers]
        busesFromSolution = busesFromSolution[0:RCLcountBuses] 
        driversFromSolutionASC = bestNeighbor.getSortedAssignedDriversASC()
        busesFromSolutionASC = bestNeighbor.getSortedAssignedBusesASC()
        driversFromSolutionASC = driversFromSolutionASC[0:RCLcountDrivers]
        busesFromSolutionASC = busesFromSolutionASC[0:RCLcountBuses] 
        #print('[%s]' % ', '.join(map(str, busesFromSolution)))  
        #print('[%s]' % ', '.join(map(str, driversFromSolution)))
        #print(driversFromSolution)
        #print(busesFromSolution)
        #print(keysServicesDrivers)
        #print('Starting Driver Local Search: ')
        print(len(driversFromSolution))
        print(len(busesFromSolution))
        for i in range(len(bestNeighbor.AssignDrivers)):
            if bestNeighbor.AssignDrivers[i] not in driversFromSolution: continue
            for j in range(len(solution.AssignDrivers)-1,-1,-1):
                if(i >= j): continue 
                if bestNeighbor.AssignDrivers[j] not in driversFromSolutionASC: continue              
                solutionNeighbor = copy.deepcopy(solution)
                drivers = solutionNeighbor.AssignDrivers
                #print(keysServicesDrivers[i])
                service1 = solutionNeighbor.getServiceById(keysServicesDrivers[i])
                service2 = solutionNeighbor.getServiceById(keysServicesDrivers[j])
                driver1 = solutionNeighbor.getDriverById(drivers[service1.id])
                driver2 = solutionNeighbor.getDriverById(drivers[service2.id])
                possible1 = True
                possible2 = True
                currentAssignmentsDriver1 = solutionNeighbor.getCurrentAssignmentsDriver(driver1.id)
                currentAssignmentsDriver2 = solutionNeighbor.getCurrentAssignmentsDriver(driver2.id)
                for servId in currentAssignmentsDriver2:
                    if (servId == service2.id): continue
                    if self.overlaps[service1.id][servId] == 1:
                        possible2 = False
                        #print(str(i) + ',' + str(j) + ' Overlap Found ' + str(service1.id) + ' and ' + str(servId))
                        #print(self.overlaps[service1.id][servId])
                        #return None
                for servId in currentAssignmentsDriver1:
                    if (servId == service1.id): continue
                    if self.overlaps[service2.id][servId] == 1:
                        possible1 = False
                        #print(str(i) + ',' + str(j) + ' Overlap Found ' + str(service1.id) + ' and ' + str(servId))
                        #print(self.overlaps[service2.id][servId])
                if (driver1.currentMinutes + service2.durationMin - service1.durationMin) > driver1.maxDriving:
                    possible1 = False
                    #print('Drivers False Driver 1: ' + str(driver1.currentMinutes) + \
                    #      ' + ' + str(service2.durationMin) + ' = '+ str(driver1.maxDriving))
                if (driver2.currentMinutes + service1.durationMin - service2.durationMin) > driver2.maxDriving:
                    possible2 = False
                    #print('Drivers False Driver 2: ' + str(driver2.currentMinutes) + \
                    #      ' + ' + str(service1.durationMin) + ' = ' + str(driver2.maxDriving))
                if (possible1 == True and possible2 == True):
                    solutionNeighbor.AssignDrivers[service1.id] = driver2.id
                    solutionNeighbor.AssignDrivers[service2.id] = driver1.id
                    driver1.substractMinutes(service1.durationMin)
                    driver1.addMinutes(service2.durationMin)
                    driver2.substractMinutes(service2.durationMin)
                    driver2.addMinutes(service1.durationMin)
                    #print('Possible Exchange found')
                newValue = solutionNeighbor.getCurrentValue()
                
                if (currentBestValue > newValue):
                    #print('\nNew best found (Drivers): ' + str(newValue) + \
                    #      '\n Old best : ' + str(currentBestValue))
                    currentBestValue = newValue
                    bestNeighbor = solutionNeighbor
            #print(str(i+1) + ' of ' + str(len(solution.AssignDrivers)))
                #else:
                    #print('\nLocal Iteration Analysis Value (Drivers): ' + str(newValue) + \
                    #      '\nCurrent Best Value : ' + str(currentBestValue))
                    #print(solutionNeighbor.AssignDrivers)
           
        #print('Starting Bus Local Search: ')
        keysServiceBuses = list(bestNeighbor.AssignBuses)
        for i in range(len(bestNeighbor.AssignBuses)):
            if bestNeighbor.AssignBuses[i] not in busesFromSolution: continue
            for j in range(len(bestNeighbor.AssignBuses)-1,-1,-1):
                if (i >= j): continue  
                if bestNeighbor.AssignBuses[j] not in busesFromSolutionASC: continue              
                solutionNeighbor = copy.deepcopy(bestNeighbor)
                buses = solutionNeighbor.AssignBuses
                service1 = solutionNeighbor.getServiceById(keysServiceBuses[i])
                service2 = solutionNeighbor.getServiceById(keysServiceBuses[j])
                bus1 = solutionNeighbor.getBusById(buses[service1.id])
                bus2 = solutionNeighbor.getBusById(buses[service2.id])
                possible1 = True
                possible2 = True
                currentAssignmentsBus1 = solutionNeighbor.getCurrentAssignmentsBus(bus1.id)
                currentAssignmentsBus2 = solutionNeighbor.getCurrentAssignmentsBus(bus2.id)
                for servId in currentAssignmentsBus2:
                    if (servId == service2.id): continue
                    if self.overlaps[service1.id][servId] == 1:
                        possible2 = False
                        
                for servId in currentAssignmentsBus1:
                    if (servId == service1.id): continue
                    if self.overlaps[service2.id][servId] == 1:
                        possible1 = False
                        
                if (bus1.capacity < service2.passengers):
                    possible1 = False
                if (bus2.capacity < service1.passengers):
                    possible2 = False
                if (possible1 == True and possible2 == True):
                    #print('Bus Exchange Possible')
                    solutionNeighbor.AssignBuses[service1.id] = bus2.id
                    solutionNeighbor.AssignBuses[service2.id] = bus1.id
                    
                newValue = solutionNeighbor.getCurrentValue()
                #print('Current ' + str(currentBestValue) + ' :: New ' + str(newValue))
                if (currentBestValue > newValue):
                   # print('\nNew best found (Buses): ' + str(newValue) + \
                   #       '\n Old best : ' + str(currentBestValue))
                    currentBestValue = newValue
                    bestNeighbor = solutionNeighbor
            #print(str(i+1) + ' of ' + str(len(solution.AssignBuses)))
                #else:
                    #print('Local Iteration Analysis Value (Buses): ' + str(newValue) + \
                     #     '\nCurrent Best Value : ' + str(currentBestValue))
                    #print(solutionNeighbor.AssignBuses)
                    
        return bestNeighbor
                    
    def runLocalSearch(self, solution, alpha):
        if solution.IsFeasible == False:
            print('Infeasible solution found. Run program again if random generated or modify instance.')
            return None
        
        bestSolution = solution
        bestValue = solution.getCurrentValue()
        startEvalTime = time.time()
        iterations = 0
        keepIterating = True
        while(keepIterating):
            keepIterating = False
            iterations += 1
            print('\n-- Local Iteration ' + str(iterations))
            neighbor = self.localSearch(bestSolution, alpha)
            currentValue = neighbor.getCurrentValue()
            if  (bestValue > currentValue):
                print('\n New optimal found: ' + str(currentValue) + \
                      '\n Last optimal was: ' + str(bestValue))
                bestSolution = neighbor
                bestValue = currentValue
                keepIterating = True
            #else:
            #    print('\n No new Optimal found.' + \
            #          '\n Best Optimal : ' + str(bestValue))
        self.iterations += iterations
        self.elapsedTime += time.time() - startEvalTime
        print('\nBest Value: ' + str(bestSolution.getCurrentValue()))
        print('Time Spent on Local search: ' + str(self.elapsedTime) + '\n' + \
              '-----------------------------------\n')
        return bestSolution
    
    def greedy(self):
        startEvalTime = time.time()
        #drivers = copy.deepcopy(self.drivers)
        buses = copy.deepcopy(self.buses)
        services = copy.deepcopy(self.services)
        
        sortedBuses = sorted(buses, key = operator.attrgetter('orderValue'), reverse = True)
        sortedServices = sorted(services, key = operator.attrgetter('orderValue'), reverse = True)
        #print('[%s]' % ', '.join(map(str, sortedServices)))
        #New Solution
        solution = Solution(self.overlaps, self.buses, copy.deepcopy(self.drivers), self.services, \
                            self.baseMinutes, self.costBaseMinute, self.costExtraMinute, \
                            self.maxBuses)
        drivers = solution.drivers
        sortedDrivers = sorted(drivers, key = operator.attrgetter('currentMinutes'))
        #Random driver selector:
        while(len(sortedServices) > 0):
           #print(len(services))
           service = sortedServices[0]
           #service = services[randomService]
           for i in range(self.nDrivers):
               driver = sortedDrivers[i] #sortedDrivers[i]
               currentAssignments = solution.getCurrentAssignmentsDriver(driver.id)
               #if driver.id in solution.AssignDrivers:
               #    currentAssignments = solution.AssignDrivers[driver.id]
               #else:
               #    currentAssignments = []
               possible = True
               for servId in currentAssignments:
                   if self.overlaps[service.id][servId] == 1:
                       #print('overlap')
                       possible = False
               if (driver.currentMinutes + service.durationMin) > driver.maxDriving:
                   #print('current')
                   possible = False
               if (possible == True):
                   solution.AssignDrivers[service.id] = driver.id
                   driver.addMinutes(service.durationMin)
                   sortedServices.pop(0)
                   #del services[randomService]
                   sortedDrivers = sorted(sortedDrivers, key = operator.attrgetter('currentMinutes'))
                   #print('\n\nCurrent List of Drivers')
                   #print('[%s]' % ', '.join(map(str, sortedDrivers)))
                   #print('\n\nDrivers Distribution')
                   #print(solution.AssignDrivers)
                   #print(driver.currentMinutes)
                   break
               
        services = copy.deepcopy(self.services)
        sortedServices = sorted(services, key = operator.attrgetter('orderValue'), reverse = True)
        #Greedy bus selector:
        if max(self.passengers) > max(self.capacity):
            print('No Solution for max service passengers : ' + str(self.passengers) + \
                  ' and max bus capacity: ' + str(self.capacity)) 
            return None
        #print(max(self.passengers))
        #print(max(self.capacity))
        repetition = 0
        currentItem = 0
        lastItem = 0
        #Using at most maxBuses
        maxBuses = sortedBuses[0:self.maxBuses]
        #print(maxBuses[0], maxBuses[1],maxBuses[2], maxBuses[3],maxBuses[4])
        while(len(sortedServices) > 0):
            #print(len(services))
            currentItem = len(sortedServices)
            if currentItem == lastItem:
                repetition += 1
            else:
                repetition = 0
            #randomService = random.randint(0,len(services)-1)
            #service = services[randomService]
            service = sortedServices[0]
            for i in range(len(maxBuses)):
                bus = maxBuses[i]
                #bus = random.choice(maxBuses)
                currentAssignments = solution.getCurrentAssignmentsBus(bus.id)
                possible = True
                for servId in currentAssignments:
                    if self.overlaps[service.id][servId] == 1:
                       possible = False
                if (bus.capacity < service.passengers):
                    possible = False
                if (possible == True):
                   solution.AssignBuses[service.id] = bus.id
                   #driver.addMinutes(service.durationMin)
                   #del services[randomService]
                   sortedServices.pop(0)
                   maxBuses = sorted(maxBuses, key = operator.attrgetter('orderValue'), reverse = True)
                   #sortedDrivers = sorted(sortedDrivers, key = operator.attrgetter('currentMinutes'))
                   #print('\n\nCurrent List of Drivers')
                   #print('[%s]' % ', '.join(map(str, sortedDrivers)))
                   #print('\n\nBuses Distribution')
                   #print(solution.AssignBuses)
                   break
            lastItem = currentItem
            if (repetition > 100):
                solution.IsFeasible = False
                break
        greedyValue = solution.getCurrentValue()
        print('The Greedy Solution Value is: ' + str(greedyValue))
        elapsedTime = time.time() - startEvalTime
        self.greedyTime = elapsedTime
        #print('Finished Greedy Random Construction in ' + str(elapsedTime))
        return solution
    
    def constructionRandom(self):
        startEvalTime = time.time()
        #drivers = self.drivers
        buses = copy.deepcopy(self.buses)
        services = copy.deepcopy(self.services)
        #sortedDrivers = sorted(drivers, key = operator.attrgetter('currentMinutes'))
        #sortedBuses = sorted(buses, key = operator.attrgetter('orderValue'), reverse = True)
        #sortedServices = sorted(services, key = operator.attrgetter('orderValue'), reverse = True)
        #print('[%s]' % ', '.join(map(str, sortedBuses)))
        #print('[%s]' % ', '.join(map(str, sortedServices)))
        #print(self.overlaps)
        #print(self.overlaps)
        solution = Solution(self.overlaps, self.buses, copy.deepcopy(self.drivers), self.services, \
                            self.baseMinutes, self.costBaseMinute, self.costExtraMinute, \
                            self.maxBuses)
        #numItemsRCL = int(self.nDrivers * alpha)
        #print('Item RCL : ' + str(numItemsRCL))
        #sortedDrivers = sortedDrivers[0:numItemsRCL]
        #Random driver selector:
        repetition = 0
        currentItem = 0
        lastItem = 0
        
        drivers = solution.drivers
        sortedDrivers = sorted(drivers, key = operator.attrgetter('currentMinutes'))
        while(len(services) > 0):
           #print(len(services))
           currentItem = len(services)
           if currentItem == lastItem:
                repetition += 1
           else:
                repetition = 0
           randomService = random.randint(0,len(services)-1)
           service = services[randomService]
           for i in range(self.nDrivers):
               #sortedDrivers = sortedDrivers[0:numItemsRCL]
               driver = sortedDrivers[i] #random.choice(sortedDrivers) #sortedDrivers[i]
               currentAssignments = solution.getCurrentAssignmentsDriver(driver.id)
               #if driver.id in solution.AssignDrivers:
               #    currentAssignments = solution.AssignDrivers[driver.id]
               #else:
               #    currentAssignments = []
               possible = True
               for servId in currentAssignments:
                   if self.overlaps[service.id][servId] == 1:
                       possible = False
               if (driver.currentMinutes + service.durationMin) > driver.maxDriving:
                   possible = False
               if (possible == True):
                   solution.AssignDrivers[service.id] = driver.id
                   driver.addMinutes(service.durationMin)
                   del services[randomService]
                   
                   #print('\n\nCurrent List of Drivers')
                   #print('[%s]' % ', '.join(map(str, sortedDrivers)))
                   #print('\n\nDrivers Distribution')
                   #print(solution.AssignDrivers)
                   #print(driver.currentMinutes)
                   break 
               sortedDrivers = sorted(drivers, key = operator.attrgetter('currentMinutes'))
           lastItem = currentItem
           if (repetition > 100):
              solution.IsFeasible = False
              break
    
        
        services = copy.deepcopy(self.services)
        #sortedServices = sorted(services, key = operator.attrgetter('orderValue'), reverse = True)
        
        #Random bus selector:
        if max(self.passengers) > max(self.capacity):
            print('No Solution for max service passengers : ' + str(self.passengers) + \
                  ' and max bus capacity: ' + str(self.capacity)) 
            return None
        #print(max(self.passengers))
        #print(max(self.capacity))
        repetition = 0
        currentItem = 0
        lastItem = 0
        #Using at most maxBuses
        #numItemsRCL = int(len(self.buses) * alpha)
        maxBuses = []
        maxItems = self.maxBuses if len(buses) >  self.maxBuses else len(buses)
        for i in range(maxItems):
            randomBus = random.randint(0, len(buses) - 1)
            maxBuses.append(buses.pop(randomBus))
        #maxBuses = buses[0:self.maxBuses]
        #numItemsRCL = int(len(maxBuses) * alpha)
        #print(maxBuses[0], maxBuses[1],maxBuses[2], maxBuses[3],maxBuses[4])
        while(len(services) > 0):
            #print(len(services))
            currentItem = len(services)
            if currentItem == lastItem:
                repetition += 1
            else:
                repetition = 0
            randomService = random.randint(0,len(services)-1)
            service = services[randomService]
            for i in range(len(maxBuses)):
                bus = maxBuses[i]
                #bus = random.choice(maxBuses)
                currentAssignments = solution.getCurrentAssignmentsBus(bus.id)
                possible = True
                for servId in currentAssignments:
                    if self.overlaps[service.id][servId] == 1:
                       possible = False
                if (bus.capacity < service.passengers):
                    possible = False
                if (possible == True):
                   solution.AssignBuses[service.id] = bus.id
                   #driver.addMinutes(service.durationMin)
                   del services[randomService]
                   #sortedBuses = sorted(buses, key = operator.attrgetter('orderValue'), reverse = True)
                   #sortedDrivers = sorted(sortedDrivers, key = operator.attrgetter('currentMinutes'))
                   #print('\n\nCurrent List of Drivers')
                   #print('[%s]' % ', '.join(map(str, sortedDrivers)))
                   #print('\n\nBuses Distribution')
                   #print(solution.AssignBuses)
                   break
            #maxBuses = sorted(maxBuses, key = operator.attrgetter('orderValue'), reverse = True)
            lastItem = currentItem
            if (repetition > 100):
                solution.IsFeasible = False
                break
            
        greedyValue = solution.getCurrentValue()
        print('The Greedy Random Solution Value is: ' + str(greedyValue))
        elapsedTime = time.time() - startEvalTime
        self.RandomTime = elapsedTime
        #print('Finished Greedy Random Construction in ' + str(elapsedTime))
        return solution, elapsedTime
        
    
    def GraspSolver(self, maxTime, alpha):  
        startingTime = time.time()
        bestGSolution = None
        bestValue = float('inf')
        startingTime = time.time()
        totalElapsedTime = 0
        #totalEvaluatedCandidates = 0
        iteration = 0
        maxExecTime = maxTime
        while(time.time() - startingTime < maxExecTime):
            print('Grasp Time: ' + str(time.time() - startingTime) + ' Current Value ' + \
                  str(bestValue))
            iteration += 1
            solutionForGrasp, it_ElapsedTime = self.constructionRandom()
            #print('Greedy in Grasp')
            totalElapsedTime += it_ElapsedTime
            if(solutionForGrasp.IsFeasible == False): 
                print('Infeasible found')
                continue
            solutionForGrasp = self.runLocalSearch(solutionForGrasp, alpha)
            solutionBestValue = solutionForGrasp.getCurrentValue()
            if (solutionBestValue < bestValue):
                bestGSolution = solutionForGrasp
                bestValue = solutionBestValue
                #print(' New Best Found : ' + str(bestValue))
                
        avgTimePerIteration = 0.0
        if(iteration > 0):
            avgTimePerIteration = totalElapsedTime / float(iteration)
        
        totalElapsedTime = time.time() - startingTime
        print('')
        print('GRASP Candidate Evaluation Performance: ')
        print(' Num. Iterations ' + str(iteration))
        print(' Avg. Time per Iteration ' + str(avgTimePerIteration) + ' ')
        print(' Total Time Spent ' + str(totalElapsedTime) + ' ')
        return bestGSolution
        
        
        
class Experiment(object):
    def __init__(self, source):
        self.sourceFile = source
        self.problem = Problem(source)
        self.problem.read()
    def GreedyPlusLocal(self, alpha):
        greedySolution = self.problem.greedy()
        solution = self.problem.runLocalSearch(greedySolution, alpha)
        solution.printSolution()
        print('Total time spent on Experiment: ' + str(self.problem.greedyTime + self.problem.elapsedTime))
    def GRASP(self,seconds, alpha):
        solution = self.problem.GraspSolver(seconds, alpha)
        solution.printSolution()
        

#GREEDY + LOCAL SEARCH
experiment = Experiment('examen.dat')
#experiment.GreedyPlusLocal(0.04)

#GRASP
experiment.GRASP(1800.0, 1)




        


        
    
        
        
        