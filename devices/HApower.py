import sqlite3
from typing import Optional

from core.device.model.Device import Device
from pathlib import Path
from core.device.model.DeviceAbility import DeviceAbility


class HApower(Device):

	@classmethod
	def getDeviceTypeDefinition(cls) -> dict:
		return {
			'deviceTypeName'        : 'HApower',
			'perLocationLimit'      : 0,
			'totalDeviceLimit'      : 0,
			'allowLocationLinks'    : True,
			'allowHeartbeatOverride': True,
			'heartbeatRate'         : 320,
			'abilities'             : [DeviceAbility.NONE]
		}


	def __init__(self, data: sqlite3.Row):
		self._imagePath = f'{self.Commons.rootDir()}/skills/HomeAssistant/devices/img/'
		super().__init__(data)


	def getDeviceIcon(self, path: Optional[Path] = None) -> Path:
		powerType = self.getParam('entityName').split('_')[-1]

		if powerType == "current":
			icon = Path(f'{self._imagePath}GeneralSensors/HAcurrent.png')
		elif powerType == "voltage":
			icon = Path(f'{self._imagePath}GeneralSensors/HAvoltage.png')
		elif powerType == "power" or powerType == 'battery':
			icon = Path(f'{self._imagePath}GeneralSensors/battery.png')
		else:
			icon = Path(f'{self._imagePath}GeneralSensors/HAsensor.png')

		return super().getDeviceIcon(icon)


	def onUIClick(self):

		answer = f"The {self.displayName} has a reading of {self.getParam('state')}"
		self.MqttManager.say(text=answer)
		return super().onUIClick()
