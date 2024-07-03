""" Constants file for Roche Cedex HiRes Parser"""

# Instrument Software Details
CEDEX_SOFTWARE = "Cedex software"
MODEL_NUMBER = "Cedex HiRes"
BRAND_NAME = "Cedex"
PRODUCT_MANUFACTURER = "Roche"
DEVICE_TYPE = "cell counter"
DISPLAY_NAME = "Roche Cedex HiRes"
DETECTION_TYPE = "brightfield"

# Errors
MULTIPLE_SYSTEM_ERROR = "Data is extracted from multiple systems and have different system parameters. Expected exactly one value for: "
VALUE_ERROR = "Unable to find value for column"
UNSUPPORTED_FILE_FORMAT_ERROR = (
    "Unsupported file format. Expected xlsx or csv file. Actual: "
)
