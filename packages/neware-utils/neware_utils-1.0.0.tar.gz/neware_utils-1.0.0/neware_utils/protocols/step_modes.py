from dataclasses import dataclass, field
from typing import Optional, Dict, Type, Union
from numbers import Number
import xml.etree.ElementTree as ET


@dataclass
class NewareStep:
	step_name: str
	step_type: int      # Unique identifier (Neware-defined)
	step_num: Optional[int] = 0
	
	main_attributes: Optional[dict] = None
	other_attributes: Optional[dict] = None

	def to_xml(self) -> ET.Element:
		"""Returns an XML ElementTree.Element object representing the given step. \n

		Returns:
			ET.Element: XML Element describing the current step.
		"""

		step_el = ET.Element(f"Step{int(self.step_num)}", Step_ID=str(int(self.step_num)), Step_Type=str(int(self.step_type)))
		if self.main_attributes or self.other_attributes:
			limit_el = ET.SubElement(
				step_el,
				"Limit",
			)
			if self.main_attributes:
				main_el = ET.SubElement(
					limit_el,
					"Main"
				)
				for tag, attr in self.main_attributes.items():
					ET.SubElement(main_el, tag, Value=str(int(attr) if isinstance(attr, Number) else attr))
			if self.other_attributes:
				other_el = ET.SubElement(
					limit_el,
					"Other"
				)
				for tag, attr in self.other_attributes.items():
					ET.SubElement(other_el, tag, Value=str(int(attr) if isinstance(attr, Number) else attr))

		return step_el


@dataclass
class CC_CHG(NewareStep):
	# current_A:float						# charge current (in amps)
	# cutoff_voltage_V:Optional[float]	# cutoff voltage
	# cutoff_time_s:Optional[float]		# step duration (in seconds)

	@classmethod
	def create(cls, current:float, cutoff_voltage:Optional[float]=None, step_duration:Optional[float]=None) -> "CC_CHG":
		"""Creates a constant current charge step (CC CHG)

		Args:
			current (float): Charge current (in amps)
			cutoff_voltage (Optional[float], optional): Optional cutoff voltage (in voltage). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_voltage`. Defaults to None.

		Returns:
			CC_CHG: Constant current charge step
		"""

		if cutoff_voltage is None and step_duration is None: raise ValueError("At least one of `cutoff_voltage` and `step_duration` must be defined.")

		main_attr = {'Curr':current * 1000,}
		if cutoff_voltage:
			main_attr['Stop_Volt'] = cutoff_voltage * 10000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CC CHG", 
			step_type=1, 
			main_attributes=main_attr
		)

@dataclass
class CC_DCHG(NewareStep):
	# current_A:float						# discharge current (in amps)
	# cutoff_voltage_V:Optional[float]	# cutoff voltage
	# cutoff_time_s:Optional[float]		# step duration (in seconds)

	@classmethod
	def create(cls, current:float, cutoff_voltage:Optional[float]=None, step_duration:Optional[float]=None) -> "CC_DCHG":
		"""Creates a constant current discharge step (CC DCHG)

		Args:
			current (float): Discharge current (in amps)
			cutoff_voltage (Optional[float], optional): Optional cutoff voltage (in voltage). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_voltage`. Defaults to None.

		Returns:
			CC_DCHG: Constant current discharge step
		"""

		if cutoff_voltage is None and step_duration is None: raise ValueError("At least one of `cutoff_voltage` and `step_duration` must be defined.")

		main_attr = {'Curr':current * 1000,}
		if cutoff_voltage:
			main_attr['Stop_Volt'] = cutoff_voltage * 10000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CC DCHG", 
			step_type=2, 
			main_attributes=main_attr
		)
	
@dataclass
class CV_CHG(NewareStep):
	# current_A:float						# charge current (in amps)
	# voltage_V:float						# charge voltage (in volts)

	# cutoff_current_A:Optional[float]	# cutoff current (in amps)
	# cutoff_time_s:Optional[float]		# step duration (in seconds)


	@classmethod
	def create(cls, current:float, voltage:float, cutoff_current:Optional[float]=None, step_duration:Optional[float]=None) -> "CV_CHG":
		"""Creates a constant voltage charge step (CV CHG)

		Args:
			current (float): Charge current (in amps)
			voltage (float): Charge voltage (in volts)
			cutoff_current (Optional[float], optional): Optional cutoff current (in amp). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_current`. Defaults to None.

		Returns:
			CV_CHG: Constant voltage charge step
		"""

		if cutoff_current is None and step_duration is None: raise ValueError("At least one of `cutoff_current` and `step_duration` must be defined.")

		main_attr = {
			'Curr':current * 1000,
			'Volt':voltage * 10000}
		if cutoff_current:
			main_attr['Stop_Curr'] = cutoff_current * 1000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CV CHG", 
			step_type=3, 
			main_attributes=main_attr
		)
	
@dataclass
class CV_DCHG(NewareStep):
	# current_A:float						# discharge current (in amps)
	# voltage_V:float						# discharge voltage (in volts)

	# cutoff_current_A:Optional[float]	# cutoff current (in amps)
	# cutoff_time_s:Optional[float]		# step duration (in seconds)


	@classmethod
	def create(cls, current:float, voltage:float, cutoff_current:Optional[float]=None, step_duration:Optional[float]=None) -> "CV_DCHG":
		"""Creates a constant voltage discharge step (CV DCHG)

		Args:
			current (float): Discharge current (in amps)
			voltage (float): Discharge voltage (in volts)
			cutoff_current (Optional[float], optional): Optional cutoff current (in amps). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_current`. Defaults to None.

		Returns:
			CV_DCHG: Constant voltage discharge step
		"""

		if cutoff_current is None and step_duration is None: raise ValueError("At least one of `cutoff_current` and `step_duration` must be defined.")

		main_attr = {
			'Curr':current * 1000,
			'Volt':voltage * 10000}
		if cutoff_current:
			main_attr['Stop_Curr'] = cutoff_current * 1000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CV DCHG", 
			step_type=19, 
			main_attributes=main_attr
		)

@dataclass
class CCCV_CHG(NewareStep):
	# current_A:float						# charge current (in amps)
	# voltage_V:float						# charge voltage (in volts)

	# cutoff_current_A:Optional[float]	# cutoff current (in amps)
	# cutoff_time_s:Optional[float]		# step duration (in seconds)

	@classmethod
	def create(cls, current:float, voltage:float, cutoff_current:Optional[float]=None, step_duration:Optional[float]=None) -> "CCCV_CHG":
		"""Creates a constant-current constant-voltage charge step (CCCV CHG)

		Args:
			current (float): Charge current (in amps)
			voltage (float): Charge voltage (in volts)
			cutoff_current (Optional[float], optional): Optional cutoff current (in amp). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_current`. Defaults to None.

		Returns:
			CCCV_CHG: Constant-current constant-voltage charge step
		"""

		if cutoff_current is None and step_duration is None: raise ValueError("At least one of `cutoff_current` and `step_duration` must be defined.")

		main_attr = {
			'Curr':current * 1000,
			'Volt':voltage * 10000}
		if cutoff_current:
			main_attr['Stop_Curr'] = cutoff_current * 1000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CCCV CHG", 
			step_type=7, 
			main_attributes=main_attr
		)
	
@dataclass
class CCCV_DCHG(NewareStep):
	# current_A:float						# discharge current (in amps)
	# voltage_V:float						# discharge voltage (in volts)

	# cutoff_current_A:Optional[float]	# cutoff current (in amps)
	# cutoff_time_s:Optional[float]		# step duration (in seconds)

	@classmethod
	def create(cls, current:float, voltage:float, cutoff_current:Optional[float]=None, step_duration:Optional[float]=None) -> "CCCV_DCHG":
		"""Creates a constant-current constant-voltage discharge step (CCCV DCHG)

		Args:
			current (float): Discharge current (in amps)
			voltage (float): Discharge voltage (in volts)
			cutoff_current (Optional[float], optional): Optional cutoff current (in amp). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_current`. Defaults to None.

		Returns:
			CCCV_DCHG: Constant-current constant-voltage discharge step
		"""

		if cutoff_current is None and step_duration is None: raise ValueError("At least one of `cutoff_current` and `step_duration` must be defined.")

		main_attr = {
			'Curr':current * 1000,
			'Volt':voltage * 10000}
		if cutoff_current:
			main_attr['Stop_Curr'] = cutoff_current * 1000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CCCV DCHG", 
			step_type=20, 
			main_attributes=main_attr
		)
	
@dataclass
class CYCLE(NewareStep):
	# start_step: int
	# num_cycles: int
	
	@classmethod
	def create(cls, start_step:int, num_cycles:int) -> "CYCLE":
		"""Creates a cycle step (CYCLE)

		Args:
			start_step (int): Step ID where cycle starts
			num_cycles (int): Number of cycles to perform.

		Returns:
			CYCLE: Cycle step
		"""
		other_attr = {
			'Start_Step':start_step,
			'Cycle_Count':num_cycles
		}
		return cls(
			step_name="CYCLE", 
			step_type=5, 
			other_attributes=other_attr
		)

@dataclass
class REST(NewareStep):
	# cutoff_time_s:Optional[float]		# step duration (in seconds)

	@classmethod
	def create(cls, step_duration:float) -> "REST":
		"""Creates a rest step (REST)

		Args:
			step_duration (float): Step duration (in seconds).

		Returns:
			REST: Rest step
		"""

		main_attr = {'Time':step_duration * 1000,}
		return cls(
			step_name="REST", 
			step_type=4, 
			main_attributes=main_attr
		)

@dataclass
class PAUSE(NewareStep):
	@classmethod
	def create(cls) -> "PAUSE":
		"""Creates a pause step (PAUSE)

		Returns:
			PAUSE: Pause step
		"""

		return cls(
			step_name="PAUSE", 
			step_type=13,
		)
	
@dataclass
class END(NewareStep):
	@classmethod
	def create(cls) -> "END":
		"""Creates a end step (END)

		Returns:
			END: End step
		"""

		return cls(
			step_name="END", 
			step_type=6,
		)
	
