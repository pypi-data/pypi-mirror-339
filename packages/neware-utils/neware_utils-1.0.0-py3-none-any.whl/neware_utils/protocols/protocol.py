

import xml.etree.ElementTree as ET
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field

from neware_utils.protocols.step_modes import NewareStep, END


@dataclass
class Protocol:
    builder_name: str
    protocol_description: str

    version:int = 17                                                    # TODO: not sure what this version refers to
    bts_client_version:str = "BTS Client 8.0.0.478(2024.06.24)(R3)"
    guid:str = "5b93f8b6-71f5-49bc-a83b-0bbe6087903e"                   # TODO: not sure what this is? BTS Client GUI version?

    steps: Dict[int, "NewareStep"] = field(default_factory=dict)

    record_attr: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None
    protection_attr: Optional[Dict[str, Dict[str, Dict[str, float]]]] = None


    def add_step(self, step:"NewareStep"):
        """Adds a NewareStep object to the protocol."""
        if not isinstance(step, NewareStep):
            raise TypeError("Only instances of NewareStep can be added.")

        cur_step_num = len(self.steps) + 1
        step.step_num = cur_step_num
        self.steps[cur_step_num] = step

    def set_protection_limits(self, property:str, lower_limit:Optional[float]=None, upper_limit:Optional[float]=None, where:str='main'):
        """Sets a protection limit to the specified property.

		Args:
			property (str): {'voltage', 'curent', 'temperature'}. 
			lower_limit (optional, float): Lower limit value. Units are in {'voltage':volts, 'current':amps, 'temperature':celsius}.
            upper_limit (optional, float): Upper limit value. Units are in {'voltage':volts, 'current':amps, 'temperature':celsius}.
            where (optional, str): {'main', 'aux'}. Where the protection is applied (ie, to the main or auxilliary measurements). Defaults to 'main'.
		"""
        xml_tag_mapping = {
            'voltage':'Volt',
            'current':'Curr',
            'temperature':'Temp'
        }

        if not property in xml_tag_mapping.keys(): raise ValueError(f"`property` must be one of the following: {list(xml_tag_mapping.keys())}")
        if lower_limit is None and upper_limit is None: raise ValueError(f'Lower and upper limits are None.')

        if not self.protection_attr: self.protection_attr = {}

        if where == 'main':
            if not 'Main' in self.protection_attr: self.protection_attr['Main'] = {}
            if property == 'temperature': raise ValueError("Temperature limits must be set to the auxilliary. Run with `where='aux'`")
            if not xml_tag_mapping[property] in self.protection_attr['Main']: self.protection_attr['Main'][xml_tag_mapping[property]] = {}
        
            if lower_limit: self.protection_attr['Main'][xml_tag_mapping[property]]['Lower'] = lower_limit
            if upper_limit: self.protection_attr['Main'][xml_tag_mapping[property]]['Upper'] = upper_limit

        elif where == 'aux':
            if not 'Aux' in self.protection_attr: self.protection_attr['Aux'] = {}
            if not xml_tag_mapping[property] in self.protection_attr['Aux']: self.protection_attr['Aux'][xml_tag_mapping[property]] = {}

            if lower_limit: self.protection_attr['Aux'][xml_tag_mapping[property]]['Lower'] = lower_limit
            if upper_limit: self.protection_attr['Aux'][xml_tag_mapping[property]]['Upper'] = upper_limit

        else:
            raise ValueError(f"Unknown value for `where`: {where}")

    def set_sampling_intervals(self, property:str, value:float, where:str='main'):
        """Sets the sampling interval for the given change in property. 

        Args:
			property (str): {'time', 'voltage', 'curent', 'temperature'}. 
			value (float): Sampling interval. Units are in {'time':seconds, 'voltage':volts, 'current':amps, 'temperature':celsius}.
            where (optional, str): {'main', 'aux'}. Where the protection is applied (ie, to the main or auxilliary measurements). Defaults to 'main'.
		"""

        xml_tag_mapping = {
            'time':'Time',
            'voltage':'Volt',
            'current':'Curr',
            'temperature':'Temp'
        }

        if not property in xml_tag_mapping.keys(): raise ValueError(f"`property` must be one of the following: {list(xml_tag_mapping.keys())}")
        if not self.record_attr: self.record_attr = {}
        if where == 'main':
            if not 'Main' in self.record_attr: self.record_attr['Main'] = {}
            if property == 'temperature': raise ValueError("Temperature intervals must be set on the auxilliary measurements. Run with `where='aux'`")
            self.record_attr['Main'][xml_tag_mapping[property]] = value
        elif where == 'aux':
            if not 'Aux' in self.record_attr: self.record_attr['Aux'] = {}
            self.record_attr['Aux'][xml_tag_mapping[property]] = value


    def is_valid(self) -> bool:
        """Checks whether the current protocol is valid."""

        #region: check unique step numbers
        if not len(self.steps) == len(np.unique(list(self.steps.keys()))):
            raise ValueError(f"Duplicate step numbers found: {list(self.steps.keys())}")
        #endregion

        #region: check min,max setpoints
        max_voltage_setpoint = None
        min_voltage_setpoint = None
        max_current_setpoint = None
        min_current_setpoint = None
        for step_num, step in self.steps.items():
            if step.main_attributes:
                max_voltage_setpoint = np.max(
                    np.hstack([
                        val for val in [
                            step.main_attributes.get('Stop_Volt'),
                            step.main_attributes.get('Volt'),
                            max_voltage_setpoint
                        ] if val is not None
                    ])
                )
                min_voltage_setpoint = np.min(
                    np.hstack([
                        val for val in [
                            step.main_attributes.get('Stop_Volt'),
                            step.main_attributes.get('Volt'),
                            min_voltage_setpoint
                        ] if val is not None
                    ])
                )
                max_current_setpoint = np.max(
                    np.hstack([
                        val for val in [
                            step.main_attributes.get('Stop_Curr'),
                            step.main_attributes.get('Curr'),
                            max_current_setpoint
                        ] if val is not None
                    ])
                )
                min_current_setpoint = np.min(
                    np.hstack([
                        val for val in [
                            step.main_attributes.get('Stop_Curr'),
                            step.main_attributes.get('Curr'),
                            min_current_setpoint
                        ] if val is not None
                    ])
                )
                
        if self.protection_attr and self.protection_attr['Main']:
            try:
                if not self.protection_attr['Main']['Volt']['Lower'] and min_voltage_setpoint < float(self.protection_attr['Main']['Volt']['Lower']):
                    raise ValueError(f"Minimum step voltage exceeds lower protection limit: {min_voltage_setpoint} < {self.protection_attr['Main']['Volt']['Lower']}")
            except KeyError:
                pass
            try:
                if not self.protection_attr['Main']['Volt']['Upper'] and max_voltage_setpoint > float(self.protection_attr['Main']['Volt']['Upper']):
                    raise ValueError(f"Maximum step voltage exceeds upper protection limit: {max_voltage_setpoint} > {self.protection_attr['Main']['Volt']['Upper']}")
            except KeyError:
                pass
                
            try:
                if not self.protection_attr['Main']['Curr']['Lower'] and min_current_setpoint < float(self.protection_attr['Main']['Curr']['Lower']):
                    raise ValueError(f"Minimum step current exceeds lower protection limit: {min_current_setpoint} < {self.protection_attr['Main']['Curr']['Lower']}")
            except KeyError:
                pass
            try:
                if not self.protection_attr['Main']['Curr']['Upper'] and max_current_setpoint > float(self.protection_attr['Main']['Curr']['Upper']):
                    raise ValueError(f"Maximum step current exceeds upper protection limit: {max_current_setpoint} > {self.protection_attr['Main']['Curr']['Upper']}")
            except KeyError:
                pass
        #endregion

        # check that protocol ends with END step
        last_step = self.steps[len(self.steps)]
        if not isinstance(last_step, END): raise ValueError("Protocol does not have an 'END' step.")

        # check that step IDs have been set
        for step_id, step in self.steps.items():
            self.steps[step_id].step_num = step_id

        # check that record sampling has been set
        if not self.record_attr: 
            raise ValueError('No sampling interval has been set. You must have at least one sampling definition \
                             (eg, `set_sampling_intervals(\'time\', 30, \'main\')`)')
        return True


    def to_xml(self) -> ET.Element:
        """Converts the protocol steps into an XML structure."""

        try:
            self.is_valid()
        except Exception as e:
            raise RuntimeError(f"Protocol is invalid: {e}")


        root = ET.Element("root")

        #region: define "config"
        config = ET.SubElement(
            root, 
            "config", 
            type="Step File",
            version=str(self.version),
            client_version=str(self.bts_client_version),
            date=datetime.today().strftime("%Y%m%d%H%M%S"),
            Guid=str(self.guid)
        )
        #endregion

        #region: define "Head_Info"
        head_info = ET.SubElement(
            config,
            "Head_Info"
        )
        head_info_subelements = {
            "Operate": {"Value": "66"},
            "Scale": {"Value": "1"},
            "Start_Step": {"Value": "1", "Hide_Ctrl_Step": "0"},
            "Creator": {"Value": self.builder_name},
            "Remark": {"Value": self.protocol_description},
            "RateType": {"Value": "103"},       # TODO: add support for C-rate mode: {"Value": "105" if c_rate_mode else "103"}, 
            "MultCap": {"Value": "3600000"}     # TODO: {"Value": str(int(c_rate_capacity * 3600000)) if c_rate_mode else "3600000"}
        }
        for tag, attr in head_info_subelements.items():
            ET.SubElement(head_info, tag, attr)
        #endregion

        #region: define "Whole_Prt"
        whole_prt = ET.SubElement(
            config,
            "Whole_Prt"
        )
        protect = ET.SubElement(
            whole_prt,
            "Protect"
        )
        for el_key in ['Main', 'Aux']:
            if not el_key in self.protection_attr: continue
            el = ET.SubElement(
                protect,
                el_key
            )
            for tag in self.protection_attr[el_key].keys():

                if tag == 'Temp':
                    # Neware uses different format for temperature (no idea why)
                    for sub_tag, sub_attr in self.protection_attr[el_key][tag].items():
                        ET.SubElement(
                            el, 
                            'Step_TempL' if sub_tag == 'Lower' else 'Step_TempH',
                            Value=str(int(float(sub_attr)*10))
                        )
                else:
                    sub_el = ET.SubElement(
                        el,
                        tag
                    )
                    
                    multiplier = None
                    if tag == 'Volt': multiplier = 10000
                    elif tag == 'Curr': multiplier = 1000
                    else: raise ValueError(f"Unknown protection tag: {tag}.")

                    for sub_tag, sub_attr in self.protection_attr[el_key][tag].items():
                        ET.SubElement(sub_el, sub_tag, Value=str(int(float(sub_attr)*multiplier)))

        record = ET.SubElement(
            whole_prt,
            "Record"
        )
        for el_key in ['Main', 'Aux']:
            if not el_key in self.record_attr: continue
            el = ET.SubElement(
                record,
                el_key
            )
            for tag, val in self.record_attr[el_key].items():
                multiplier = None
                if tag == 'Volt': multiplier = 10000
                elif tag == 'Curr': multiplier = 1000
                elif tag == 'Temp': multiplier = 10
                elif tag == 'Time': multiplier = 1000
                else: raise ValueError(f"Unknown record tag: {tag}.")

                ET.SubElement(el, tag, Value=str(int(float(val)*multiplier)))
        #endregion

        #region: define "Step_Info"
        step_info = ET.SubElement(
            config,
            "Step_Info",
            Num=str(len(self.steps)),
        )
        for step_id in sorted(self.steps.keys()):
            step_info.append(self.steps[step_id].to_xml())
        #endregion

        #region: define "SMBUS" (TODO)
        smbus = ET.SubElement(
            config,
            "SMBUS"
        )
        ET.SubElement(smbus, "SMBUS_Info", Num="0", AdjacentInterval="0")
        #endregion

        return root
    
    def export(self, filepath:Path):
        """Exports the current protocol to the defined filepath."""
        if not filepath.suffix.lower() == '.xml':
            filepath.suffix = '.xml'

        tree = ET.ElementTree(self.to_xml())
        with open(filepath, "wb") as file:
            tree.write(file, encoding="GB2312")





