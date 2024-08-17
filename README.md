# Amazon-Project-1
**Summary:**  
Returned_Drivers_Tracker.py (90+ lines of code) finds out what time all the drivers from a specific delivery company delivered their last package & how far away they were from one of their struggling peers who they could have potentially went to help  
The script extracts 9 different data points & exports the report to an excel for managers to review & develop action plans to improve the operations  

**Problem:**   
Amazon delivery station has many different indepedent delivery companies. Each delivery company has 30+ drivers working to deliver Amazon packages. Some drivers are fast & finish delivering their route way before their 10 hour shift. Other drivers need support from their peers to take off a few packages from their route. Every week, drivers end up returning a lot of packages due to their pace & a lot of times they are not 'rescued' by their peers who finish their job early.  

**Solution:**  
This python script opens up amazon website & filters by a specific delivery company (entered by the user).  
It then searches for the driver name who brought back most amount of packages (entered by the user). Let's call them 'Slow Driver' for the explaination below.  

Following metrics for the 'Slow Driver' are scraped & stored in PANDAS dataframe:  
RouteCode  
LastStopAddress  
LastStopTime  
Delivery App login Time   	
Planned End Time  

Next, the script loops through all of the drivers, scrapes & stores the following metrics in PANDAS dataframe:  
RouteCode  
Driver Name  
LastStopAddress        	
LastStopTime  
DistanceLastStopTo'SlowDriver'    	
TravelTimeLastStopTo'SlowDriver'    	
App login Time  
Planned End Time    

The metrics below are grabbed from GOOGLE MAPS API  
DistanceLastStopTo'SlowDriver'  
TravelTimeLastStopTo'SlowDriver'  	

Once we loop through all drivers, PANDAS dataframe is exported to an excel file



 
