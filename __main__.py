# misura

import sys
import pkg_resources

if "--version" in sys.argv:
	print("v" + pkg_resources.get_distribution("misura").version)