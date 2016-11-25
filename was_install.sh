#!/bin/bash
function argsCheck(){
	if [[ $imcl_path != '' ]] || [[ $was_install_dir != '' ]] || [[ $package != '' ]]|| [[ $version != '' ]] || [[ $repository != '' ]] || [[ $user != '' ]] || [[ $group != '' ]]; then
        	        echo "Check the passed Arguments to the script None of the following values should be empty"
                	echo "imcl_path=$imcl_path Arg was_install_dir=$was_install_dir 2Arg package=$packag 3Arg version=$version 4Arg repository=$repository 5Arg user=$user 6Arg group=$group 7Arg"
       			exit 1
	 else
         	       echo "Arguments Passed to the script are imcl_path=$imcl1Arg was_install_dir=$was_install_dir 2Arg package=$packag 3Arg version=$version 4Arg repository=$repository 5Arg user=$user 6Arg group=$group 7Arg "

                	echo "Starting Installation Process"
	fi
}
function verify (){
       if [[ -d $imcl_path ]] ;then
		echo "Imcl (Installation Manager install location) path $imcl provided"
	else
		echo "Failed Instalaltion Manager $imcl_path not existed on the system"
	fi
        if [[ -d $was_install_dir ]] ;then
               echo "$was_install_dir  Exist On The System  installation"
         else
               echo "Provided Path Not exist on the system $was_install_dir"
	       mkdir "$was_install_dir"
	fi
	if [[ `id $user` ]] && [[`grep $group /etc/group`]];then
	   echo "Installation perfomed using  $user and $group "
	else
	   echo "Failed  user $user and group $group not exist on the system"
	   exit 1
	fi
}
function getFiles(){
	user_home=`eval  echo ~$user`
if [[ -f '/var/ibm/InstallationManager/installed.xml' ]]; then
        installed_file='/var/ibm/InstallationManager/installed.xml'
        registry_file='/var/ibm/InstallationManager/installRegistry.xml'
elif [[ -f "$user_home/var/ibm/InstallationManager/installed.xml" ]]; then
	installed_file="$user_home/var/ibm/InstallationManager/installed.xml"
        registry_file="$user_home/var/ibm/InstallationManager/installRegistry.xml"
fi
}
function imcl(){

	imcl_data=`grep "location id='IBM Installation Manager'" ${installed_file}`     
        imcl_path=$(echo $imcl_data | awk -F "path" {'print $2'} | awk -F "=" {'print $2'} | awk -F ">" {'print $1'}| awk -F "'" {'print $2'})
        imcl_command_path="$imcl_path/tools/imcl"
	if [[ -f $imcl_command_path ]]; then
        	command="${imcl_command_path} ${options}"
       		if [[$user != root ]];then
		result=$(su -c "${command}")
		else
	 		result=$(${command})
			echo $result
		fi
	else
		echo "$imcl_command_path Not Exist"
	fi
}
function stopProc()
{
	if [[ -d $was_install_dir ]];then
		stopJava=$(ps -ef | grep "$was_install_dir" | grep -v "grep" | awk {'print $2'})
		echo $stopJava
	#	cmd_kill=$(kill -9 $stopJava)
		echo $cmd_kill
	fi
}
function wasInstall() 
{
	if [[ $response_file != '' ]];then

		options="$response_file"
	 else 
		options="install ${package}_${version}"
		options+=" repositories $repository -installationDriectory $was_install_dir" 
	 fi
	 options+=" -acceptLicense"
	 if [[ $args_options != '' ]];then
		 options+=" $args_options "
	 fi
	stopProc
	imcl
}
echo "starting "
if [[ $# -eq 1 ]] && [[ -f $1 ]]; then
	response_file=$1
	if [[  -f $response_file ]]; then
		echo "Reading Property File"
		source $response_file 
	else 
		echo "Reponse File is missing $response_file not exist on the system"
	fi
	argsCheck
elif [[ $# -gt 1  ]] && [[ $# -ge 7 ]] && [[ $# -le 8 ]]; then
	echo "entered"
	imcl_path=$1
	was_install_dir=$2
	package=$3
	version=$4
	repository=$5
	user=$6
	group=$7
	args_options=$8
	echo "geting files"
	argsCheck
	verify
	getFiles
	#wasInstall
else
	echo "	Usage:$0 reponseFile		"
	echo "=========or======================="
	echo "Usage:$0 imcl_path was_install_dir package version repository user group options(OPTIONAL Argument)"
fi





