#!/bin/bash

function NOW ()
{
        NOW=$(date "+%F | %T -")
}
function verifyPackage()
{
	existing_installed_data=$(grep "$package" $registry_file |  awk -F "id=" {'print $2'} | awk -F ">" {'print $1'} | awk -F "'" {'print $2'})
	existing_version_data=$(grep "$version" $registry_file | awk -F "value='" {'print $2'} | awk -F "' repoInfo=" {'print $1'})
        existing_repo_file=$(grep "$version" $registry_file | awk -F 'Name=' {'print $2'} | awk -F "," {'print $1'})
	NOW
	echo "$NOW ${existing_installed_data}_${existing_version_data}_${existing_repo_file}"
	NOW
	if [[ "${existing_installed_data}_${existing_version_data}_${existing_repo_file}" == "${package}_${version}_${repository}" ]];then
		echo "$NOW package is already installed ${package}_${version}_${repository}"	
		exit 0
	fi
}

function uninstall_was(){
    options="uninstall ${package}_${version} -s -installationDirectory $was_install_dir"
    imcl
}
function argsCheck(){
	NOW
	if [[ $imcl_path == '' ]] || [[ $was_install_dir == '' ]] || [[ $package == '' ]]|| [[ $version == '' ]] || [[ $repository == '' ]] || [[ $user == '' ]] || [[ $group == '' ]] || [[ $install == '' ]]; then
			NOW
        	        echo "$NOW Check the passed Arguments to the script None of the following values should be empty"
                	echo "$NOW imcl_path=$imcl_path Arg was_install_dir=$was_install_dir 2Arg package=$packag 3Arg version=$version 4Arg repository=$repository 5Arg user=$user 6Arg group=$group 7Arg install=$install 8Arg"
       			exit 1
	 else
         	       echo "$NOW Arguments Passed to the script are imcl_path=$imcl_pathArg was_install_dir=$was_install_dir 2Arg package=$packag 3Arg version=$version 4Arg repository=$repository 5Arg user=$user 6Arg group=$group 7Arg "

                	echo "$NOW Starting Installation Process"
	fi
}
function verify (){
        NOW
	if [[ -d $imcl_path ]] ;then
		echo "$NOW Imcl (Installation Manager install location) path $imcl provided"
	else
		echo "$NOW Failed Instalaltion Manager $imcl_path not existed on the system"
	fi
        if [[ -d $was_install_dir ]] ;then
               echo "$was_install_dir  Exist On The System "
         else
               echo "Provided Path Not exist on the system $was_install_dir Creating the directory"
	       mkdir "$was_install_dir"
	fi
	if [[ `id $user` ]] && [[ `grep $group /etc/group` ]];then
	   echo "Installation perfomed using  $user and $group "
	else
	   echo "Failed  user $user and group $group not exist on the system"
	   exit 1
	fi
}
function getFiles(){
	NOW
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
	NOW
	imcl_data=`grep "location id='IBM Installation Manager'" ${installed_file}`     
        imcl_path=$(echo $imcl_data | awk -F "path" {'print $2'} | awk -F "=" {'print $2'} | awk -F ">" {'print $1'}| awk -F "'" {'print $2'})
        imcl_command_path="$imcl_path/tools/imcl"
	echo "$NOW $imcl_command_path ${options}"
	if [[ -f $imcl_command_path ]]; then
        	command="${imcl_command_path} ${options}"
       		if [[ $user == root ]];then
		result=$(su -c "${command}")
		else
	 		result=$(${command})
			echo $result
		fi
	else
		echo "$NOW $imcl_command_path Not Exist"
	fi
}
function stopProc()
{
	NOW
	if [[ -d $was_install_dir ]];then
		stopJava=$(ps -ef | grep java |grep "$was_install_dir" | grep -v "grep" | awk {'print $2'})
		echo " $NOW Stopping Necessary Java Process $stopJava"
		if [[ $stopJava != '' ]]; then
			cmd_kill=$(kill -9 $stopJava)
			echo $cmd_kill
		fi
	fi
}
function wasInstall() 
{
	if [[ $response_file != '' ]];then

		options="$response_file"
	 else 
		options="install ${package}_${version}"
		options+=" -repositories $repository -installationDirectory $was_install_dir" 
	 fi
	 options+=" -acceptLicense"
	 if [[ $args_options != '' ]];then
		 options+=" $args_options "
	 fi
	stopProc
	imcl
}
NOW
echo "starting "
if [[ $# -eq 1 ]] && [[ -f $1 ]]; then
	response_file=$1
	if [[  -f $response_file ]]; then
		echo " $NOW Reading Property File"
		source $response_file 
	else 
		echo "$NOW Reponse File is missing $response_file not exist on the system"
	fi
	getFiles
        wasInstall
elif [[ $# -gt 1  ]] && [[ $# -ge 8 ]] && [[ $# -le 9 ]]; then
	echo " $NOW Starting Script execution "
	imcl_path=$1
	was_install_dir=$2
	package=$3
	version=$4
	repository=$5
	user=$6
	group=$7
	install=$8
	args_options=$9
	argsCheck
	verify
	getFiles
	if [[ $install == install ]]; then
	 	verifyPackage
		wasInstall
	elif [[ $install == uninstall ]]; then
		uninstall_was		
	fi	
else
	echo " $NOW	Usage:$0 reponseFile		"
	echo "=========or======================="
	echo " $NOW Usage:$0 imcl_path was_install_dir package version repository user group install options(OPTIONAL Argument)"
fi





