from .data import PriceData
from datetime import datetime

data = PriceData()
# list_ = data.read_data("PTBA")
data.update_info["PTBA"] = datetime.now()
data.store_last_update()
data.update_info = {}
data.load_last_update()
print(data.update_info)