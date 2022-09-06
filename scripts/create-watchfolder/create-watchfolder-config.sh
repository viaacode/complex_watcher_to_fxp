#!/bin/bash
## i: org_id
## p: process_mets
READ_METS=False
FTPHOST_DEST=server2.ftp-qas.mh
FTPHOST_DEST=server.ftp-qas
FTPUSER_DEST=larry
FTPPASS_DEST=moo
FTPPATH_DEST=/______
FTPUSER_SRC=srcuser
FTPPASS_SRC=xxxxxxx
BASE_PATH_FTP=/export/home/
SUFFIX_PATH_FTP=/incoming/complex2fxp/
ORG_API_URL=http://org-api-qas
MQ_HOST=mq-qas
MQ_USER=user
MQ_PASS=tpasssss
MQ_QUEUE=test-fxp-queue
MQ_ERR_QUEUE=test_error

_usage(){
cat <<EOF
$(basename "${0}")
  Usage
   $(basename "${0}") [OPTIONS]
  Options
   -h  display this help
   -i the NOID of org OR_ID
   -p enable get mam name for tarhet dir
   -o output filepath for config
  Notes
   creates a watchfolder and config.yaml on ftp
EOF
}

# check args are given, else run _usage
if [[ -z $1 ]] || [[ -z $2 ]]; then _usage ;fi;
_create_config () {
cat <<EOF
viaa:
  logging:
    level: INFO

app:
  watcher:
    dest_path: $FTPPATH_DEST
    dest_host: $FTPHOST_DEST
    dest_user: $FTPUSER_DEST
    dest_pass: $FTPPASS_DEST
    source_host: $FTPHOST_DEST
    source_path: $FTPPATH_SRC
    source_user: $FTPUSER_SRC
    source_pass: $FTPPASS_SRC
    read_mets: $READ_METS
    org_api_url: $ORG_API_URL
  amqpPublisher:
    host: $MQ_HOST
    user: $MQ_USER
    pass: $MQ_PASS
    queue: $MQ_QUEUE
    error_queue: $MQ_ERR_QUEUE

EOF
}

while getopts "hi:p:o:" OPT ; do
    case "${OPT}" in

      h) _usage ; exit 0
        ;;
      i)
        export OR_ID=$OPTARG
	export FTPPATH_SRC=${BASE_PATH_FTP}${OR_ID}${SUFFIX_PATH_FTP}
         ;;
      p)
        READ_METS=$OPTARG
        if [[ ! -z "READ_METS" ]];then echo ___ using $READ_METS for READ_METS  ___;else echo no such type givven;_usage  ;exit 1;fi
        if [ "$READ_METS" == 'y' ]
          then export READ_METS=True; 
	  echo ________DEST PATH WILL BE CALCULATED________________
	  export FTPPATH_DEST=_CALCULATED_
        else
	  echo keeping default $READ_METS for READ_METS
	  export READ_METS=False
        fi
        ;;
      o)
        OUTPUT_PATH=$OPTARG
          export OUTPUT_PATH=$OPTARG
	echo configfile path: $OPTARG
        ;;


      *) echo "bad option -${OPTARG}" ; _usage ; exit 1 ;
  esac
done

_create_config | tee $OUTPUT_PATH

