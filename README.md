# Unparticles Workflow

## Ntuplizing

Run ExoDiphotonAnalyzer. See instruction in diphoton-analysis repo.
Then use eoshelper to spit out full path to the unmerged ntuples.

```
chmod u+x eoshelper.sh
./eoshelper.sh
```

One can inspect the root files by doing something like:

```
root -l root://cmsxrootd.fnal.gov//store/user/jjesusFchrist/rootFile.root
```

## MakeHistograms with Cuts

Chain files to loop on

```
python runChainClass.py
```

This creates the directory and template files for us to make templates
Edit the Templates with the appropriate cuts and histograms you want to store

```
cd analysis
```

To run background and barrel region
```
python createHistFiller.py -a run --background True -e BB -y 2017
```

To run unparticles sample by du and spin:
```
python createHistFiller.py -a run -s 2 -d 1p5 -e BB -y 2018
```

To run several models or parameters:
```
./runHistFiller.sh
```


# Plots

# Limits

# `makeDataCard.py`

Make datacard for one model point. Currently Basic Cut and Count.

```
cd python
python makeDataCard.py -s 2 -d 1p1
```

Script to make several datacards
```
cd script
./makeDatacardsUnparticles.sh
```

# `runCombine.sh`

After creating the datacard run Combine. This script runs the Asymptotic Limits method:
http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods/ and will spit out the limit on the signal strength (number of signal events / number of expected signal events).

`./scripts/runCombine.sh`

# `runCombineHarvester.sh`

To convert the Combine root output to json files for making plots. Currently only works for AsymptoticLimits

`./scripts/runCombineHarvester.sh`
