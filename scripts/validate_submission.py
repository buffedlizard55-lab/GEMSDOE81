#!/usr/bin/env python3
import sys; sys.path.insert(0,"src")
from gems81.submission_writer import validate
import json, glob
f=sys.argv[1] if len(sys.argv)>1 else glob.glob("docs/downloads/*.tif")[0]
print(json.dumps(validate(f,"data/sample_submission.tif"),indent=2))
