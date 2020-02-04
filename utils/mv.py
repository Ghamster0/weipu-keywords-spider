from pathlib import Path
import shutil
import re
from datetime import datetime

source_root = Path("/search/odin/data/weipu_data")
dest_root = Path("/search/odin/data/pack")

# 200 per package
count = 0
package_perfix = "package_" + datetime.now().strftime("%Y%m%d%H%M%S") + "_"
package_index = 0

# finished dirs name like: QK-99908X-200311-8562752.20200202010816
for article_dir in source_root.glob("*.*"):
    dest_package = dest_root / (package_perfix + str(package_index))
    dest_dir_name = article_dir.name[:-15]
    dest_path = dest_package / dest_dir_name
    shutil.move(str(article_dir), str(dest_path))
    count += 1
    if count >= 400:
        count = 0
        package_index += 1
