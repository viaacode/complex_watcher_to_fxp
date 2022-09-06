#!/bin/bash
set +e-x
#:i > csv: or_id,read_mets
#

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT


export BASEPATH=$(pwd)
while IFS="," read -r OR_ID READ_METS
do
   echo "Organisation: $OR_ID process $READ_METS"
   mkdir /export/home/$OR_ID/incoming/complex2fxp/ 2> /dev/null || echo source dir exits
   cd "$BASEPATH"
   mkdir "$OR_ID" 2>/dev/null || echo target exists
   cd  "$OR_ID"
   echo creating config for watcher in dir $(pwd)
   sh "$BASEPATH"/create-watchfolder-config.sh -i $OR_ID -p $READ_METS -o config.yml
   echo starting  watcher in $(pwd), reading mets is $READ_METS
   complex_watcher &
   echo "$!" > "$BASEPATH"/"$OR_ID".pid

done  < <(tail -n +1 orgs.csv)

function ctrl_c() {
        echo "** Trapped CTRL-C"
        cd "$BASEPATH"
	for p in `ls *pid`;do kill `cat "$p"` && rm "$p";done
}

# keep sleeping
wait

