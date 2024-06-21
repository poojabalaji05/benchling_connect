""" Constants file for Roche Cedex HiRes Parser"""

# Instrument Software Details
CEDEX_SOFTWARE = "Cedex software"
MODEL_NUMBER = "Roche Cedex HiRes"
PRODUCT_MANUFACTURER = "Roche"
DEVICE_TYPE = "cell count"

# Calculated Data Items List
CALCULATED_DATA_ITEM = [
    "Avg Area",
    "Avg Perimeter",
    "Avg Segm. Area",
    "Avg Compactness",
    "Total Object Count",
    "Std Dev.",
    "Aggregate Rate",
]

# Errors
MULTIPLE_SYSTEM_ERROR = (
    "Data is extracted from multiple systems and have different system parameters: "
)
