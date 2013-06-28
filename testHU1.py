#!/bin/python
import os
from subprocess import check_output
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-c', nargs='?', dest='clean', const=True, default=False,
	help='cleans the directory first')
parser.add_argument('-e', nargs='?', dest='extract', const=True, default=False,
	help='extracts the archives')
parser.add_argument('-b', nargs='?', dest='build', const=True, default=False,
	help='builds the compiler')
parser.add_argument('-t', nargs='?', dest='test', const=True, default=False,
	help='tests the compiler')

args = parser.parse_args()

clean = args.clean
extract = args.extract
build = args.build
test = args.test

# get pwd
pwd = os.path.abspath(os.curdir)

if clean:
	if os.path.exists('Extracted'):
		shutil.rmtree('Extracted')

if extract:
	# get tar files
	tars = [tar for tar in os.listdir('Abgabe') if len(tar) > 7 and tar[-7:] == '.tar.gz']

	# extract to Extracted
	if not os.path.exists('Extracted'):
		os.mkdir('Extracted')
	os.chdir('Extracted')
	for tar in tars:
		output = check_output(['tar', '-xzvf', '../Abgabe/' + tar], universal_newlines=True)
		print(output)
	os.chdir(pwd)

if build:
	# get dirs
	os.chdir('Extracted')
	dirs = os.listdir(os.curdir)
	for d in dirs:
		os.chdir(d)
		try:
			output = check_output(['make'], universal_newlines=True)
			print(output)
		except Exception as e:
			print(e)
		os.chdir(pwd+'/Extracted')
	os.chdir(pwd)

if test:
	# get dirs
	os.chdir('Extracted')
	dirs = os.listdir(os.curdir)
	for d in dirs:
		os.chdir(d)
		print(d)
		for test in [test  for test in os.listdir('../../reftests') if len(test) > 4 and test[-4:] == '.spl']:
			try:
				output = check_output(['./spl', '--absyn', '../../reftests/'+test], universal_newlines=True)
				#print(output)
			except Exception as e:
				print(e)
		os.chdir(pwd+'/Extracted')
	os.chdir(pwd)
