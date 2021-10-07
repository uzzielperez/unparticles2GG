#!/bin/bash

####### Directories
# Main
eosdir='/store/user/cuperez'

#------ECHO SETTINGS
quickcheck=false
crabntuplesDEEP=false     # To search deep for ALL the unmerged CRAB ntuples
crabntuples=false         # true to get full path, uncomment appropriate sub
merged=false              # true to get full path, uncomment appropriate sub
crabADD=false
crabADDfiles=false
midsearch=true            # to get full path to directory where the root files live

project='/UnparticlesGG'



#-----------------------------
DIR=$eosdir$project$sub
DIR2=$eosdir$project$sub2

####### eos aliases
eosls='eos root://cmseos.fnal.gov ls'
eosmkdir='eos root://cmseos.fnal.gov mkdir'
eosrm='eos root://cmseos.fnal.gov rm'
eosrmdir='eos root://cmseos.fnal.gov rm -r '
xrdfsls='xrdfs root://cmseos.fnal.gov ls'

# flags
#-u=prints urls
#-l= lists

###### eos commands
# EDIT COMMAND HERE:
#$eosls -l eosdir

#--------/store/user/cuperez/projectname
while $quickcheck; do
 echo 'Printing out subdirectories of' $eosdir$project:
 for i in `$eosls $eosdir$project`
 do
   echo $i
 done
break
done

#--------/store/user/cuperez/projectname
while $crabADD; do
 echo 'Printing out subdirectories of' $eosdir$project:
 for i in `$eosls $eosdir$project`
 do
   #echo $i
   newg=$eosdir$project/$i
   for j in `$eosls $newg`
   do
     newg2=$newg/$j
     #echo $newg2
     for k in `$eosls $newg2`
     do
	newg3=$newg2/$k
	#echo $newg3
	while $crabADDfiles;
	do
	 for p in `$eosls $newg3`
	 do
	  newg4=$newg3/$p
          #echo $newg4
	  for q in `$eosls $newg4`
          do
	     newg5=$newg4/$q
	     echo $newg5
	  done
	 done
	break
	done
     done
   done
 done
break
done


#-------/store/user/cuperez/projectname/sub ------>  MERGED
while $merged; do
 echo 'Printing out Contents of Directories with Merged files':
 for i in `$eosls $DIR`
 do
  #echo $i
  newdir=$DIR/$i
  for j in `$eosls $newdir`
  do
   new=$newdir/$j
   echo $new
  done
 done
break
done

#-------/store/user/cuperez/projectname/sub2 -----> CRABNTUPLES
while $crabntuples; do
 echo 'CRAB Ntuples here:'
 for i in `$eosls $DIR2`
 do
  newdir2=$DIR2/$i
  for j in `$eosls $newdir2`
  do
   new2=$newdir2/$j
   echo $new2
  done
 done
break
done
#------MidSearch Full
redirector='root://cmsxrootd.fnal.gov/'
while $midsearch; do
 for i in `$eosls $DIR2`
 do
  newdir2=$DIR2/$i
  for j in `$eosls $newdir2`
  do
   new2=$newdir2/$j
   #echo $new2
   for k in `$eosls $new2`
   do
    new3=$new2/$k
    echo $new3
   done
  done
 done
break
done

#------DEEP Full
redirector='root://cmsxrootd.fnal.gov/'
while $crabntuplesDEEP; do
 echo 'CRAB unmerged ntuples:'
 for i in `$eosls $DIR2`
 do
   #echo $i
   newdir3=$DIR2/$i
   #echo $eosls $newdir
   for j in `$eosls $newdir3`
   do
    new3=$newdir3/$j
    for k in `$eosls $new3`
    do
     new4=$new3/$k
     #echo $new3/$k ---> just up to datesdir
     for l in `$eosls $new4`
     do
      #echo $l
      new5=$new4/$l
      #echo $new5 # -----> just up to 0000/
      for m in `$eosls $new5`
      do
       new6=$new5/$m
       echo $new6
       # echo $m # filename only
       #echo $new6 >> ${k}fi.txt
       #echo $redirector$new6 >> ${j}fi.txt
      done
     done
    done
   done
 done
break
done

echo 'To check root files'
echo 'root -l root://cmsxrootd.fnal.gov//store/user/jjesus/rootFile.root'
