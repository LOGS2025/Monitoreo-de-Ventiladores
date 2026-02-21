# Monitoreo-de-Ventiladores

Arduino nos incoporated as of yet. The idea is to set 30min on fans and then 30min off fans. 

To ensure data is recorded in the same environment, the data recolection should only begin whenever the initial temperature is reached again after every cycle with fan on/off.

Up until now, data recolection is succesful except the library isn't capable of reaching every sensor. It is also succesfully put inside a .csv