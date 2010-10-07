#
# namcap rules - elffiles
# Copyright (C) 2009 Hugo Doria <hugo@archlinux.org>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import os
from Namcap.util import is_elf, clean_filename

def scanelf(invalid_elffiles, dirname, names):
	'''Method to scan for ELF files in invalid directories'''

	# Valid directories for ELF files
	valid_dirs = ['/bin/', '/sbin/', '/usr/bin/', '/usr/sbin/', '/lib/',
			'/usr/lib/', '/usr/lib32/']
	
	for i in names:
		file_path = os.path.join(dirname, i)
		valid_dir_found = False
		
		# Checking for ELF files
		if is_elf(file_path):
			for f in valid_dirs:
				if ('/' + clean_filename(file_path)).startswith(f):
					valid_dir_found = True
					break 

			if not valid_dir_found:
				invalid_elffiles.append(clean_filename(file_path))


class package:
	def short_name(self):
		return "elffiles"
	def long_name(self):
		return "Check about ELF files outside some standard paths."
	def prereq(self):
		return "extract"
	def analyze(self, pkginfo, data):
		ret = [[], [], []]
		invalid_elffiles = []
		
		os.path.walk(data, scanelf, invalid_elffiles)		
		if len(invalid_elffiles) > 0:			
			for i in invalid_elffiles:
				ret[0].append(("elffile-not-in-allowed-dirs %s", i))
					
		return ret
	
	def type(self):
		return "tarball"

# vim: set ts=4 sw=4 noet:
