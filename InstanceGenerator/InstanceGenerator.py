'''
AMMM Instance Generator v1.0
Instance Generator class.
Copyright 2016 Luis Velasco and Lluis Gifre.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os, random

# Generate instances based on read configuration. 
class InstanceGenerator(object):
    def __init__(self, config):
        self.config = config
    
    def generate(self):
        instancesDirectory = self.config.instancesDirectory
        fileNamePrefix = self.config.fileNamePrefix
        fileNameExtension = self.config.fileNameExtension
        numInstances = self.config.numInstances
        nBuses = self.config.nBuses
        nDrivers = self.config.nDrivers
        minCapacity = self.config.minCapacity
        maxCapacity = self.config.maxCapacity

        nServices = self.config.nServices
        minDuration = self.config.minDuration
        maxDuration = self.config.maxDuration
        minPassengers = self.config.minPassengers
        maxPassengers = self.config.maxPassengers

        if(not os.path.isdir(instancesDirectory)):
            raise Exception('Directory(%s) does not exist' % instancesDirectory)

        for i in xrange(0, numInstances):
            instancePath = os.path.join(instancesDirectory, '%s_%d.%s' % (fileNamePrefix, i, fileNameExtension))
            fInstance = open(instancePath, 'w')
           #Services
            minutes = [];
            start = [];
            kms = [];
            passengers = [];
            for service in xrange(0, nServices):
                starts = random.randint(0, 24 * 60)
                start.append(starts)
                duration = random.randint(minDuration, maxDuration)
                minutes.append(duration)
                km = random.randint(duration, duration * 2)
                kms.append(km)
                passenger = random.randint(minPassengers, maxPassengers)
                passengers.append(passenger)

            #Cost
            capacity = []
            costKm = []
            costMinute = []
            for bus in xrange(0, nBuses):
                capacities = random.randint(minCapacity, maxCapacity)
                capacity.append(capacities)
                cost_km = random.uniform(0.01, 0.2)
                costKm.append(cost_km)
                cost_min = random.uniform(0.01, 0.2)
                costMinute.append(cost_min)

            #Minutes
            maxDrivingMinutes = []
            for driver in xrange(0, nDrivers):
                maxDrivingMinute = nServices * random.randint(((minDuration + maxDuration) / 2), round(maxDuration * 1.25)) / nDrivers
                maxDrivingMinutes.append(maxDrivingMinute)
            maxBuses = nServices * random.randint(((minDuration + maxDuration) / 2), maxDuration) / 24
            baseMinutes = 200
            costBaseMinute = 0.2
            costExtraMinute = 0.3

            fInstance.write('nBuses = %d;\n' % nBuses)
            fInstance.write('nDrivers = %d;\n' % nDrivers)
            fInstance.write('nServices = %d;\n\n' % nServices)

            fInstance.write('start = [%s];\n' % (' '.join(map(str, start))))
            fInstance.write('minutes = [%s];\n' % (' '.join(map(str, minutes))))
            fInstance.write('kms = [%s];\n' % (' '.join(map(str, kms))))
            fInstance.write('passengers = [%s];\n\n' % (' '.join(map(str, passengers))))

            fInstance.write('capacity = [%s];\n' % (' '.join(map(str, capacity))))
            fInstance.write('costKm = [%s];\n' % (' '.join(map(str, costKm))))
            fInstance.write('costMinute = [%s];\n\n' % (' '.join(map(str, costMinute))))

            fInstance.write('maxDrivingMinutes = [%s];\n' % (' '.join(map(str, maxDrivingMinutes))))
            fInstance.write('maxBuses = %d;\n\n' % maxBuses)

            fInstance.write('baseMinutes = %s;\n' % str(baseMinutes))
            fInstance.write('costBaseMinute = %s;\n' % str(costBaseMinute))
            fInstance.write('costExtraMinute = %s;\n' % str(costExtraMinute))

            fInstance.close()
