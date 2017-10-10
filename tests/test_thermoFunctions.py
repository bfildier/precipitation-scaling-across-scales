import sys,os
import numpy as np
import dask.array as da
import matplotlib.pyplot as plt
import time

## Own functions
currentpath = os.getcwd()
sys.path.insert(0,os.path.join(os.path.dirname(currentpath),'functions'))

from thermoFunctions import *

if __name__ == "__main__":

	figdir = os.path.join(currentpath,'figures_tests')
	npts = 5e1
	temp = np.linspace(300,250,num=npts)
	pres = np.linspace(100000,20000,num=npts)
	shum = np.linspace(0.02,0.005,num=npts)
	chunks = npts//4
	temp_da = da.from_array(temp,chunks)
	pres_da = da.from_array(pres,chunks)
	shum_da = da.from_array(shum,chunks)

	print("--Test airDensity:")
	start = time.time()
	rho = airDensity(temp,pres,shum)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print("With dask arrays")
	start = time.time()
	rho_da = airDensity(temp_da,pres_da,shum_da)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print(type(rho_da))
	fig = plt.figure(figsize=(5,4))
	plt.plot(rho,pres/100)
	plt.plot(rho_da.compute(),pres/100,'--')
	plt.xlabel('Density (kg/m3)')
	plt.ylabel('Pressure (hPa)')
	plt.gca().invert_yaxis()
	plt.savefig(os.path.join(figdir,'test_thermoFunctions_airDensity.pdf'),
				bbox_inches='tight')
	print()

	print("--Test saturationVaporPressure")
	start = time.time()
	esat = saturationVaporPressure(temp)
	end = time.time()
	print("time elapsed:",end-start,"s")
	start = time.time()
	esat_da = saturationVaporPressure(temp_da)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print(type(esat_da))
	fig = plt.figure(figsize=(5,4))
	plt.plot(temp,esat)
	plt.plot(temp_da,esat_da,'--')
	plt.xlabel('Temperature (K)')
	plt.ylabel('Saturation vapor pressure (Pa)')
	plt.savefig(os.path.join(figdir,'test_thermoFunctions_saturationVaporPressure.pdf'),
				bbox_inches='tight')
	print()

	print("--Test saturationSpecificHumidity")
	start = time.time()
	qvsat = saturationSpecificHumidity(temp,pres)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print("With dask arrays")
	start = time.time()
	qvsat_da = saturationSpecificHumidity(temp_da,pres_da)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print(type(qvsat_da))
	fig = plt.figure(figsize=(5,4))
	plt.plot(qvsat,pres/100)
	plt.plot(qvsat_da,pres_da/100,'--')
	plt.xlabel('Saturation specific humidity (kg/kg)')
	plt.ylabel('Pressure (hPa)')
	plt.gca().invert_yaxis()
	plt.savefig(os.path.join(figdir,'test_thermoFunctions_saturationSpecificHumidity.pdf'),
				bbox_inches='tight')
	print()

	print("--Test dryAdiabaticLapseRate")
	start = time.time()
	Gamma_dry = dryAdiabaticLapseRate(temp,pres,shum)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print("With dask arrays")
	start = time.time()
	Gamma_dry_da = dryAdiabaticLapseRate(temp_da,pres_da,shum_da)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print(type(Gamma_dry_da))
	fig = plt.figure(figsize=(5,4))
	plt.plot(Gamma_dry*10000,pres/100)
	plt.plot(Gamma_dry_da*10000,pres_da/100,'--')
	plt.xlabel('Dry adiabatic lapse rate (K/100hPa)')
	plt.ylabel('Pressure (hPa)')
	plt.gca().invert_yaxis()
	plt.title('On pressure coordinate')
	plt.savefig(os.path.join(figdir,'test_thermoFunctions_dryAdiabaticLapseRate.pdf'),
				bbox_inches='tight')
	print()

	print("--Test moistAdiabaticLapseRateSimple")
	start = time.time()
	Gamma_m_simple = moistAdiabaticLapseRateSimple(temp,pres,shum)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print("With dask arrays")
	start = time.time()
	Gamma_m_simple_da = moistAdiabaticLapseRateSimple(temp_da,pres_da,shum_da)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print(type(Gamma_m_simple_da))
	fig = plt.figure(figsize=(5,4))
	plt.plot(Gamma_m_simple*10000,pres/100)
	plt.plot(Gamma_m_simple_da*10000,pres_da/100,'--')
	plt.xlabel('Simple moist adiabatic lapse rate (K/100hPa)')
	plt.ylabel('Pressure (hPa)')
	plt.gca().invert_yaxis()
	plt.title('On pressure coordinate')
	plt.savefig(os.path.join(figdir,'test_thermoFunctions_moistAdiabaticLapseRateSimple.pdf'),
				bbox_inches='tight')
	print()
	print()
	print("--Test moistAdiabatSimple")
	print("- Example of what to avoid: using several chunks in the vertical")
	start = time.time()
	temp_adiab = moistAdiabatSimple(temp[0],pres,shum,levdim=0)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print("Also derive it for fewer levels to see the difference")
	pres_15lev = np.linspace(100000,20000,num=15)
	shum_15lev = np.linspace(0.02,0.005,num=15)
	temp_adiab_15lev = moistAdiabatSimple(temp[0],pres_15lev,shum_15lev,levdim=0)
	print("With dask arrays")
	start = time.time()
	temp_adiab_da = da.map_blocks(moistAdiabatSimple,temp_da[0],pres_da,shum_da,0)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print(type(temp_adiab_da))
	fig = plt.figure(figsize=(5,4))
	plt.plot(temp_adiab,pres/100)
	plt.plot(temp_adiab_da,pres_da/100,'--')
	plt.plot(temp_adiab_15lev,pres_15lev/100)
	plt.xlabel('Simple moist adiabat (K)')
	plt.ylabel('Pressure (hPa)')
	plt.gca().invert_yaxis()
	plt.savefig(os.path.join(figdir,'test_thermoFunctions_moistAdiabatSimple_what_not_to_do.pdf'),
				bbox_inches='tight')
	print()
	print("- Again with one single chunk in the vertical")
	nlev = 25
	npts = 5e3
	temp = np.transpose(np.array([np.linspace(300,250,num=nlev)]*
		int(npts/nlev))).reshape(nlev,int(npts/nlev))
	pres = np.transpose(np.array([np.linspace(100000,20000,num=nlev)]*
		int(npts/nlev))).reshape(nlev,int(npts/nlev))
	shum = np.transpose(np.array([np.linspace(0.02,0.005,num=nlev)]*
		int(npts/nlev))).reshape(nlev,int(npts/nlev))
	chunks = (nlev,(npts/nlev)//4)
	temp_da = da.from_array(temp,chunks)
	pres_da = da.from_array(pres,chunks)
	shum_da = da.from_array(shum,chunks)
	# print(temp.shape,pres.shape,shum.shape)
	# print(temp_da.shape,pres_da.shape,shum_da.shape)
	# print(temp_da.chunks,pres_da.chunks,shum_da.chunks)
	start = time.time()
	temp_adiab = moistAdiabatSimple(temp[0],pres,shum,levdim=0)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print("With dask arrays")
	start = time.time()
	# print(temp_da[0].shape,temp_da[0].chunks)
	temp_adiab_da = da.map_blocks(moistAdiabatSimple,temp_da[0],
								  pres_da,shum_da,levdim=0)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print(type(temp_adiab_da))
	print(temp_adiab.shape,temp_adiab_da.shape)
	print(pres.shape,pres_da.shape)
	fig = plt.figure(figsize=(5,4))
	ind = [slice(None),0]
	plt.plot(temp_adiab[ind],pres[ind]/100)
	plt.plot(temp_adiab_da[:,0],pres_da[:,0]/100,'--')
	plt.xlabel('Simple moist adiabat (K)')
	plt.ylabel('Pressure (hPa)')
	plt.gca().invert_yaxis()
	plt.savefig(os.path.join(figdir,'test_thermoFunctions_moistAdiabatSimple_lev_in_dim0.pdf'),
				bbox_inches='tight')
	print()

	print("- Again with one single chunk in the vertical, vertical coordinate "+
		"in second dimension")
	nlev = 25
	npts = 5e3
	temp = np.array([np.linspace(300,250,num=nlev)]*int(npts/nlev)).reshape(
		int(npts/nlev),nlev)
	pres = np.array([np.linspace(100000,20000,num=nlev)]*int(npts/nlev)).reshape(
		int(npts/nlev),nlev)
	shum = np.array([np.linspace(0.02,0.005,num=nlev)]*int(npts/nlev)).reshape(
		int(npts/nlev),nlev)
	chunks = ((npts/nlev)//4,nlev)
	temp_da = da.from_array(temp,chunks)
	pres_da = da.from_array(pres,chunks)
	shum_da = da.from_array(shum,chunks)
	# print(temp.shape,pres.shape,shum.shape)
	# print(temp_da.shape,pres_da.shape,shum_da.shape)
	# print(temp_da.chunks,pres_da.chunks,shum_da.chunks)
	start = time.time()
	temp_adiab = moistAdiabatSimple(temp[:,0],pres,shum,levdim=1)
	end = time.time()
	print("time elapsed:",end-start,"s")
	print("With dask arrays")
	start = time.time()
	# print(temp_da[:,0].shape,temp_da[:,0].chunks)
	temp_adiab_da = da.map_blocks(moistAdiabatSimple,temp_da[:,0],
								  pres_da,shum_da,levdim=1,chunks=((npts/nlev)//4,25))
	end = time.time()
	print("time elapsed:",end-start,"s")
	print(type(temp_adiab_da))
	print(temp_adiab.shape,temp_adiab_da.shape)
	print(pres.shape,pres_da.shape)
	# print(temp_adiab_da.chunks,pres_da.chunks)
	fig = plt.figure(figsize=(5,4))
	plt.plot(temp_adiab[0,:],pres[0,:]/100)
	plt.plot(temp_adiab_da[0,:25],pres_da[0,:]/100,'--')
	plt.xlabel('Simple moist adiabat (K)')
	plt.ylabel('Pressure (hPa)')
	plt.gca().invert_yaxis()
	plt.savefig(os.path.join(figdir,'test_thermoFunctions_moistAdiabatSimple_lev_in_dim1.pdf'),
				bbox_inches='tight')
	print("""Function works with dask arrays with vertical coordinate in second
	dimension, but the output dimension is duplicated many times along that axis.
	That dimension is multiplied by the number of chunks. Needs more work on that.""")
	print()



	sys.exit(0)
