
import os, time, shutil, json
import numpy as np
import pandas as pd
import dask.dataframe as dd
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Union, Dict, Type
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

from battkit.config import MEMORY_LIMIT
from battkit.logging_config import logger
from battkit.dataset.data_converter import load_data_converter, DATA_CONVERTER_REGISTRY
from battkit.utils.dataframe_utils import dask_partition_file_naming_fnc, dask_partition_file_naming_sort_fnc





def infer_data_converter(file:Path) -> str:
	"""Returns the name of the inferred DataConverter subclass. Inferred from the DATA_CONVERTER_REGISTRY."""
	valid_data_converters = []
	for dc_name in DATA_CONVERTER_REGISTRY:
		data_converter = load_data_converter(dc_name)
		if data_converter.validate_converter(file):
			valid_data_converters.append(dc_name)

	if not valid_data_converters:
		logger.error("Failed to find a suitable data converter.")
		raise RuntimeError("Failed to find a suitable data converter. Please manually specify one")

	elif len(valid_data_converters) > 1:
		logger.warning(f"Multiple valid data converters were detected. The first one will be used ({valid_data_converters[0]}).")

	return valid_data_converters[0]

def _extract_group_by_single(file:Path, data_converter:str) -> dict:
	converter_instance = load_data_converter(data_converter)
	try:
		gb = converter_instance.extract_group_by_data(file)
		if gb is None or len(gb) == 0:
			return {}
		gb['FILEPATH'] = str(file)
		gb['DATA_CONVERTER'] = data_converter
		return gb
	except Exception as e:
		logger.error(f"Error processing file {file}: {e}")
		raise e  # Reraise to propagate the error

def _extract_group_by_data(files:Union[Path, List[Path]], data_converter:str, n_jobs:int=-1) -> pd.DataFrame:	
	if n_jobs == -1: n_jobs = os.cpu_count()
	if not hasattr(files, '__len__'): files = [files]

	partial_function = partial(_extract_group_by_single, data_converter=data_converter)

	start_time = time.time()
	with ProcessPoolExecutor(max_workers=n_jobs) as executor:
		gbs = list(executor.map(partial_function, files))
	logger.info(f"Extracted group_by data from {len(files)} files in {round(time.time()-start_time, 4)} seconds.")
	return pd.DataFrame(gbs).dropna(axis=0, how='all')	# drop any empty rows


def _extract_time_series(data_converter:str, file:Path) -> tuple:
	converter_instance = load_data_converter(data_converter)
	df = converter_instance.extract_timeseries_data(file)
	return df, file

def _extract_frequency(data_converter:str, file:Path) -> tuple:
	converter_instance = load_data_converter(data_converter)
	df = converter_instance.extract_frequency_data(file)
	return df, file


class Dataset:
	def __init__(self, name:str, dir_storage:Path, overwrite_existing:bool=False):
		self._name = name
		if not dir_storage.exists():
			logger.error(f"Directory ({dir_storage}) does not exist.")
			raise ValueError(f"Directory ({dir_storage}) does not exist.")
		
		self._tables = {}		# Organizes tabular data by name (str:dataframe)
		self._summary = {}		# Stores summary statistics

		self.dir_storage = dir_storage.joinpath(f"Dataset {self._name}")
		if self.dir_storage.exists():
			if not overwrite_existing:
				logger.info(f"Dataset already exists at this location. Loading saved files.")
				try:
					self._load_existing_dataset()
				except Exception as e:
					logger.error(f"Could not load existing dataset at {self.dir_storage}")
					raise e
			else:
				import shutil
				shutil.rmtree(self.dir_storage)
				self.dir_storage.mkdir(exist_ok=False, parents=True)
		else:
			self.dir_storage.mkdir(exist_ok=False, parents=True)

	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, new_name:str):
		self._name = new_name


	def get_summary(self, summary_type:str='Files'):
		"""Retrieve the given summary type

		Args:
			summary_type (str, optional): {'Files' or any TestSchema name}. Defaults to 'Files'.
		"""
		if not summary_type in self._summary.keys():
			logger.error(f"Unknown summary type: ({summary_type}).")
			raise ValueError(f"{summary_type} does not exist in this dataset.")
		
		if summary_type == 'Files':
			df_summary = pd.DataFrame(self._summary['Files']).T
			return df_summary
		else:
			df_s = pd.DataFrame(self._summary[summary_type]).T
			return df_s.reset_index().rename(columns={"index":"CELL_ID"})


	def get_table(self, name:str):
		"""Retrieve the specified table. \n
			*Note:* The default index is the RECORD_NUMBER and thus repeats for each FILE_ID \
				(ie, **the default index is not unique**). If a unique index is needed, convert to Pandas and \
				use a multi-index with 'FILE_ID' & 'RECORD_NUMBER'. Multi-indices are not currently \
				supported in Dask. Ex: `df.set_index(['FILE_ID', 'RECORD_NUMBER'], drop=False, inplace=True)`"""
		if name not in self._tables.keys():
			logger.error(f"Table ({name}) does not exist.")
			raise ValueError(f"Table ({name}) does not exist. Try adding it first.")
		return self._tables[name]

	def add_files(self, dir_files:Union[Path, List[Path]], group_by:Union[str, List[str]]=None, data_converter:str=None, custom_label:str=None, n_jobs:int=-1) -> bool:
		"""
		Add raw files under the `dir_files` directory to the dataset. 
		Data will be standardized and appended to the corresponding key in the `tables` attribute.

		Args:
			dir_files (Path): Directory or list of filepaths containing the raw data to add.
			group_by (Union[str, List[str]], optional): The key(s) to use to group files belonging to the 
				same cell (e.g., ['CHANNEL_ID']). If not specified, defaults keys defined by the 
				DataConverter will be used. Defaults to None.
			data_converter (str, optional): Can specify the appropriate DataConverter name for these 
				files, if known. Otherwise, an appropriate DataConverter will be automatically selected. 
				Defaults to None.
			custom_label (str, optional): Can choose to add a custom label to the provided set of files for future sorting (eg, label='diagnostics'). Defaults to None.
			n_jobs (int, optional): Can specify the number of parallel cores to use. 
				Defaults to -1 (all available CPU cores).

		Returns:
			bool: Return True if files are added successfully, otherwise returns False.
		"""

		# Set number of parallel workers
		if n_jobs == -1: n_jobs = os.cpu_count()

		# Get all files from folder (search recursively)
		files = None
		if hasattr(dir_files, '__len__'):
			files = dir_files
		elif isinstance(dir_files, Path) and dir_files.is_file():
			files = [dir_files]
		elif isinstance(dir_files, Path) and dir_files.is_dir():
			files = [f for f in dir_files.rglob('*') if not f.name.startswith('.') and f.is_file()]
		else:
			logger.error(f"dir_files is not a file or directory: {dir_files}")
			raise TypeError("dir_files is not a directory or filepath.")
		
		# Check if files have already been added
		next_file_id = 0
		if 'Files' in self._tables.keys():
			files = [f for f in files if f.name not in self._tables['Files']['FILENAME'].values]
			next_file_id = self._tables['Files']['FILE_ID'].max() + 1
		if len(files) == 0:
			logger.info("There are no new files to process.")
			return True
		

		# Infer converter_instance if not provided
		# TODO: We are assuming the same data converter applies to all files. It may be better to check for every file 
		# which could be sped up using parallelization (inference takes ~0.1s per file for a single process)
		if data_converter is None: 
			data_converter = infer_data_converter(files[0])
		converter_instance = load_data_converter(data_converter)

		if not converter_instance.validate_converter(files[0]):
			logger.error(f"{converter_instance.__repr__()} is not compatible with the given files: {files[0]}.")
			raise ValueError(f"{converter_instance.__repr__()} is not compatible with the given files.")
		
		# Extract group_by data and organize by specified group_by term
		df_group_by = _extract_group_by_data(files, data_converter, n_jobs=n_jobs)
		
		# Get group_by terms if not specified
		group_by = None
		if group_by is None: 
			try:
				group_by = list(converter_instance.default_group_by.keys())
			except:
				group_by = list(converter_instance.group_by_schema.keys())
		missing_keys = [k for k in group_by if k not in df_group_by.columns]
		if missing_keys:
			logger.error(f"Group_by keys ({missing_keys}) do not exist in the extracted file data.")
			raise ValueError(f"Group_by keys ({missing_keys}) do not exist in the extracted file data. Select new group_by terms.")

		# Assign CELL_ID column
		gb = df_group_by.groupby(by=group_by)
		df_group_by['CELL_ID'] = gb.ngroup().fillna(0)
		df_group_by['GROUP_BY'] = np.full(len(df_group_by), fill_value=str(group_by))
		# df_group_by['GROUP_BY_VALUES'] = df_group_by[group_by_conditions].apply(tuple, axis=1)

		# Assign FILE_ID column
		df_group_by.sort_values(by=["CELL_ID"] + group_by, inplace=True)
		df_group_by.reset_index(drop=True, inplace=True)
		df_group_by.index.name = 'FILE_ID'
		df_group_by.reset_index(drop=False, inplace=True)	
		df_group_by['FILE_ID'] += next_file_id		

		# Create 'Files' table
		table_keys = ['FILE_ID', 'CELL_ID'] + [k for k in df_group_by.columns if k not in ['FILE_ID', 'CELL_ID', 'FILEPATH']]
		files_table = df_group_by[table_keys].copy()
		files_table['LABEL'] = str(custom_label) if custom_label is not None else ''
		self._update_table(name='Files', data=files_table)

		# Standardize all raw files and temporarily resave (stored as {dir_storage}/FILENAME.parquet)
		start_time = time.time()
		with ProcessPoolExecutor(max_workers=n_jobs) as executor:
			futures = []
			for i in range(len(df_group_by)):
				file = Path(df_group_by.iloc[i]['FILEPATH'])
				test_type = df_group_by.iloc[i]['TEST_TYPE']
				if test_type == 'TimeSeries':
					futures.append( executor.submit(_extract_time_series, data_converter, file) )
				elif test_type == 'Frequency':
					futures.append( executor.submit(_extract_frequency, data_converter, file) )
				else:
					logger.error(f"Test type ({test_type}) is not supported by {converter_instance}.")
					raise ValueError(f"Test type ({test_type}) is not supported.")
			
			for future in as_completed(futures):
				df, file = future.result()
				if df is None or df.empty:
					logger.warning(f"Failed to extract data from file: {file}. File has been skipped.")
					continue
				filepath = self.dir_storage.joinpath("standardized_raw_files", f"{file.stem}.parquet")
				filepath.parent.mkdir(exist_ok=True, parents=False)
				logger.debug(f"Successfully processed {(file)}. Stored to {(filepath)}.")
				df.to_parquet(filepath)
		
		logger.info(f"Extracted data from {len(df_group_by)} files in {round(time.time()-start_time, 4)} seconds.")

		# Update timeseries or frequency table
		self._update_table_from_processed_files()
		return True

	def regroup(self, group_by:Union[str, List[str]]=None, mapping:Optional[dict]=None):
		"""Regroups cells and files based on a new set of group_by terms or an explicit mapping. 

		Args:
			group_by (Union[str, List[str]], optional): The new key(s) to use to group files belonging to the same cell (e.g., ['CHANNEL_ID', 'PROTOCOL', etc]). Defaults to None.
			mapping (Optional[dict], optional): An explicit mapping of \'FILE_ID\' to \'CELL_ID\'. Defaults to None.
		"""

		if (group_by is None) and (mapping is None):
			logger.error(f"\'group_by\' and \'mapping\' are both None.")
			raise ValueError("You must provide either new \'group_by\' terms or an explicit \'mapping\'.")
		if (not group_by is None) and (not mapping is None): 
			logger.error(f"\'group_by\' and \'mapping\' are both defined. Only one can be defined.")
			raise ValueError("Provide either a new \'group_by\' terms or an explicit \'mapping\', not both.")


		files_table = self.get_table('Files')
		new_gb_term = 'USER DEFINED'

		# Step 1 - Re-group all existing FILE_IDs based on new grouping terms (creates an explicit mapping)
		if mapping is None:
			new_gb_term = [group_by,] if isinstance(group_by, str) else group_by
			missing_keys = [k for k in group_by if k not in files_table.columns]
			if missing_keys:
				logger.error(f"Group_by keys ({missing_keys}) do not exist in the \'Files\' table.")
				raise ValueError(f"Group_by keys ({missing_keys}) do not exist in the \'Files\' table.  You must use a subset of the following keys: {files_table.columns}.")

			# Create mapping using new group_by terms: mapping={} (keys=existing FILE_ID, vals=new CELL_ID)
			gb = files_table.groupby(by=group_by)
			file_ids = files_table['FILE_ID'].loc[gb.ngroup().index].values
			cell_ids = gb.ngroup().values
			mapping = {int(file_ids[i]): int(cell_ids[i]) for i in range(len(file_ids))}

		# Step 2 - Use explicit mapping (keys=existing FILE_ID, vals=new CELL_ID) to update tables
		# Ensure all FILE_IDs (only only those FILE_IDs) are defined in mapping
		valid_file_ids = self.get_table('Files')['FILE_ID'].values
		invalid_keys = [int(k) for k in mapping.keys() if k not in valid_file_ids]
		missing_keys = [int(k) for k in valid_file_ids if k not in mapping.keys()]
		if invalid_keys: 
			logger.error(f"Invalid FILE_IDs in mapping: {invalid_keys}.")
			raise ValueError(f"Invalid FILE_IDs in mapping: {invalid_keys}.")
		if missing_keys:
			logger.warning(f"The following FILE_IDs are missing from \'mapping\': {missing_keys}. The missing FILE_IDs will remain at the previously mapped CELL_ID.")

		# Update Files table: rewrite CELL_ID and GROUP_BY columns
		files_table['CELL_ID'] = files_table['FILE_ID'].map(mapping).fillna(files_table['CELL_ID'])
		files_table.loc[files_table['FILE_ID'].isin(mapping), 'GROUP_BY'] = np.full(shape=len(mapping), fill_value=str(new_gb_term))
		self.create_table(name='Files', data=files_table, overwrite_existing=True)


		# Re-create all test_type tables with new FILE_ID and CELL_ID values
		for test_type in files_table['TEST_TYPE'].unique():
			files_to_add = files_table.loc[
				(files_table['TEST_TYPE'] == test_type),
				['FILE_ID', 'CELL_ID', 'FILENAME']].copy()
		
			if len(files_to_add) > 0:
				files_to_add['FILENAME_STANDARDIZED'] = files_to_add['FILENAME'].apply(lambda f: f"{Path(f).stem}.parquet")
				# For each row in files_to_add, read the file to dask dataframe and assign the file_id index
				ddfs = [dd.read_parquet(
					self.dir_storage.joinpath("standardized_raw_files", row.FILENAME_STANDARDIZED)).assign(
						FILE_ID=row.FILE_ID,
						CELL_ID=row.CELL_ID
					) for row in files_to_add.itertuples(index=False)]
				# Concatenate all DataFrames
				ddf = dd.concat(ddfs)
				reordered_keys = ['FILE_ID', 'CELL_ID'] + [k for k in ddf.columns if k not in ['FILE_ID', 'CELL_ID']]
				ddf = ddf[reordered_keys]
				self.create_table(test_type, ddf, overwrite_existing=True)

		logger.info(f"Re-mapped CELL_IDs. All tables have been regenerated.")


	def export(self, dir_save:Path, overwrite:bool=False) -> Path:
		"""Export the current Dataset to the specified directory.

		Args:
			dir_save (Path): Location to save Dataset (a new folder will be created within this directory)

		Returns:
			Path: Location of saved Dataset.
		"""
		
		# Datasets are exported using the following structure:
		# |- {dir_save}/{Dataset.name}/
		# 	|- standardized_raw_files/			-> Stores all standardized raw data
		#		|- {raw_file_name}.parquet
		#		|- ...
		#	|- tables/							-> Stores all table data
		#		|- Files/
		#			|- File_p0.parquet
		#			|- ...
		#		|- TimeSeries/
		#			|- TimeSeries_p0.parquet
		#			|- ...
		#		|- Frequency/
		#			|- Frequency_p0.parquet
		#			|- ...
		#	|- config.json						-> Store other Dataset attributes (eg, name, schemas, etc)

		# Create main folder to export Dataset
		dir_export = dir_save.joinpath(f"Dataset {self._name}")
		if dir_export.exists():
			if overwrite:
				shutil.rmtree(dir_export)
				dir_export.mkdir(exist_ok=False, parents=True)
			else:
				logger.error(f"Dataset already exists at {dir_export}")
				raise FileExistsError("Dataset already exists at this location. Set `overwrite` to True if you want to replace it.")

		# Export all tables as parquet files
		for t_name in self._tables.keys():
			self._save_table(t_name, dir_export)
		
		# Export all standardized data
		if self.dir_storage.joinpath("standardized_raw_files").is_dir():
			shutil.copytree(
				src=self.dir_storage.joinpath("standardized_raw_files"),
				dst=dir_export.joinpath("standardized_raw_files"))
		
		self._save_config(dir_export)

		return dir_export

	def _identify_table_type(self, headers:List[str]) -> Union[str, None]:
		"""Identify the table name (eg, \'TimeSeries\') from a given list of column names.

		Args:
			headers (List[str]): List of column names.

		Returns:
			Union[str, None]: Returns the table name (str) if only one matching table exists. Else, returns None.
		"""
		matching_tables = []
		for table_name in self._tables.keys():
			dd = self.get_table(table_name)
			# Check if all headers exist in this table
			if set(headers).issubset(set(dd.columns)):  
				matching_tables.append(table_name)
		if len(matching_tables) > 1:
			raise ValueError("These column names match multiple tables. You will need to specify the table type.")
		elif len(matching_tables) == 0:
			return None
		else:
			return matching_tables[0]


	def filter(self, table_name:Optional[str]=None, data:Optional[Union[pd.DataFrame, dd.DataFrame]]=None, **conditions) -> dd.DataFrame:
		"""Filters the specified table or data based on conditions applied to the 'Files' table and the specified table.

		Args:
			table_name (Optional[str], optional): The name of the table to filter (eg, 'TimeSeries'). If not specified, the table type is automatically determined from the \'data\' schema.
			data (Optional[Union[pd.DataFrame, dd.DataFrame]], optional): The subset of data to filter. If None, the entire table specified by \'table_name\' is filtered.
			conditions (dict): Key-value pairs specifying filtering conditions. 

		Returns:
			dd.DataFrame: Dask DataFrame comprising a filtered subset of the specified table or data.
		"""
		if table_name is None: assert data is not None, "Either \'table_name\' or \'data\' must be provided."
		if data is None: assert table_name is not None, "Either \'table_name\' or \'data\' must be provided."

		# determine table type if not specified
		if table_name is None and not data is None: table_name = self._identify_table_type(list(data.columns))
		if 'Files' not in self._tables.keys() or table_name not in self._tables.keys():
			logger.error(f"Unknown table name: {table_name}")
			raise ValueError(f"Invalid table name: {table_name}")

		files_table = self.get_table('Files')
		target_table = self.get_table(table_name) if data is None else data

		# Step 1: separate conditions for File table and target table
		files_conditions = {k:v for k,v in conditions.items() if k in files_table.columns}
		target_conditions = {k:v for k,v in conditions.items() if k in target_table.columns}
		invalid_conditions = {k:v for k,v in conditions.items() if (k not in files_conditions) and (k not in target_conditions)}
		if invalid_conditions:
			logger.warning(f"Invalid keywords are being ignored: {invalid_conditions.keys()}")

		# Step 2: filter File table first (if applicable)
		if files_conditions:
			# Apply File table conditions
			for k,v in files_conditions.items():
				# support for range functions like 'lambda x : x <= 4.2'
				if callable(v):
					if isinstance(files_table, dd.DataFrame):
						files_table = files_table[files_table[k].apply(v, meta=(k, 'bool'))]
					else:
						files_table = files_table[files_table[k].apply(v)]
				# support for multiple condition values
				elif isinstance(v, (list, tuple, set, np.ndarray)):	
					files_table = files_table[files_table[k].isin(v)]
				else:
					files_table = files_table[files_table[k] == v]

			# Get matching FILE_IDs
			file_ids = files_table['FILE_ID'].values
			# Filter target table by FILE_IDs
			target_table = target_table[target_table['FILE_ID'].isin(file_ids)]

		# Step 3: apply target table conditions
		if target_conditions:
			for k,v in target_conditions.items():
				# support for range functions like 'lambda x : x <= 4.2'
				if callable(v):
					if isinstance(target_table, dd.DataFrame):
						target_table = target_table[target_table[k].apply(v, meta=(k, 'bool'))]
					else:
						target_table = target_table[target_table[k].apply(v)]
				# support for multiple condition values
				elif isinstance(v, (list, tuple, set, np.ndarray)):	
					target_table = target_table[target_table[k].isin(v)]
				else:
					target_table = target_table[target_table[k] == v]

		return target_table

	def sort(self, sort_columns:List[str], table_name:Optional[str]=None, data:Optional[Union[pd.DataFrame, dd.DataFrame]]=None, ascending:Union[bool, List[bool]]=True) -> Union[pd.DataFrame, dd.DataFrame]:
		"""Sorts the specified table or data based on conditions applied to the 'Files' table and the specified table. *IMPORTANT: Sorting requires loading all specified data into memory. Ensure the data to be sorted is first filtered to only the required subset*.

		Args:
			sort_columns (List[str]): The column names to sort by. Can contain column name in the specified \'table_name\', \'data\', or the \'Files\' table.
			table_name (Optional[str], optional): The name of the table to sort (eg, 'TimeSeries'). If not specified, the table type is automatically determined from the \'data\' schema.
			data (Optional[Union[pd.DataFrame, dd.DataFrame]], optional): The subset of data to sort. If None, the entire table specified by \'table_name\' is sorted *(WARNING: This will load the entire table into memory!)* 
			ascending (Union[bool, List[bool]]=True). Sort order for all or each column in \'sort_columns\'. Defaults to True (ascending for all \'sort_columns\').
		
		Returns:
			Union[pd.DataFrame, dd.DataFrame]: A DataFrame comprising a sorted version of the specified table or data.
		"""

		if table_name is None: assert data is not None, "Either \'table_name\' or \'data\' must be provided."
		if data is None: assert table_name is not None, "Either \'table_name\' or \'data\' must be provided."

		# determine table type if not specified
		if table_name is None and data is None: table_name = self._identify_table_type(list(data.columns))
		if 'Files' not in self._tables.keys() or (table_name is not None and table_name not in self._tables.keys()):
			logger.error(f"Unknown table name: {table_name}")
			raise ValueError(f"Invalid table name: {table_name}")

		files_table = self.get_table('Files')
		target_table = self.get_table(table_name) if data is None else data

		# Step 1: Determine which columns are in the specified data or table_name
		original_columns = target_table.columns
		available_columns = [col for col in sort_columns if col in target_table.columns]
		missing_columns = [col for col in sort_columns if col not in target_table.columns]

		# Step 2: If any columns are missing, check the 'Files' table
		if missing_columns:	
			# Ensure all missing columns exist in the 'Files' table
			for col in missing_columns:
				if col not in files_table.columns:
					raise ValueError(f"Column '{col}' not found in \'data\' or the {f'{table_name} and ' if table_name is not None else ''}'Files' tables.")

			# Merge the original table with 'Files' on FILE_ID
			target_table = target_table.merge(files_table[['FILE_ID'] + missing_columns], on='FILE_ID', how='left')

		# Step 3: If target_table is a dask dataframe, we will need to load it into memory
		if isinstance(target_table, dd.DataFrame):
			# Check if the approx. memory required exceeds the user's limit.
			approx_mem = target_table.memory_usage(deep=True).sum().compute()
			# If so, use set_index(sort=True). This is an approximate sort that doesn't require loading all data in memory at once (still a very expensive operation)
			if approx_mem > MEMORY_LIMIT * 10**9:
				logger.warning(f"Data exceeds in-memory limit ({MEMORY_LIMIT} Gb). The resulting sort is approximate (sorted within partition but not globally).")
				target_table = target_table.set_index(sort_columns, sorted=True)
			# Otherwise, load into memory and sort with sort_values
			else:
				target_table = target_table.compute()
		
		# Pandas df can be sorted with sort_values
		if isinstance(target_table, pd.DataFrame):
			target_table = target_table.sort_values(by=sort_columns, ascending=ascending)

		# Step 4: Drop extra columns from Files table
		target_table = target_table[target_table.columns.intersection(original_columns)]

		return target_table



	def _load_existing_dataset(self):
		# Check that all files exist to load Dataset (see export() method)
		dir_raw_files = self.dir_storage.joinpath("standardized_raw_files")
		
		# Load tables
		dir_tables = self.dir_storage.joinpath("tables")
		for dir_t in [f for f in dir_tables.glob('*') if f.is_dir()]:
			table_name = dir_t.name
			# 'Files' table should always be pandas
			if table_name == 'Files':
				df_files = None
				for f in list(dir_t.glob('*.parquet')):
					if df_files is None: df_files = pd.read_parquet(f)
					else: df_files = pd.concat([df_files, pd.read_parquet(f)], ignore_index=True)
				self._tables[table_name] = df_files
			# Other tables (eg, TimeSeris) should be dask
			else:
				self._tables[table_name] = dd.read_parquet(list(dir_t.glob('*.parquet')))

		# Load dataset config
		file_config = self.dir_storage.joinpath("config.json")
		with open(file_config, "r") as f:
			config_data = json.load(f)
			self._summary = config_data['summary']
			# TODO: updated with future attributes to load

		# Ensure that all raw data files is added to tables
		self._update_table_from_processed_files()
		for test_type in self._tables.keys(): self._update_summary(test_type)

		assert len(list(dir_raw_files.glob('*.parquet'))) == len(self._tables['Files'])

	def _save_config(self, dir_export:Optional[Path]=None):
		if dir_export is None: dir_export = self.dir_storage

		with open(dir_export.joinpath("config.json"), "w") as f:
			json_data = {
				'name':self._name,	
				'summary':self._summary,			
				#'TODO': ADD TO THIS DICT WITH FUTURE DATASET ATTRIBUTES
			}
			json.dump(json_data, f, indent=4)

	def _save_table(self, name:str, dir_export:Optional[Path]=None):
		if dir_export is None: dir_export = self.dir_storage
		dir_table = dir_export.joinpath("tables", name)
		dir_table.mkdir(exist_ok=True, parents=True)
		
		if isinstance(self._tables[name], pd.DataFrame):
			filename = dask_partition_file_naming_fnc(
				partition_index=0, stem=name, file_type='parquet')
			self._tables[name].to_parquet(dir_table.joinpath(filename))
		elif isinstance(self._tables[name], dd.DataFrame):
			# Repartition into ~100MB files
			self._tables[name] = self._tables[name].repartition(partition_size="100MB")

			# Save newly partitioned files
			self._tables[name].to_parquet(
				dir_table, 
				name_function=lambda x: dask_partition_file_naming_fnc(
					partition_index=x, stem=name, file_type='parquet'
				))
						
			# Remove any old files (parititon number greater than current)
			del_files = [f for f in dir_table.glob('*.parquet') \
				if dask_partition_file_naming_sort_fnc(f) > self._tables[name].npartitions-1]
			for f in del_files: os.remove(f)
			
		# Updated config file with test schema
		self._save_config()
		logger.debug(f"Updated cache for the \'{name}\' table. Saved to: {(dir_table)}.")

	def create_table(self, name:str, data:Union[pd.DataFrame, dd.DataFrame], overwrite_existing:bool=False):
		if name in self._tables.keys() and not overwrite_existing:
			logger.error(f"Table (\'{name}\') already exists.")
			raise ValueError(f"Table (\'{name}\') already exists. Use `_update_table()` to add to it.")
		
		if not (isinstance(data, pd.DataFrame) or isinstance(data, dd.DataFrame)):
			logger.error("Data must be a Pandas or Dask Dataframe.")
			raise TypeError("Data must be a Pandas or Dask Dataframe.")

		self._tables[name] = data
		logger.info(f"Table (\'{name}\') successfully added to Dataset.")
		self._save_table(name)

		# Update summary properties
		self._update_summary(name)


	def _update_table(self, name:str, data:Union[pd.DataFrame, dd.DataFrame]):
		# If table doesn't exist, create one
		if name not in self._tables.keys():
			logger.warning(f"Table (\'{name}\') does not exist. One will be created.")
			self.create_table(name, data)
			return
		
		# Type checking
		if not (isinstance(data, pd.DataFrame) or isinstance(data, dd.DataFrame)):
			logger.error("Data must be a Pandas or Dask Dataframe.")
			raise TypeError("Data must be a Pandas or Dask Dataframe.")
		if not type(data) == type(self._tables[name]):
			logger.error(f"New data does not match existing data type: {type(data)} != {type(self._tables[name])}.")
			raise TypeError(f"New data must match the existing data type: {type(data)} != {type(self._tables[name])}.")
		
		# Update existing table
		if isinstance(data, pd.DataFrame):
			self._tables[name] = pd.concat([self._tables[name], data], axis=0, ignore_index=True)
			logger.info(f"New data successfully added to table (\'{name}\').")
		elif isinstance(data, dd.DataFrame):
			self._tables[name] = dd.concat([self._tables[name], data], axis=0, ignore_index=True)
			logger.info(f"New data successfully added to table (\'{name}\').")

		# Update cached table
		self._save_table(name)

		# Update summary properties
		self._update_summary(name)
		return

	def _update_table_from_processed_files(self, force_update:bool=False):
		# Check that 'Files' table exists
		if 'Files' not in self._tables.keys():
			logger.error("Failed to update table from processed data. \'Files\' table does not exist.")
			raise ValueError("The \'Files\' table does not exist. You must run `add_files` first.")
			
		# For each test type, get files that haven't been added
		for test_type in self._tables['Files']['TEST_TYPE'].unique():
			files_to_add = None
			if test_type not in self._tables.keys() or force_update:		# update all files for this test_type
				files_to_add = self._tables['Files'].loc[
					(self._tables['Files']['TEST_TYPE'] == test_type),
					['FILE_ID', 'CELL_ID', 'FILENAME']].copy()
			else:
				files_to_add = self._tables['Files'].loc[					# only update new FILE_IDs
					(self._tables['Files']['TEST_TYPE'] == test_type) & \
					(~self._tables['Files']['FILE_ID'].isin(self._tables[test_type]['FILE_ID'].compute().values)),
					['FILE_ID', 'CELL_ID', 'FILENAME']].copy()
				
			if len(files_to_add) > 0:
				files_to_add['FILENAME_STANDARDIZED'] = files_to_add['FILENAME'].apply(lambda f: f"{Path(f).stem}.parquet")
				# For each row in files_to_add, read the file to dask dataframe and assign the file_id index
				ddfs = [dd.read_parquet(
					self.dir_storage.joinpath("standardized_raw_files", row.FILENAME_STANDARDIZED)).assign(
						FILE_ID=row.FILE_ID,
						CELL_ID=row.CELL_ID
					) for row in files_to_add.itertuples(index=False)]
				# Concatenate all DataFrames
				ddf = dd.concat(ddfs)
				reordered_keys = ['FILE_ID', 'CELL_ID'] + [k for k in ddf.columns if k not in ['FILE_ID', 'CELL_ID']]
				ddf = ddf[reordered_keys]
				self._update_table(test_type, ddf)
		
		return

	def _update_summary(self, summary_type:str):
		"""Updates the specified summary type 

		Args:
			type (str): {'Files' or table name}
		"""
		logger.info(f"Generating summary for Table (\'{summary_type}\').")

		# Dataset summary
		if summary_type == 'Files':
			df_files = self.get_table("Files")

			files_summary = {
				'NUM_FILES':{
					'description':'Number of files', 
					'value':len(df_files),							},
				'NUM_CELLS':{
					'description':'Number of cells', 
					'value':len(df_files['CELL_ID'].unique()),		},
				'NUM_PROTOCOLS':{
					'description':'Number of unique protocols', 
					'value':len(df_files['PROTOCOL'].unique()),		},
				'PROTOCOLS':{
					'description':'A list of unique protoypes', 
					'value':list(df_files['PROTOCOL'].unique()),			},
				'NUM_TEST_TYPES':{
					'description':'Number of test types', 
					'value':len(df_files['TEST_TYPE'].unique()),	},
				'TEST_TYPES':{
					'description':'A list of unique test types', 
					'value':list(df_files['TEST_TYPE'].unique()),			},
			}
			if 'LABEL' in df_files.columns:
				files_summary['CUSTOM_LABEL'] = {
					'description':'A list of user-defined file labels', 
					'value':list(df_files['LABEL'].unique()),			}
			self._summary[summary_type] = files_summary

		# TimeSeries
		elif summary_type == 'TimeSeries':
			# Cell Summary - TimeSeries
			df_files = self.get_table("Files")
			ddf = self.get_table('TimeSeries')

			time_series_summary = {}
			for cell_id in ddf['CELL_ID'].unique().compute():  # Compute only unique cell IDs
				ddf_cell = ddf[ddf['CELL_ID'] == cell_id]

				num_cycles = ddf_cell.groupby('FILE_ID')['CYCLE_NUMBER'].max().sum().compute()
				current_stats = ddf_cell.groupby('FILE_ID')['CURRENT_A'].agg(['max', 'min']).compute()
				current_max = current_stats['max'].max()
				current_min = current_stats['min'].min()
				voltage_stats = ddf_cell.groupby('FILE_ID')['VOLTAGE_V'].agg(['max', 'min']).compute()
				voltage_max = voltage_stats['max'].max()
				voltage_min = voltage_stats['min'].min()
				
				# Compute capacity-related values
				def get_max_q_delta(df_gb:pd.DataFrame) -> float:
					q_throughput = 0
					q_delta_max = 0

					# Take cumulative capacity within each file
					q_steps = [0]
					for _, df_ggb in df_gb.groupby(['CYCLE_NUMBER', 'STEP_NUMBER', 'STEP_MODE']):
						last_capacity = df_ggb['STEP_CAPACITY_AH'].values[-1]
						q_steps.append(last_capacity)
						q_throughput += df_ggb['STEP_CAPACITY_AH'].abs().max()

					# Record maximum difference in cumulative capacity
					q_cum = np.cumsum(q_steps)
					q_delta_max = max(q_cum) - min(q_cum)

					# Wrap in Series
					return pd.Series({"q_delta_max": q_delta_max, "q_throughput": q_throughput})  
				
				gb_res = (ddf_cell.groupby(["FILE_ID"]).apply(get_max_q_delta, meta={"q_delta_max": "f8", "q_throughput": "f8"})).compute()
				q_delta_max = gb_res['q_delta_max'].max()
				q_throughput = gb_res['q_throughput'].sum()

				# Time under test calculations
				start_time = df_files.loc[df_files['CELL_ID'] == cell_id, 'DATETIME_START'].min()
				end_time = df_files.loc[df_files['CELL_ID'] == cell_id, 'DATETIME_END'].max()

				time_under_test = 'UNDEFINED'
				try:
					time_under_test = (end_time - start_time).days
					start_time = start_time.isoformat()
					end_time = end_time.isoformat()
				except:
					pass 

				# Store summary
				time_series_summary[int(cell_id)] = {
					'TEST_TIME_START': start_time,
					'TEST_TIME_END': end_time,
					'TIME_UNDER_TEST_DAYS': time_under_test,
					'NUM_CYCLES': int(num_cycles),
					'CAPACITY_CYCLE_DELTA_AH': float(q_delta_max),
					'CURRENT_MAX_A': float(current_max),
					'CURRENT_MIN_A': float(current_min),
					'CURRENT_THROUGHPUT_AH': float(q_throughput),
					'VOLTAGE_MAX_V': float(voltage_max),
					'VOLTAGE_MIN_V': float(voltage_min),
				}

			self._summary[summary_type] = time_series_summary

		# Frequency:
		elif summary_type == 'Frequency':
			# TODO:
			raise RuntimeError("NOT IMPLEMENTED YET.")

		else:
			logger.warning("Unknown table type. No summary will be provided.")




def create_dataset(name:str, dir_storage:Path, overwrite_existing:bool=False) -> Dataset:
    """Creates a new Dataset instance

    Args:
        name (str): Provide a name for the dataset
        dir_storage (Path): Provide a folder for where this dataset should be stored. 
        overwrite_existing (bool, optional): Whether to override an existing dataset with the same name at the provided directory. Defaults to False.

    Returns:
        Dataset: A new Dataset instance.
    """
    return Dataset(name=name, dir_storage=dir_storage, overwrite_existing=overwrite_existing)

def load_dataset(dir_dataset:Path) -> Dataset:
    """Loads an existing Dataset instance

    Args:
        dir_dataset (Path): Head directory of the stored Dataset instance.

    Returns:
        Dataset: _description_
    """

    if not dir_dataset.is_dir():
        logger.error(f"Path is not a directory: {dir_dataset}")
        raise TypeError(f"The provided path is not a directory: {dir_dataset}")
    file_config = dir_dataset.joinpath("config.json")
    if not file_config.exists():
        logger.error(f"Dataset does not contain a config.json file.")
        raise FileNotFoundError("Could not find a config.json file in this directory.")

    with open(file_config, "r") as f:
        config_data = json.load(f)
        name = config_data['name']

    return Dataset(name=name, dir_storage=dir_dataset.parent)


