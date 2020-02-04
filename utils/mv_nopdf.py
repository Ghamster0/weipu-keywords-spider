from pathlib import Path
import shutil
import re
from datetime import datetime

source_root = Path("/search/odin/data/weipu_data")
dest_root = Path("/search/odin/data/pack_nopdf")
fix_root = Path("/search/odin/data/fix_data")

# 200 per package
count = 0
package_perfix = "package_" + datetime.now().strftime("%Y%m%d%H%M%S") + "_"
package_index = 0

# finished dirs name like: QK-99908X-200311-8562752.20200202010816
for article_dir in source_root.iterdir():
    file_count = len(list(article_dir.iterdir()))
    if file_count==1:
        shutil.move(str(article_dir), str(fix_root/article_dir.name))
        print(article_dir)
        continue
    elif file_count==3:
        continue
    dest_package = dest_root / (package_perfix + str(package_index))
    dest_dir_name = article_dir.name
    dest_path = dest_package / article_dir.name
    shutil.move(str(article_dir), str(dest_path))
    count += 1
    if count >= 1000:
        count = 0
        package_index += 1
