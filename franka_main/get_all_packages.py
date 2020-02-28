# Prints out all packages installed and saves them to a file in the local directory
# The command line version is : pip freeze > requirements.txt
# Created by Medad Newman 28/02/2020


#!/usr/bin/env python3

import pkg_resources

dists = [str(d).replace(" ","==") for d in pkg_resources.working_set]

with open('packages.txt', 'w') as the_file:
    for i in dists:
        print(i)
        the_file.write(i+"\n")


print("done")