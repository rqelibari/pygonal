#!/bin/bash
#############################################################################
#	Pygonal
#
#	(c) 2016 Copyright Rezart Qelibari <qelibarr@informatik.uni-freiburg.de>
#	Portions copyright (c) 2010 by Casey Duncan
#	Portions copyright (c) 2009 The Super Effective Team
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
# 		http://www.apache.org/licenses/LICENSE-2.0
#
#	Unless required by applicable law or agreed to in writing, software
#	distributed under the License is distributed on an "AS IS" BASIS,
#	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#	See the License for the specific language governing permissions and
#	limitations under the License.
#
#	See LICENSE.txt and CREDITS.txt
#############################################################################


# - Run unit tests from python 2.6, 2.7, 3.1
# - Then run doctests to verify doc examples

error=0

rm -rf build

OLDPYTHONPATH="${PYTHONPATH}";
export PYTHONPATH="./pygonal/tests:${PYTHONPATH}";
for ver in 2.7 3 3.5; do
	echo "************"
	echo " Python $ver"
	echo "************"
	echo
	if which python${ver}; then
		python${ver} -m unittest discover || error=1
	else
		echo >&2 "!!! Python ${ver} not found !!!"
		error=1
	fi
done
export PYTHONPATH="${OLDPYTHONPATH}";

echo
echo -n "Doctests... "
srcdir=`pwd`
python3 -m doctest ${srcdir}/doc/source/*.rst && echo "OK" || error=1

exit $error
