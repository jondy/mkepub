@ECHO OFF
REM
REM 延安红云平台 PDF 批量转换 EPUB 脚本
REM
REM 首先需要安装 ghostscript 工具，用于对 PDF 文件进行预处理，下载地址
REM     http://yancloud.red/downloads/gs927w64.exe
REM
REM 然后把所有需要转换的全路径 PDF 文件名称写入到文件 filelist.txt 每一个 PDF 文件占一行
REM 
REM 运行脚本之前，请检查脚本里面所有的 TODO 语句，确保已经完成 TODO 中指定的操作，主要的设置包括:
REM    * 设置输出路径，所有的输出文件，转换好的 EPUB 都会存放到这里
REM 
REM 脚本检查好之后，双击该脚本就可以运行，本工具会执行下面的操作：
REM     1. 读取和脚本相同目录下面的文件 filelist.txt 
REM     2. 读取第一行包含的需要转换的 PDF 文件
REM     3. 使用 ghostscript 对 PDF 文件进行优化，并检查是否能够进行转换
REM             如果检查失败，那么该 PDF 无法被转换，保存文件名到 result.failed.txt，然后继续处理下一本 PDF
REM     4. 转换 PDF 的前5页到一个 html 文件，用于人工检查转换后的格式是否正确
REM             如果检查失败，那么该 PDF 无法被转换，保存文件名到 result.failed.txt，然后继续处理下一本 PDF
REM     5. 转换 PDF 到 EPUB，保存在编辑工具安装路径下面的 epub/ 子目录下面
REM              如果转换失败，保存文件名到 result.failed.txt
REM              如果转换成功，保存文件名到 result.pass.txt
REM     6. 继续处理下一本 PDF
REM

SetLocal

REM TODO: 设置输出路径，默认是当前脚本所在的路径
Set OUTPUT=%~dp1

REM TODO: 设置编辑工具所在路径，默认是当前脚本所在的路径的上两级路径
Set MKEPUBPATH=%~dp1\..\..

REM TODO: 设置 ghostscript 脚本
Set GS=C:\Program Files\gs\gs9.27\bin\gswin64c.exe
Set GS=C:\Program Files\gs\gs9.26\bin\gswin64c.exe

Set ROOTPATH=%~dp1
Set INPUTFILE=%ROOTPATH%\filelist.txt

Set PDF2HMLT=%MKEPUBPATH%\tools\pdf2html\pdf2htmlEx.exe
Set MKEPUB=mkepub.exe

Set PDFPATH=%OUTPUT%\input
Set HMTLPATH=%OUTPUT%\html
Set LOGPATH=%OUTPUT%\log
Set EPUBPATH=%OUTPUT%\epub

Set RESULTFILE=%OUTPUT%\result.txt
Set PASSFILE=%OUTPUT%\result.pass.txt
Set FAILEDFILE=%OUTPUT%\result.failed.txt

If NOT EXIST "%GS%" (
    Echo.
    Echo  找不到 %GS% ，请下载安装 http://yancloud.red/downloads/gs927w64.exe
    Echo.
    Goto END
)

If NOT EXIST "%INPUTFILE%" (
    Echo.
    Echo  输入文件 %INPUTFILE% 不存在
    Echo.
    Goto END
)

If NOT EXIST "%MKEPUBPATH%\%MKEPUB%" (
    Echo.
    Echo  找不到编辑工具，请下载安装 http://yancloud.red/downloads/yanhong-editor.exe
    Echo.
    Goto END
)

FOR /F "" %i IN (%INPUTFILE%) DO (
    @Echo 开始处理 %i ...
    @Echo %filename% >> %RESULTFILE%
    
    Set filename=%~ni
    Set logfile=%LOGPATH%\%filename%.log
    
    @Echo 文件名称 %filename%
    @Echo 输出日志到  %logfile%
    
    @Echo 开始对 pdf 文件进行预处理 ...
    %GS%  -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dDetectDuplicateImages=true -o %PDFPATH%/%filename% %filename% >> %logfile% 2>&1
    If NOT ERRORLEVEL 0 (
        Echo.
        Echo 预处理失败，该 PDF 格式存在问题
        Echo.
        @Echo %filename% 预处理失败 >> %FAILEDFILE%
        Goto END
    )
    @Echo 预处理成功，处理后的文件保存为 %PDFPATH%/%filename%
    
    @Echo 正在生成前 5 页的 HTML 文件
    %PDF2HMLT% --last-page 5 %PDFPATH%/%filename% %filename%.html >> %logfile% 2>&1
    
    If NOT ERRORLEVEL 0 (
        Echo.
        Echo 生成 HTML 文件失败
        Echo.
        @Echo %filename% 生成 HTML 文件失败 >> %FAILEDFILE%
        Goto END
    )    
    MOVE /Y %filename%.html %HMTLPATH%
    @Echo 生成的 HTML 文件保存在 %HMTLPATH%/%filename%.html
    
    SetLocal
        @Echo 切换到路径 %MKEPUBPATH%
        CD /D %MKEPUBPATH%
        
        @Echo 开始生成 EPUB ...
        %MKEPUB% %PDFPATH%/%filename% >> %logfile% 2>&1
        If NOT ERRORLEVEL 0 (
            Echo.
            Echo 生成 EPUB 文件失败
            Echo.
            @Echo %filename% 生成 EPUB 文件失败 >> %FAILEDFILE%
            Goto END
        )    
        
        @Echo %filename% >> %PASSFILE%
        @Echo EPUB 文件成功生成，保存在 %MKEPUBPATH%/output
    
    EndLocal
)

:END

EndLocal
Pause
