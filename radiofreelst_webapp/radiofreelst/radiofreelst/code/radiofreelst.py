
class Source(object):
	def __init__(self):
		self.name = None
		self.ra = None
		self.dec = None
		self.riseLST = None
		self.setLST = None


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



def findLST(observatory, sourceList ):
    '''
    Takes a list of source objects and populates their LST values.

	Parameters
	----------
	observatory : pyephem.observer object
	sourceList : list of Source objects.

    '''

    import ephem

    for source in sourceList:
        
        datastr = "{0},f|V|A0,{1},{2},2000".format(source.name, source.ra, source.dec)

        print ("*****", datastr)

        galaxy = ephem.readdb(datastr)
        galaxy.compute(observatory)        

        if galaxy.circumpolar:
            source.riseLST = 0.0
            source.setLST = 24.0
        elif galaxy.neverup:
            source.riseLST = None
            source.setLST = None
        else:
            observatory.date = galaxy.rise_time
            source.riseLST = observatory.sidereal_time()
            
            observatory.date = galaxy.set_time
            source.setLST = observatory.sidereal_time()

def runMe(observatoryName, horizon, sourceData):

    import ephem

    observatory = setUpObservatory(observatoryName, horizon)
    
    getSourceList(sourceData)

    sourceList = findLST(observatory,sourceList)



    


