from typing import List

SENSOR_TYPE: List[List[str]] = [
    ["Monochrome", "Camera produces monochrome array with no Bayer encoding"],
    ["Colour",
     "Camera produces color image directly, requiring not Bayer decoding"],
    ["RGGB", "Camera produces RGGB encoded Bayer array images"],
    ["CMYG", "Camera produces CMYG encoded Bayer array images"],
    ["CMYG2", "Camera produces CMYG2 encoded Bayer array images"],
    ["LRGB", "Camera produces Kodak TRUESENSE Bayer LRGB array images"]

]

STATUS_CODES: List[str] = [
    "CameraIdle At idle state, available to start exposure",
    "CameraWaiting Exposure started but waiting "
    "(for shutter, trigger, filter wheel, etc.)",
    "CameraExposing Exposure currently in progress",
    "CameraReading CCD array is being read out (digitized)",
    "CameraDownload Downloading data to PC",
    "CameraError Camera error condition serious enough to prevent "
    "further operations (connection fail, etc.)."
]
