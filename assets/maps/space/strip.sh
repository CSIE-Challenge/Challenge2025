if [[ $# -ne 1 ]]
then 
    exit 1
fi
cp $1 $1.bak
# use a / 2 to decrease shade, 0 to remove
convert $1 \
  -alpha on \
  -channel A \
  -fx "((r==0 && g==0 && b==0) ? a / 2 : a)" \
  $1