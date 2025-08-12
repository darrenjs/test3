ff is a function
ff () 
{ 
    for file in $*;
    do
        find . -iname \*$file\* | \grep --color=auto -i $file;
    done
}
