
from typing import List
from pathlib import Path
import re
import numpy as np
import pandas as pd
import sxl
import warnings
from datetime import datetime

from . import logger, DataConverter
from battkit.dataset.test_schema import TimeSeriesSchema
from battkit.utils.file_utils import get_xlsx_sheet_ids

class NewareDataConverter(DataConverter):

	# Use class variables and @staticmethod decorator to allow for efficient parallelization
	name = "Neware"
	file_types = ['.xlsx',]
	default_group_by = {
		"TESTER_ID":int, 
		"UNIT_ID":int,
		"CHANNEL_ID":int, 
	}

	def __init__(self):
		super().__init__(NewareDataConverter.name, NewareDataConverter.file_types)

	## REQUIRED METHOD DEFINITIONS ##
	@staticmethod
	def define_schema() -> dict:
		return {
			"TEST_TYPE":str,
			"TESTER_ID":int, 
			"UNIT_ID":int,
			"CHANNEL_ID":int, 
			"PROTOCOL":str, 
			"FILENAME":str,
			"DATETIME_START":datetime,
			"DATETIME_END":datetime,
		}

	@classmethod
	def validate_file_type(cls, file:Path) -> bool:
		"""Checks whether the provided file uses a file type supported by this DataConverter"""
		if file.suffix not in cls.file_types:
			logger.error(f"Validation failed. File type ({file.suffix}) is not supported by {cls.name}.")
			return False
		logger.debug(f"Validation successful. File type ({file.suffix}) is supported by {cls.name}.")
		return True

	@classmethod
	def validate_converter(cls, file:Path):
		# Check whether this file matches the Neware tester format 
		# Perform checks sorted by operation execution time (ie, check file suffix first, 
		# then sheet names is Excel file, etc)
		# Want to read the least amount of information necessary to determine if the file 
		# matches the Neware format

		# 1. Check that the file type is supported
		if not cls.validate_file_type(file):
			return False
		
		# 2. For xlsx files, check formatting
		if file.suffix == '.xlsx':
			sheet_names = get_xlsx_sheet_ids(file)
			if 'Info' not in sheet_names: 
				logger.error(f"Validation failed. Excel file is missing required {cls.name} sheet name (\'Info\').")
				return False
			
			# The 'Info' sheet has several fixed cell values, those are checked below
			info_fmt = sxl.Workbook(file).sheets['Info'].rows[7][0]
			expected_fmt = ['device', 'Unit', 'Channel', 'P/N', 'Step file', 'Starting time', 'End time', 'Sorting files', 'Class', 'Remarks']
			if not info_fmt == expected_fmt:
				logger.error(f"Validation failed. \'Info\' sheet does not match {cls.name} format.")
				return False

		# 3. Other formats not yet supported
		else:
			logger.error(f"Validation failed. File type ({file.suffix}) is supported but not yet implemented.")
			return False

		logger.debug(f"Validation successful. File matches the {cls.name} format.")
		return True
	
	@classmethod
	def extract_group_by_data(cls, file:Path) -> dict:
		grouping_data = {k:None for k in cls().group_by_schema}
		
		if file.suffix == '.xlsx':
			grouping_data["TEST_TYPE"] = "TimeSeries"			# TODO: assuming all Neware data is TimeSeries (do they have EIS?)
			# Extract grouping data from this file
			data = sxl.Workbook(file).sheets['Info'].rows[8][0]
			grouping_data["TESTER_ID"] = int(data[0])
			grouping_data["UNIT_ID"] = int(data[1])
			grouping_data["CHANNEL_ID"] = int(data[2])
			grouping_data["PROTOCOL"] = str(data[4])
			grouping_data["FILENAME"] = file.name
			grouping_data["DATETIME_START"] = datetime.strptime(str(data[5]), "%Y-%m-%d %H:%M:%S")
			grouping_data["DATETIME_END"] = datetime.strptime(str(data[6]), "%Y-%m-%d %H:%M:%S")
			
		else:
			logger.error(f"File type ({file.suffix}) not currently supported.")
			raise TypeError(f"File type ({file.suffix}) not currently supported.")
		
		# Check if there are supported group_by terms that have no values
		missing_groups = [k for k,v in grouping_data.items() if v is None]
		if missing_groups:
			logger.warning(f"Following group_by terms are missing values: {missing_groups}")

		logger.debug(f"Group_by data extracted successfully.")
		return grouping_data
	
	@classmethod
	def extract_timeseries_data(cls, file:Path) -> pd.DataFrame:
		# Check file validation
		if not cls.validate_converter(file):
			raise ValueError(f"Validation failed for the {cls.name} DataConverter.")
		
		# Create dataframe to return using required columns from 
		schema = TimeSeriesSchema()
		df_to_return = pd.DataFrame(columns=schema.req_schema.keys())

		# Format time-series data for each supported file type
		# For .xlsx files
		if file.suffix == '.xlsx':
			sheet_names = np.asarray(get_xlsx_sheet_ids(file))

			df = None
			#region: load details sheet
			sheet_name_details = sheet_names[np.where(np.char.find(sheet_names, 'Detail_') == 0)]
			assert len(sheet_name_details) == 1
			with warnings.catch_warnings():
				warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
				df = pd.read_excel(file, sheet_name=sheet_name_details[0], engine='openpyxl')
				df.rename(columns={'Date(h:min:s.ms)':'Date'}, inplace=True)
			#endregion

			#region: if has temperature information in separate sheet, merge sheets
			sheet_name_temp = sheet_names[np.where(np.char.find(sheet_names, 'DetailTemp_') == 0)]
			if len(sheet_name_temp) == 1:
				with warnings.catch_warnings():
					warnings.filterwarnings("ignore", category=UserWarning, module=re.escape('openpyxl.styles.stylesheet'))
					df_temp = pd.read_excel(file, sheet_name=sheet_name_temp[0], engine='openpyxl')
				df_temp.drop(columns=['Record number', 'Relative Time(h:min:s.ms)'], inplace=True)
				df_temp.rename(columns={'Aux.CH TU1 T(°C)':'Temperature'}, inplace=True)
				# merge temperature and fill any gaps with linear interpolation
				df = pd.merge(left=df, right=df_temp, how='inner', on=['Date', 'State'])
				df['Temperature'] = df['Temperature'].interpolate(method='linear', inplace=False)
				df.drop_duplicates(subset='Record number', inplace=True, ignore_index=True)
			#endregion
			
			df_to_return['RECORD_NUMBER'] = df['Record number'].astype(int).values
			df_to_return['CYCLE_NUMBER'] = df['Cycle'].astype(int).values
			df_to_return['STEP_NUMBER'] = df['Steps'].astype(int).values
			df_to_return['STEP_MODE'] = df['State'].str.upper().values

			#region: get units of voltage, current, and capacity columns
			headers = cls.extract_data_headers(file)
			v_key = headers[np.argwhere(np.char.find(headers, 'Voltage') == 0)[0][0]]
			v_modifier = 1 if (v_key.rfind('mV') == -1) else (1/1000)
			i_key = headers[np.argwhere(np.char.find(headers, 'Current') == 0)[0][0]]
			i_modifier = 1 if (i_key.rfind('mA') == -1) else (1/1000)
			q_key = headers[np.argwhere(np.char.find(headers, 'Capacity') == 0)[0][0]]
			q_modifier = 1 if (q_key.rfind('mAh') == -1) else (1/1000)
			#endregion
			
			df_to_return['VOLTAGE_V'] = df[v_key].astype(float).values * v_modifier
			df_to_return['CURRENT_A'] = df[i_key].astype(float).values * i_modifier

			# calculate the sign of current (-1 if DCHG step)
			signs = np.asarray([-1 if 'DCHG' in step_mode else 1 for step_mode in df_to_return['STEP_MODE'].values])
			df_to_return['STEP_CAPACITY_AH'] = df[q_key].astype(float).values * q_modifier * signs

			#region: calculate cumulative capacity
			# dqs = np.zeros(len(df_to_return['STEP_CAPACITY(AH)']), dtype=float)
			# for step_num in df_to_return['STEP NUMBER'].unique():
			# 	df_step = df_to_return.loc[(df_to_return['STEP_NUMBER'] == step_num)]
			# 	idxs = df_step.index.values
			# 	assert len(df_step['STEP MODE'].unique()) == 1
			# 	sign = -1 if 'DChg' in df_step['STEP MODE'].unique()[0] else 1
			# 	dqs[idxs[1:]] = df_step['STEP CAPACITY (AH)'].diff().values[1:] * sign
			# 	dqs[idxs[0]] = 0
			# q_cum = np.cumsum(dqs)
			# df_to_return['PROTOCOL_CAPACITY(AH)'] = q_cum.astype(float)
			#endregion

			#region: calculate time
			step_time = pd.to_datetime(df['Relative Time(h:min:s.ms)'], format=r"%H:%M:%S.%f")
			rel_seconds = (step_time - pd.to_datetime(df['Relative Time(h:min:s.ms)'].values[0], format=r"%H:%M:%S.%f")).dt.total_seconds().values
			d_seconds = np.hstack([0, np.diff(rel_seconds)])
			d_seconds[np.where(d_seconds < 0)] = 0
			cum_seconds = np.cumsum(d_seconds)
			df_to_return['TIME_S'] = cum_seconds.astype(float)
			# # convert total time to TIMESTAMP format
			# start_date = pd.to_datetime(df['Date'], format=r"%Y-%m-%d %H:%M:%S").values[0]
			# timestamps = (start_date + pd.to_timedelta(cum_seconds, unit='second')).strftime(r"%Y-%m-%d %H:%M:%S.%f")
			# df_to_return['TIMESTAMP'] = timestamps
			#endregion
			
			#region: add any optional parameters
			if 'Temperature' in df.columns:
				df_to_return['CELL_TEMPERATURE_C'] = df['Temperature'].astype(float).values
			#endregion

		# TODO: add support for other file types
		else:
			logger.error(f"Time-series extraction failed. File type ({file.suffix}) is supported but not yet implemented.")
			raise ValueError(f"Time-series extraction failed. File type ({file.suffix}) is supported but not yet implemented.")

		#region: validate schema
		if not schema.validate_data({col: df_to_return[col].dtype for col in df_to_return.columns}):
			raise ValueError("Validation failed. Extracted time-series data does not match expected schema.")
		
		if not schema.validate_step_mode(df_to_return['STEP_MODE'].unique()):
			raise ValueError("Validation failed. Steps modes contain unsupported values.")
		#endregion

		return df_to_return

	## HELPER METHODS ##
	@classmethod
	def extract_data_headers(cls, file:Path) -> List[str]:
		"""Extracts the headers of the data contained in the file."""

		sheet_names = get_xlsx_sheet_ids(file)
		sheet_name_details = sheet_names[np.where(np.char.find(sheet_names, 'Detail_') == 0)[0][0]]

		headers = sxl.Workbook(file).sheets[sheet_name_details].rows[1][0]
		return headers
	

# # Neware Excel files have the following sheet_names:
# #   'Info': 									general protocol information
# #   'Cycle_{Tester-ID}_{Unit}_{Channel}': 	summary statistics over cycles (avg/sum for each cycle num)
# #	  'Statis_{Tester-ID}_{Unit}_{Channel}': 	summary statistics over step numbers (avg/sum for each step num)
# #	  'Detail_{Tester-ID}_{Unit}_{Channel}': 	the raw sampled data
# #      - header: [Record number	State	Jump	Cycle	Steps	Current(A)	Voltage(V)	Capacity(Ah)	Energy(Wh)	Relative Time(h:min:s.ms)	Date(h:min:s.ms)]
# #      - Note that units may change based on users configured settings

# #   'DetailVol_{Tester-ID}_{Unit}_{Channel}':	optional, stores delta_U and delta_P
# #   'DetailTemp_{Tester-ID}_{Unit}_{Channel}': optional, stored auxilliary temperature
# #      - header: [Record number	State	Relative Time(h:min:s.ms)	Date	Aux.CH TU1 T(°C)	Aux. ΔT]
# #      - 'Aux.CH TU1 T(°C)' stores thermocouple values
