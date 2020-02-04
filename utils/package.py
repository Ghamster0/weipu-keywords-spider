from pathlib import Path
import shutil
import os
from datetime import datetime

work_dir = Path("/search/odin/data/pack")
out_dir = "/search/odin/data/tmp"

current_batch = datetime.now().strftime("%Y%m%d%H%M%S")
prefix = "package_"

for d in work_dir.glob(prefix + "*"):
    print(f"Next:\n{str(d)}")
    
    print("archive")
    tar_name = f"{current_batch}_{d.name[len(prefix):]}_full"
    # tar_name = f"{current_batch}_{d.name[len(prefix):]}_nopdf"
    shutil.make_archive(
        out_dir + "/" + tar_name, "gztar", str(d),
    )

    print("upload")
    tar_path = f"{out_dir}/{tar_name}.tar.gz"
    os.system(f"hadoop fs -put {tar_path} /user/slave/websac/cqvip/agw/")
    print("clean")
    os.remove(tar_path)
    shutil.rmtree(str(d))
