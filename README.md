# Create CF-compliant trajectory NetCDF file

The script `make_trajectory_netcdf.py` creates a CF-compliant trajectory NetCDF file from an input file.


## Usage

Example usage using the two example files included in this repo.

### 1. Example 1

This example uses a csv files where all of the required columns have the default axes labels required by the `pocean-core` library used by this script to create the CF-compliant trajectory NetCDF files.

The example dataset has the following format:

```bash
head inputs/example_input_01.csv
time,lon,lat,depth,trajectory,temperature,humidity
1990-01-01 00:00:00.000000,-35.078842,2.152863,0.0,Trajectory0,13.466983,65.38418
1990-01-01 01:00:00.000000,-44.12696,33.60481,1.0,Trajectory0,23.050304,7.0401154
1990-01-01 02:00:00.000006,-18.115444,22.562508,2.0,Trajectory0,15.112072,45.15019
```

To convert files adhering to this structure, the command is simply:


```bash
python make_trajectory_netcdf.py inputs/example_input_01.csv outputs/example_output_01.nc
```

The result is a CF-compliant trajectory NetCDF file

```bash
ncdump -h outputs/example_output_01.nc
netcdf example_output_01 {
dimensions:
	obs = 50 ;
	trajectory = 4 ;
variables:
	string trajectory(trajectory) ;
		trajectory:cf_role = "trajectory_id" ;
		trajectory:long_name = "trajectory identifier" ;
	double time(trajectory, obs) ;
		time:_FillValue = -9999.9 ;
		time:units = "seconds since 1990-01-01 00:00:00Z" ;
		time:standard_name = "time" ;
		time:axis = "T" ;
	double depth(trajectory, obs) ;
		depth:_FillValue = -9999.9 ;
		depth:axis = "Z" ;
	double lat(trajectory, obs) ;
		lat:_FillValue = -9999.9 ;
		lat:axis = "Y" ;
	double lon(trajectory, obs) ;
		lon:_FillValue = -9999.9 ;
		lon:axis = "X" ;
	double temperature(trajectory, obs) ;
		temperature:_FillValue = -9999.9 ;
		temperature:coordinates = "time depth lon lat" ;
	double humidity(trajectory, obs) ;
		humidity:_FillValue = -9999.9 ;
		humidity:coordinates = "time depth lon lat" ;
	int crs ;

// global attributes:
		:Conventions = "CF-1.6" ;
		:date_created = "2019-04-01T22:13:00Z" ;
		:featureType = "trajectory" ;
		:cdm_data_type = "Trajectory" ;
```

### 2. Example 2

This example uses the same csv file as in Example 1, but the column names have been changed, and there is extra-column with a "battery" status.

```bash
head inputs/example_input_02.csv
datetime,longitude,latitude,depths,particle_id,temperature,humidity,battery
1990-01-01 00:00:00.000000,-35.078842,2.152863,0.0,Trajectory0,13.466983,65.38418,low
1990-01-01 01:00:00.000000,-44.12696,33.60481,1.0,Trajectory0,23.050304,7.0401154,low
1990-01-01 02:00:00.000006,-18.115444,22.562508,2.0,Trajectory0,15.112072,45.15019,low
```

To handle this, the column names must be passed to the script as command line arguments.

```bash
python make_trajectory_file.py inputs/example_input_02.csv outputs/example_output_02.nc --time datetime --lat latitude --lon longitude --depth depths --trajectory particle_id
```

Notice the output for the second file reflects the different names of the axes and includes the "battery" status as a string.

```bash
ncdump -h outputs/example_output_02.nc
netcdf example_output_02 {
dimensions:
	obs = 50 ;
	particle_id = 4 ;
variables:
	string particle_id(particle_id) ;
		particle_id:cf_role = "trajectory_id" ;
		particle_id:long_name = "trajectory identifier" ;
	double datetime(particle_id, obs) ;
		datetime:_FillValue = -9999.9 ;
		datetime:units = "seconds since 1990-01-01 00:00:00Z" ;
		datetime:standard_name = "time" ;
		datetime:axis = "T" ;
	double depths(particle_id, obs) ;
		depths:_FillValue = -9999.9 ;
		depths:axis = "Z" ;
	double latitude(particle_id, obs) ;
		latitude:_FillValue = -9999.9 ;
		latitude:axis = "Y" ;
	double longitude(particle_id, obs) ;
		longitude:_FillValue = -9999.9 ;
		longitude:axis = "X" ;
	double temperature(particle_id, obs) ;
		temperature:_FillValue = -9999.9 ;
		temperature:coordinates = "datetime depths longitude latitude" ;
	double humidity(particle_id, obs) ;
		humidity:_FillValue = -9999.9 ;
		humidity:coordinates = "datetime depths longitude latitude" ;
	string battery(particle_id, obs) ;
		battery:coordinates = "datetime depths longitude latitude" ;
	int crs ;

// global attributes:
		:Conventions = "CF-1.6" ;
		:date_created = "2019-04-01T22:35:00Z" ;
		:featureType = "trajectory" ;
		:cdm_data_type = "Trajectory" ;
}
```
