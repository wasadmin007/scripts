#!/bin/bash
function createProfile()
{
hostname=`hostname`
   if [[ "${profile_host}" == "${hostname}" ]];then
	if [[ $template_type == dmgr ]] ;then	
		options="-create -profileName ${profile_name} -profilePath ${profile_base}/${profile_name} -templatePath ${template_path} -nodeName ${node_name} -hostName ${profile_host} -cellName ${cell}"
	elif [[ $template_type == managed ]];then
		options="-create -profileName ${profile_name} -profilePath ${profile_base}/${profile_name} -templatePath ${template_path} -nodeName ${node_name} -hostName ${profile_host} -federateLater true -cellName ${cell}"
	else 
		echo "Profile type must be in cell  default  dmgr  managed  management  secureproxy"
		echo "AppNode profile should be managed"
	fi
	if [[ -f "${was_installed_dir}/bin/manageprofiles.sh" ]] && [[ $options != '' ]]; then
                ${was_installed_dir}/bin/manageprofiles.sh $options
        fi
   fi
}
function readArgs(){
	createProfile  
}
if [[ $1 == options ]] && [[ $# == 3 ]];then
	options=$2
	was_installed_dir=$3
	profile_host=$4
	readArgs  
elif [[ $1 == file ]] && [[ $# == 2 ]];then
	source $2
	readArgs
elif [[ $# -gt 3 ]] && [[ $# == 7 ]]; then
	profile_name=$1
	profile_base=$2
	was_installed_dir=$3
	template_type=$4
	if [[ $template_type == 'dmgr' ]]; then
		template_path=${was_installed_dir}/profileTemplates/${template_type}			
	elif [[ $template_type == 'app' ]]; then
		template_path=${was_installed_dir}/profileTemplates/${template_type}
	fi
	node_name=$5
	profile_host=$6
	cell=$7
	readArgs
else
	echo "Usage : $0 profile_name profile_base was_installed_dir template_type node_name profile_host cell"
	echo " ============================OR================================="
	echo "Usage: $0 options  '"-create -profileName ${profile_name} -profilePath ${profile_base}/${profile_name} -templatePath ${template_path} -nodeName ${node_name} -hostName ${profile_host} -cellName ${cell}"'"
	echo "=============================OR================================="
	echo "Usage : $0 file propsFile.txt "
	echo "Propeties are profile_name profile_base was_installed_dir template_type node_name profile_host cell"
fi
