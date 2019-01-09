/*********************************************
 * OPL 12.6.0.0 Model
 * Author: Sana Jabeen
 * Creation Date: Nov 8, 2018 at 7:14:48 PM
 *********************************************/
 int nServices = ...;
 int nBuses = ...;
 int nDrivers = ...;

 range S = 1..nServices;
 range B = 1..nBuses;
 range D = 1..nDrivers;
 
 // ********************************
 //           INPUT DATA
 // ********************************
 // data about services
 int start[s in S] = ...; // minutes after 0:00 (i.e. 510 is 8:30am)
 int minutes[s in S] = ...;
 int kms[s in S] = ...;
 int passengers[s in S] = ...;
 
 // data about buses
 int capacity[b in B] = ...;
 float costKm[b in B] = ...;     // in euros
 float costMinute[b in B] = ...; // in euros
 
 // data about drivers
 int maxDrivingMinutes[d in D] = ...;
 
 // IMPORTANT HINT!!!!!!!!!!
 // overlapping not input data, but should be computed in the first execute block using input data
 // overlapping[s1][s2] == 1 if and only if services s1 and s2 overlap in time
 // However, if you solve the problem without using "overlapping", you can remove the first execute block
// int overlapping[s1 in S][s2 in S];
 
 int maxBuses = ...;
 int baseMinutes = ...;
 float costBaseMinute = ...;  // in euros
 float costExtraMinute = ...; // in euros. It always holds that costExtraMinute > costBaseMinute
 
 // ********************************
 //        DECISION VARIABLES
 // ********************************

 dvar boolean ds[d in D][s in S]; // whether driver d is assigned to service s
 dvar boolean bs[b in B][s in S]; // whether bus b is assigned to service s
 dvar int+ dbase[d in D]; //duration of driver�s work for the first BM minutes or less.
 dvar int+ dextra[d in D]; //duration of extra driver�s work if dbased is greater than BM
 dvar boolean bus[b in B]; //true iff bus b is working in a service
 dvar float z;
// execute {
// for (var s1 in S)
// 	for (var s2 in S) 
// 		if (s1 < s2 && true ){ // CHANGE!!!!!!!!! true should be replaced by the corresponding expression
// 			overlapping[s1][s2] = 1; 
// 	}	
//}	
 
 // ********************************
 //        PRE PROCESSING
 // ********************************
 //int compb[b in B][s in S];
 int overlap[s1 in S][s2 in S];
 //boolean decisionBus[b in B];
 
 execute {
 //	 for (var b=1;b<=nBuses;b++)
//		for(var s=1;s<=nServices;s++)
//			if(capacity[b] >= passengers[s])
//				compb[b][s] = 1;
				
	 for (var i=1;i<=nServices;i++)
	 	for(var j=1;j<=nServices;j++)
	 		if(i != j)
	 			if((start[i] < (start[j] + minutes[j])) && (start[j] < (start[i] + minutes[i])))
	 			{
					overlap[i][j] = 1;
	 				overlap[j][i] = 1;	 				 			
	 			}

 }
 
 // ********************************
 //        OBJECTIVE FUNCTION
 // ********************************
 
 minimize z;
 		  //sum(d in D) dbase[d]*costBaseMinute+
 		  //sum(d in D) dextra[d]*costExtraMinute;
 
  
 // ********************************
 //        CONSTRAINTS
 // ********************************
 subject to {

	 	//A bus can only serve in those services for which it has enough capacity
	 	forall(b in B, s in S : passengers[s] > capacity[b])
			bs[b][s] <= 0;
			
		//Max buses		
		
	 	//All services must be serviced  
	 	forall(s in S)
	 		sum(b in B) bs[b][s] == 1;
	 	
	 	//Identify buses doing services
	 	forall(b in B)
	 	   bus[b]*nServices >= sum(s in S) bs[b][s];	 	
	 	   
	 	sum(b in B) bus[b] <= maxBuses;
		 	
	 	    
	 	//All services must be serviced	 	
	 	forall(s in S) 
	 		sum(d in D) ds[d][s] == 1;
	 	    
	 	//A driver cannot work more than maxDuration
	 	forall(d in D)
	 	  sum(s in S)
	 	    ds[d][s] * minutes[s] <= maxDrivingMinutes[d];
	 	
	 	//A driver cannot work simultaniously in two services that overlap in time
	 	forall(d in D, s1, s2 in S : overlap[s1][s2] == 1)
	 	      	ds[d][s1] + ds[d][s2] <= 1;
	 	
	 	// A bus cannot operate two services simultaniously that overlap in time.
	 	forall(b in B, s1, s2 in S : overlap[s1][s2] == 1)
	 	      bs[b][s1] + bs[b][s2] <= 1;
	 	
	 	
	 	// Finding the total cost divided in base + extra	 	  
	 	forall(d in D)
	 	   	dbase[d] + dextra[d] >= sum(s in S) ds[d][s] * minutes[s];
	 	  
	 	forall(d in D)
			dbase[d] <= baseMinutes;
	 	  
	 	//forall(d in D : maxDrivingMinutes[d] <= baseMinutes)
	 	//  dextra[d] <= 0;
	 	  
	 	//forall(d in D)
	 	  
	 	z >= sum(s in S, b in B) bs[b][s]*kms[s]*costKm[b]+
 		  sum(s in S, b in B) bs[b][s]*minutes[s]*costMinute[b]+
 		  sum(d in D) dbase[d]*costBaseMinute+
 		  sum(d in D) dextra[d]*costExtraMinute;  	
	 	  	
}  	


 execute {
 	for (var s in S) {
 		var countBuses = 0;
 		var bus; 
 		for (var b in B) if (bs[b][s] == 1) {++countBuses; bus = b;}	
 		if (countBuses == 0) writeln("ERROR: Service " + s + " has no bus!!!!!");
 		if (countBuses > 1) writeln("ERROR: Service " + s + " has more than one bus!!!!!");

 		var countDrivers = 0;
 		var driver; 
 		for (var d in D) if (ds[d][s] == 1) {++countDrivers; driver = d;}	
 		if (countDrivers == 0) writeln("ERROR: Service " + s + " has no driver!!!!!");
 		if (countDrivers > 1) writeln("ERROR: Service " + s + " has more than one driver!!!!!");
	
		writeln("Service " + s + ": bus " + bus + ", driver " + driver)			 		
 	}
 	
 	writeln("");
 	for (d in D) {
		var mins = 0;
		write("Driver " + d + " has services: ");		
		for (s in S) if (ds[d][s] == 1) {write(s + " [" + start[s] + "," + (start[s] + minutes[s]) + "] "); mins += minutes[s];}
		writeln("");
		for (var s1 in S) 
			for (var s2 in S)
				if (ds[d][s1] == 1 && ds[d][s2] == 1 && s1 < s2 && start[s1] + minutes[s1] > start[s2] && start[s1] < start[s2] + minutes[s2])
					writeln("ERROR: Services " + s1 + " and " + s2 + " overlap in time!!!!!");
		writeln("\tThat requires " + mins + " working minutes of a maximum of " + maxDrivingMinutes[d]);
		if (mins > maxDrivingMinutes[d]) writeln("ERROR: maxDrivingMinutes exceeded");				
	} 	 	
 
 	writeln("");
 	for (b in B) {
 		write("Bus " + b + " (size " + capacity[b] + ") has services: ");
 	 	for (s in S) if (bs[b][s] == 1) write(s + " [" + start[s] + "," + (start[s] + minutes[s]) + "] (pass. " + passengers[s] + "), ");
 	 	writeln("");
 	 	for (var s1 in S) 
			for (var s2 in S)
				if (bs[b][s1] == 1 && bs[b][s2] == 1 && s1 < s2 && start[s1] + minutes[s1] > start[s2] && start[s1] < start[s2] + minutes[s2])
					writeln("ERROR: Services " + s1 + " and " + s2 + " overlap in time!!!!!");
			for (s in S) if (bs[b][s] == 1 && passengers[s] > capacity[b]) 
					writeln("ERRROR: service " + s + " has " + passengers[s] + " passengers and bus " + b + " has capacity " + capacity[b]);
			 	 	
 	}
}  
 