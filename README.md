# BlackHoleGalaxyPredictor
A Program which analyzes the radial light profiles of galaxy's and predicts if the galaxy has a black hole or not

# Collecting Data
Using a subset of the Hubble Space TeleScope Catalog, the Sloan Digital SkyServer, I requested for Galaxy's with an apparent brighteness greater than 22. Galaxy's are ranked from 0 to ~30 on a logrhythmic scale. As Galaxy's as far dimmer than stars in these pictures, very bright Galaxy's and very dim Galaxy's indicate difficulty in classification.

The query used to retrieve 500k Galaxy's locations:
(http://skyserver.sdss.org/dr16/en/tools/search/sql.aspx?cmd=+SELECT+TOP+1000+objID+%0d%0a+FROM+Galaxy+%0d%0a+WHERE+%0d%0a+(r+-+extinction_r)+%3c+22+%0d%0a)

```SQL
 SELECT objID, ra, dec
 FROM Galaxy 
 WHERE 
 (r - extinction_r) < 22 
 ```
 
Next, using the CSV Data (provided in data file), use the skyServer Large Data Image Search to retrieve each image. The limit is 1000.  (http://skyserver.sdss.org/dr16/en/tools/chart/list.aspx)
I made a program which reads from the csv, searches the image, and saves to file (see imageRetrieval.py). This can be used for any length file.

