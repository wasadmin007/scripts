#!/bin/bash
if [[ $# == 0  ]];then
    NOW
    echo "	$NOW	You must PASS proper arguments to the script"
    echo "		$0 takes  one argument as file "
    echo "			======	or  	 ========"
    echo "		$0 takes 6 arguments		"
    echo " 		$0 sourcedir im_install_loc user uid group gid temp_log options" 
    exit 1
fi

function NOW ()
{
        NOW=$(date "+%F | %T -")
}
function im_install_root(){
                NOW
		echo " $NOW This Installation  Triggered as root user"
                if [[ ! `grep  $group /etc/group`  ]];then
                        NOW
						echo " $NOW creating $group "
                        groupadd -g $gid $group
                fi
                if  [[ ! `id $user` ]];then
                        NOW
						echo " $NOW creating $user" 
                        useradd -c "$user" -u $uid  -m -g $group $user
                fi
                if [[ ! -f "$temp_log" ]];then
                        mkdir -p ${temp_log}
                fi
                options+=" -log ${temp_log}/mylogfile.xml"
                options+=" -installationDirectory ${im_install_loc}"
                if [[ ! -f "${im_install_loc}/eclipse/tools/imcl"  ]]; then
			${source_dir}/installc $options
        	fi
	        if [[ -f "${im_install_loc}/eclipse/tools/imcl" ]];then
                        NOW
					echo " $NOW Installation Manager Installed"
            fi
}
function  im_install_non_root(){
                NOW
		echo " $NOW Starting Installation as $user"
                if [[ `whoami` == $user ]];then
                        if [[ ! -f "$temp_log" ]];then
                                  mkdir -p ${temp_log}
                        fi
                	options+=" -log ${temp_log}/mylogfile.xml"
               		options+=" -installationDirectory ${im_install_loc}"
			if [[ ! -f "${im_install_loc}/eclipse/tools/imcl"  ]]; then
	                ${source_dir}/userinstc $options
                	fi 
			if [[ -f "${im_install_loc}/eclipse/tools/imcl" ]];then
                          NOW
		      		echo " $NOW Installation Manager Installed"
                	else
                              echo " $NOW Instalaltion Failed"
                              exit 1
                	fi
                fi
}
if [[ $# == 1 ]];then
	if [[ -f $1 ]];then
		propFileName=$1
		temp_log='/tmp/imlog/'
        	options=' -acceptLicense -s'
		source $propFileName		
		if [[ `whoami` == root ]];then
		        im_install_root
        	elif [[ `id $user` ]] || [[ `grep  $group /etc/group` ]]; then
        		im_install_non_root
        	else
                	NOW
                	echo "$NOW User $user or Group $group   Doesnot exist"
                	exit 1
        	fi
        else 
		NOW
		echo " $NOW	Usage : $0 propertyFileName"
		exit 1
	fi
elif [[ $# -gt 1 ]] && [[ $# == 6 ]];then 
	source_dir=$1
	im_install_loc=$2
	user=$3
	uid=$4
	group=$5
	gid=$6
	temp_log='/tmp/imlog/'
	options=' -acceptLicense -s'
	if [[ `whoami` == root ]];then
       	im_install_root
	elif [[ `id $user` ]] || [[ `grep  $group /etc/group` ]]; then
	im_install_non_root
	else
  		NOW
    		echo "$NOW User $user or Group $group   Doesnot exist"
    		exit 1
	fi
else 
	NOW
	echo " $NOW Usage : $0 takes 6 arguments  "
	echo " $NOW $0 sourcedir im_install_loc user uid group gid temp_log options"
	exit 1
fi
