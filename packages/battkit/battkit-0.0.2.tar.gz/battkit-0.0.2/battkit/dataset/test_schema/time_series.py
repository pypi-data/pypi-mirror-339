

from typing import Dict, Type, List
from battkit.dataset.test_schema import TestSchema, logger


class TimeSeriesSchema(TestSchema):
	step_modes = [
		'CC CHG', 'CV CHG', 'CCCV CHG', 'CC DCHG', 'CV DCHG', 'CCCV DCHG',
		'CP CHG', 'CP DCHG', 'CR DCHG', 'REST',
		'UNDEFINED'
	]
	def __init__(self):
		test_name = 'TimeSeries'
		required_schema = {
			'RECORD_NUMBER':int, 					# unique for each sampled point (natural number)
			'TIME_S':float,                       # test time (in seconds)
			'CYCLE_NUMBER':int,                     # unique for each cycle number in protocol (natural number)
			'STEP_NUMBER':int, 						# unique for each step number in protocol (natural number)
			'STEP_MODE':str,						# see supported step modes below
			'VOLTAGE_V':float,					# cell voltage (in volts)
			'CURRENT_A':float,					# applied current (positive if charge step, negative if discharge step)
			'STEP_CAPACITY_AH':float,				# cumulative capacity since start of step number (can be negative)
		}
		optional_schema = {
			'CELL_TEMPERATURE_C':float,			# cell temperature (in deg C)
			'AMBIENT_TEMPERATURE_C':float, 		# ambient temperature (in deg C)
		}
		super().__init__(test_name, required_schema, optional_schema)

	def validate_data(self, data_schema:Dict[str, Type]) -> bool:
		# This subclass method allows for custom validation to be performed in addition to 
		# the direct schema validation that is performed in super()._validate_data() 
		if not super()._validate_data(data_schema): 
			return False
		
		return True
	
	def validate_step_mode(self, step_modes:List[str]):
		invalid_modes = [m for m in step_modes if m not in self.step_modes]

		if invalid_modes:
			logger.error(f"Data validation failed. Invalid step modes found: {invalid_modes}")
		else:
			logger.info(f"Step mode validation successful.")
			return True
		
		return False