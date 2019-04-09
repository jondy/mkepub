output=D:/projects/mkepub/tools/storage

pdfpath=$output/pdf_input
checkpath=$output/checked
logpath=$output/logs

[[ -d "$pdfpath" ]] || mkdir "$pdfpath"
[[ -d "$checkpath" ]] || mkdir "$checkpath"
[[ -d "$logpath" ]] || mkdir "$logpath"

result=$output/result.pass.txt
failed=$output/result.fail.txt

filelist=filelist.txt

ghostscript=ghostscript/gswin64c.exe
pdf2html=pdf2html/pdf2htmlEx.exe
mkepub=../dist/mkepub/mkepub.exe

for filename in $(cat $filelist) ; do
    
    echo "Processing $filename ..."
    name=$(basename $filename)

    echo "Got name: $name"
    logfile=$logpath/$name.log
    
    # Prepare pdf file
    echo "Verify pdf file by ghost scripts..."
    $ghostscript  -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dCompatibilityLevel=1.4 \
                  -dPDFSETTINGS=/ebook -dDetectDuplicateImages=true \
                  -o $pdfpath/$name $filename >> $logfile 2>&1
    
    if (( $? )) ; then
        echo "Verify file failed"
        echo "$filename verify failed" >> $failed
        continue
    fi
    
    # Generate check page
    echo "Generate check page"
    $pdf2html --last-page 10 $pdfpath/$name $name.html >> $logfile 2>&1
    
    echo "Convert to pdf"
    (cd $(dirname $mkepub); ./mkepub.exe $pdfpath/$name >> $logfile 2>&1)

    if (( $? )) ; then
        echo "Make epub failed"
        echo "$filename make epub failed" >> $failed
    else
        echo "Make epub OK"
        echo "$filename" >> $result
    fi
    
done

