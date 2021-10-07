# Unparticles Workflow

## Step 0:

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

## Step 1:

Chain files to loop on

```
python runChainClass.py
```

This creates the directory and template files for us to make templates

## Step 2:
