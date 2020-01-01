import os
import argparse
import sys
import secrets
import weights as fightWeights
import subprocess
import platform

from os import listdir
from subprocess import PIPE, STDOUT

# Check if Mac or PC
if platform.system() == 'Darwin':
    pyVar = 'python3'
else:
    pyVar = 'python'

profiles = []
apiKey = secrets.apiKey
version = 'nightly'
weights = '-s'
weightsSingle = fightWeights.weightsSingle
weightsNy = fightWeights.weightsNy

parser = argparse.ArgumentParser(description='Parses a list of reports from Raidbots.')
parser.add_argument('dir', help='Directory you wish to sim. Options are 1. talents/ 2. racials/ 3. gear/ 4. enchants/ 5. consumables/ 6. azerite-traits/')
parser.add_argument('--weights', help='For sims ran with weights this flag will change how simParser is ran.', action='store_true')
parser.add_argument('--iterations', help='Pass through specific iterations to run on. Default is 10000')
parser.add_argument('--dungeons', help='Run a dungeonsimming batch of sims.', action='store_true')
parser.add_argument('--talents', help='indicate talent build for output.', choices=['AS','SC'])
args = parser.parse_args()

if args.weights:
    weights = ''

if args.iterations:
    iterations = args.iterations
else:
    iterations = "10000"

sys.path.insert(0, args.dir)
import reports

print("Running sims on {0} in {1}".format(version, args.dir))

if args.dir == "stats/":
    report = reports.reportsStats
    DSreport = reports.reportsDungeonsStats
elif args.dir == "talents/":
    report = reports.reportsTalents
    DSreport = reports.reportsDungeonsTalents
elif args.dir == "trinkets/":
    report = reports.reportsTrinkets
    DSreport = reports.reportsDungeonsTrinkets
elif args.dir == "azerite-gear/":
    report = reports.reportsAzerite
    DSreport = reports.reportsDungeonsAzerite
elif args.dir == "azerite-traits/":
    report = reports.reportsAzeriteTraits
    DSreport = reports.reportsDungeonsAzeriteTraits
else:
    DSreport = reports.reportsDungeons
    report = reports.reports

# determine sim files
if args.dungeons:
    for value in DSreport:
        profile = value.replace('results', 'profiles')
        profile = profile.replace('json', 'simc')
        profiles.append(profile)
else:
    for value in report:
        profile = value.replace('results', 'profiles')
        profile = profile.replace('json', 'simc')
        profiles.append(profile)

# determine existing jsons
existing = listdir(args.dir + 'results/')
count = 0

for value in profiles:
    count = count + 1
    if not args.dungeons:
        lookup = value[9:-5]
        if args.dir == "talents/" or args.dir == "trinkets/" or args.dir == "stats/" or args.dir == "azerite-gear/" or args.dir == "azerite-traits/":
            lookup = lookup[lookup.index('_')+1:]
        weight = weightsNy.get(lookup)
        weightST = weightsSingle.get(lookup)
        if weightST:
            weight = weight + weightST
    else:
        weight = 1
    print("Simming {0} out of {1}.".format(count, len(profiles)))
    name = value.replace('simc', 'json')
    name = name.replace('profiles', 'results')
    if name[8:] not in existing and weight > 0:
        reportName = args.dir + name[8:-5]
        name = args.dir + name
        value = args.dir + value
        subprocess.call([pyVar, 'api.py', apiKey, value, '--simc_version', version, name, reportName, '--iterations', iterations], shell=False)
    elif weight == 0:
        print("{0} has a weight of 0. Skipping file.".format(name[8:]))
    else:
        print("{0} already exists. Skipping file.".format(name[8:]))

results_dir = args.dir + "results/"
subprocess.call([pyVar, 'simParser.py', '-c', weights, '-r', '-d', results_dir], shell=False)

# analyze.py
if args.dungeons:
    script = "analyzeDS.py"
else:
    script = "analyze.py"

cmd = "{0} {1} {2}".format(pyVar, script, args.dir)

if args.weights:
    cmd += " --weights"
if args.talents:
    cmd += " --talents {0}".format(args.talents)
subprocess.call(cmd, shell=True)
