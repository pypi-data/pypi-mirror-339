
from battkit.dataset.test_schema import TestSchema, logger

class FrequencySchema(TestSchema):
	def __init__(self, test_name, required_schema, optional_schema = None):
		test_name = 'Frequency'
		raise RuntimeError("Not implemented yet")
		required_schema = None
		optional_schema = None
		super().__init__(test_name, required_schema, optional_schema)
	