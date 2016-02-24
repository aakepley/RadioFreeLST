import ephem
from astropy.coordinates.angles import Angle
import astropy.units as u

class Source(object):
	def __init__(self):
		self.name = None
		#self.ra = None
		#self.dec = None
		self.riseLST = None
		self.setLST = None
		self.neverUp = False
		self.j2000coord = None


def setUpObservatory (observatoryName, horizon):
    """
    set up object with observatory parameters.

    Input:
        observatoryName: name of observatory as string

    Output:
        observatory: pyephem object populated with correct values
    

    Right now I'm hard-coding with GBT values. In the future, it will
    be a database.
    
    """

    import ephem # pyephem

    if observatoryName == 'GBT':
        observatory = ephem.Observer()

        # GBT data from proposer's guide
        observatory.lon =  "-79:50:23.406" # negative sign because west
        observatory.lat = "38:25:59.236"  
        observatory.elevation =  807.43 # m
        observatory.date = "2015/10/1" # This date is arbitrary and shouldn't matter
        observatory.horizon = ephem.degrees(str(horizon)) # for some reason, the argument has to be a string

    return observatory
    
def getSourceList(sourceData):
    """
    get the list of sources

    Input:
        ???

    Output:
        sourceList

    Hard-coding with values.
    
    """

    sourceList = [{'name': 'n1569', 'ra': '04:30:49.0', 'dec':'+64:50:53', 'riseLST':'', 'setLST':''},
                  {'name': 'n4214', 'ra': '+64:50:53', 'dec':'12:15:39.2', 'riseLST':'', 'setLST':''}]

    return sourceList


def sanitizeInput():
    '''

    This function will eventually sanitize the input from the web application
    '''

    pass



def findLST(observatory, sourceList):
    '''
    Takes a list of source objects and populates their LST values.

	Parameters
	----------
	observatory : pyephem.observer object
	sourceList : list of Source objects.

    '''

    for source in sourceList:
        
        # format: http://www.clearskyinstitute.com/xephem/help/xephem.html#mozTocId468501
        ra = "{0[0]:02.0f}:{0[1]:02.0f}:{0[2]:02.0f}".format(source.j2000coord.ra.hms)
        dec = "{0[0]:02.0f}:{0[1]:02.0f}:{0[2]:02.0f}".format(source.j2000coord.dec.dms)
        datastr = "{0},f|V|A0,{1},{2},2000".format(source.name, ra, dec)

        #print ("*****", datastr)

        galaxy = ephem.readdb(datastr)
        
        #print(observatory.date)
        
        galaxy.compute(observatory)        

        if galaxy.circumpolar:
            source.riseLST = Angle(0.0 * u.hour)
            source.setLST = Angle(24.0 * u.hour)
        elif galaxy.neverup:
            #source.riseLST = None
            #source.setLST = None
            source.neverUp = True
        else:
            observatory.date = galaxy.rise_time
            source.riseLST = Angle(observatory.sidereal_time() * u.rad)
            
            observatory.date = galaxy.set_time
            source.setLST = Angle(observatory.sidereal_time() * u.rad)
        print("--> source.riseLST: ", source.riseLST, type(source.riseLST))


def runMe(observatoryName, horizon, sourceData):

    import ephem

    observatory = setUpObservatory(observatoryName, horizon)
    
    getSourceList(sourceData)

    sourceList = findLST(observatory,sourceList)



    


