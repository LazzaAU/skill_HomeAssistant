import sqlite3
from pathlib import Path
from typing import Optional

from core.device.model.Device import Device
from skills.HomeAssistant.HomeAssistant import HomeAssistant
from core.device.model.DeviceAbility import DeviceAbility


class HAswitch(Device):

	@classmethod
	def getDeviceTypeDefinition(cls) -> dict:
		return {
			'deviceTypeName'        : 'HAswitch',
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
		iconPath = self.selectIconBasedOnState()

		if Path(iconPath).exists():
			icon = iconPath
		else:
			icon = Path(f"{self._imagePath}Switches/HAswitch.png")

		return super().getDeviceIcon(icon)


	def onUIClick(self):

		# Display default icons
		if self.getParam(key='state') == "on":
			self.updateParam(key='state', value='off')
			self.updateStateOfDeviceInHA()

		elif self.getParam(key='state') == "off":
			self.updateParam(key='state', value='on')
			self.updateStateOfDeviceInHA()

		else:
			self.logInfo("Sorry but it appears that switch is currently unavailable")

		return super().onUIClick()


	def updateStateOfDeviceInHA(self):
		""" Sends uid to HomeAssistant skill which then sends the command over
			API to HomeAssistant to turn on or off the device
		"""
		haClass = HomeAssistant()
		haClass.deviceClicked(uid=self.uid)


	def selectIconBasedOnState(self):
		return Path(f"{self._imagePath}Switches/{self.getParam('entityGroup')}{str(self.getParam('state')).capitalize()}.png")

