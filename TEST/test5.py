import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAFwjZrvIHWVmXPeXajRTRYGFk4d2Saz4I')

#short form of address, such as country + postal code
geocode_result = gmaps.geocode('singapore 018956')

#full address
geocode_result = gmaps.geocode("10 Bayfront Ave, Singapore 018956")

#a place name
geocode_result = gmaps.geocode("zhongshan park")

#Chinese characters
geocode_result = gmaps.geocode('滨海湾花园')

#place name/restaurant name
geocode_result = gmaps.geocode('jumbo seafood east coast')

print(geocode_result[0]["formatted_address"]) 
print(geocode_result[0]["geometry"]["location"]["lat"]) 
print(geocode_result[0]["geometry"]["location"]["lng"])