#!/bin/bash
Echo "1: Reset Only Migration Files"
Echo "2: Reset The Whole Database. Historical Data will ALL LOSE!"
Echo "3: Quit"
options=("Option 1" "Option 2" "Quit")

title="What you want to do: "
prompt="Pick an option (choose 1,2 or 3): "

echo "$title"
PS3="$prompt "

select opt in "${options[@]}"
do
    case $opt in
        "Option 1")
            echo "Deleting migration files..."
            find . -path "*/migrations/*.pyc"  -delete
            find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
            echo "Done."
            break
            ;;
        "Option 2")
            echo "Deleting migration files and database files..."
            find . -path "*/migrations/*.pyc"  -delete
            find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
            rm -rf ./mysql_data/mysql/*
            touch ./mysql_data/mysql/.keep
            echo "Done."
            break
            ;;
        "Quit")
            echo "Quit"
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

