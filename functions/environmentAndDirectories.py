"""Module environmentAndDirectories

Contains functions to define directory structure, paths and other settings.
"""

#---- modules ----#

import socket, os

hostname = socket.gethostname()

#---- Own functions ----#
# currentpath = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(0,os.path.join(os.path.dirname(currentpath),'functions'))

#---- Functions ----#

## Define dataroot
def getDataroot(compset=None):
	## Host name
	if hostname in ["jollyjumper","Jordans-Air"] or "ucbvpn" in hostname:
		## Parent directory to load data
		dataroot = "/Users/bfildier/Data"
	elif "edison" in hostname or "cori" in hostname or "nid" in hostname:
		if compset == 'FAMIPC5':
			dataroot = "/global/cscratch1/sd/bfildier"
		else:
			dataroot = "/global/cscratch1/sd/bfildier/lawrencium_runs"
	return dataroot

## Define input directories for different platforms
def getInputDirectories(compset,experiment):

	"""Arguments:
		- compset is FSPCAMm_AMIP or FAMIC5
		- experiment is piControl of abrupt4xCO2
	Returns inputdir, inputdir_processed_day, inputdir_processed_1hr,
		inputdir_results, inputdir_fx."""

	case = "bf_%s_%s"%(compset,experiment)
	dataroot = getDataroot(compset)

	if hostname in ["jollyjumper","Jordans-Air"] or "ucbvpn" in hostname:
		inputdir = os.path.join(dataroot,"simulations",case)		
	elif "edison" in hostname or "cori" in hostname or "nid" in hostname:
		inputdir = os.path.join(dataroot,'archive',case,"atm/hist")

	inputdir_processed_day = os.path.join(dataroot,'preprocessed',case,'day')
	inputdir_processed_1hr = os.path.join(dataroot,'preprocessed',case,'1hr')
	inputdir_results = os.path.join(dataroot,'results')
	inputdir_fx = os.path.join(dataroot,'preprocessed/allExperiments/fx')

	return inputdir, inputdir_processed_day, inputdir_processed_1hr,\
		inputdir_results, inputdir_fx

	