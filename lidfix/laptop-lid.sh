#!/bin/bash

#source $HOME/.Xdbus
grep -q closed /proc/acpi/button/lid/LID/state
if [ $? = 0 ]
then
    # close action
    echo "roberto"
else
    # open action
    runuser -l robot -c 'python /opt/alienfx/restoreConfig.py'
fi

