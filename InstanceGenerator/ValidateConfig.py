'''
AMMM Instance Generator v1.0
Config attributes validator.
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

# Validate config attributes read from a DAT file. 
class ValidateConfig(object):
    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        for paramName in ['instancesDirectory', 'fileNamePrefix', 'fileNameExtension', 'numInstances', 
                            'nDrivers', 'nBuses', 'minCapacity', 'maxCapacity', 'nServices', 'minDuration', 'maxDuration', 'minPassengers', 'maxPassengers']:
            if(not data.__dict__.has_key(paramName)):
                raise Exception('Parameter(%s) not contained in Configuration' % str(paramName))
        
        instancesDirectory = data.instancesDirectory
        if(len(instancesDirectory) == 0): raise Exception('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if(len(fileNamePrefix) == 0): raise Exception('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if(len(fileNameExtension) == 0): raise Exception('Value for fileNameExtension is empty')

        numInstances = data.numInstances
        if(not isinstance(numInstances, (int, long)) or (numInstances <= 0)):
            raise Exception('numInstances(%s) has to be a positive integer value.' % str(numInstances))

        nDrivers = data.nDrivers
        if(not isinstance(nDrivers, (int, long)) or (nDrivers <= 0)):
            raise Exception('nDrivers(%s) has to be a positive integer value.' % str(nDrivers))

        nBuses = data.nBuses
        if(not isinstance(nBuses, (int, long)) or (nBuses <= 0)):
            raise Exception('nBuses(%s) has to be a positive integer value.' % str(nBuses))

        minCapacity = data.minCapacity
        if(not isinstance(minCapacity, (int, long)) or (minCapacity <= 0)):
            raise Exception('minCapacity(%s) has to be a positive integer value.' % str(minCapacity))

        maxCapacity = data.maxCapacity
        if(not isinstance(maxCapacity, (int, long)) or (maxCapacity <= 0)):
            raise Exception('maxCapacity(%s) has to be a positive integer value.' % str(maxCapacity))

        nServices = data.nServices
        if(not isinstance(nServices, (int, long)) or (nServices <= 0)):
            raise Exception('nServices(%s) has to be a positive integer value.' % str(nServices))

        minDuration = data.minDuration
        if(not isinstance(minDuration, (int, long)) or (minDuration <= 0)):
            raise Exception('minDuration(%s) has to be a positive integer value.' % str(minDuration))

        minPassengers = data.minPassengers
        if(not isinstance(minPassengers, (int, long)) or (minPassengers <= 0)):
            raise Exception('minPassengers(%s) has to be a positive integer value.' % str(minPassengers))

        maxPassengers = data.maxPassengers
        if(not isinstance(maxPassengers, (int, long)) or (maxPassengers <= 0)):
            raise Exception('maxPassengers(%s) has to be a positive integer value.' % str(maxPassengers))
