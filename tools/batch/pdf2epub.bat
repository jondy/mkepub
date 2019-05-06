@ECHO OFF
REM
REM �Ӱ�����ƽ̨ PDF ����ת�� EPUB �ű�
REM
REM ������Ҫ��װ ghostscript ���ߣ����ڶ� PDF �ļ�����Ԥ�������ص�ַ
REM     http://yancloud.red/downloads/gs927w64.exe
REM
REM Ȼ���������Ҫת����ȫ·�� PDF �ļ�����д�뵽�ļ� filelist.txt ÿһ�� PDF �ļ�ռһ��
REM 
REM ���нű�֮ǰ������ű��������е� TODO ��䣬ȷ���Ѿ���� TODO ��ָ���Ĳ�������Ҫ�����ð���:
REM    * �������·�������е�����ļ���ת���õ� EPUB �����ŵ�����
REM 
REM �ű�����֮��˫���ýű��Ϳ������У������߻�ִ������Ĳ�����
REM     1. ��ȡ�ͽű���ͬĿ¼������ļ� filelist.txt 
REM     2. ��ȡ��һ�а�������Ҫת���� PDF �ļ�
REM     3. ʹ�� ghostscript �� PDF �ļ������Ż���������Ƿ��ܹ�����ת��
REM             ������ʧ�ܣ���ô�� PDF �޷���ת���������ļ����� result.failed.txt��Ȼ�����������һ�� PDF
REM     4. ת�� PDF ��ǰ5ҳ��һ�� html �ļ��������˹����ת����ĸ�ʽ�Ƿ���ȷ
REM             ������ʧ�ܣ���ô�� PDF �޷���ת���������ļ����� result.failed.txt��Ȼ�����������һ�� PDF
REM     5. ת�� PDF �� EPUB�������ڱ༭���߰�װ·������� epub/ ��Ŀ¼����
REM              ���ת��ʧ�ܣ������ļ����� result.failed.txt
REM              ���ת���ɹ��������ļ����� result.pass.txt
REM     6. ����������һ�� PDF
REM

SetLocal

REM TODO: �������·����Ĭ���ǵ�ǰ�ű����ڵ�·��
Set OUTPUT=%~sdp0

REM TODO: ���ñ༭��������·����Ĭ���ǵ�ǰ�ű����ڵ�·����������·��
Set MKEPUBPATH=%~sdp0\..\..

REM TODO: ���� ghostscript �ű�
Set GS=C:\Program Files\gs\gs9.27\bin\gswin64c.exe

Set ROOTPATH=%~sdp0
Set INPUTFILE=%ROOTPATH%\filelist.txt

Set PDF2HMLT=%MKEPUBPATH%\tools\pdf2html\pdf2htmlEx.exe
Set MKEPUB=mkepub.exe

Set PDFPATH=%OUTPUT%\input
Set HMTLPATH=%OUTPUT%\html
Set LOGPATH=%OUTPUT%\log
Set EPUBPATH=%OUTPUT%\epub
Set MKEPUB_OUTPUT=%OUTPUT%\epub

Set RESULTFILE=%OUTPUT%\result.txt
Set PASSFILE=%OUTPUT%\result.pass.txt
Set FAILEDFILE=%OUTPUT%\result.failed.txt

If NOT EXIST "%GS%" Set GS=C:\Program Files\gs\gs9.26\bin\gswin32c.exe
If NOT EXIST "%GS%" (
    Echo.
    Echo �Ҳ��� %GS% �������ذ�װ http://yancloud.red/downloads/gs927w64.exe
    Echo.
    Goto END
)

If NOT EXIST %INPUTFILE% (
    Echo.
    Echo �����ļ� %INPUTFILE% ������
    Echo.
    Goto END
)

If NOT EXIST %MKEPUBPATH%\%MKEPUB% (
    Echo.
    Echo �Ҳ����༭���ߣ������ذ�װ http://yancloud.red/downloads/yanhong-editor.exe
    Echo.
    Goto END
)

If NOT EXIST %PDFPATH% MD %PDFPATH%
If NOT EXIST %HMTLPATH% MD %HMTLPATH%
If NOT EXIST %LOGPATH% MD %LOGPATH%
If NOT EXIST %MKEPUB_OUTPUT% MD %MKEPUB_OUTPUT%

FOR /F "delims=;" %%i IN (%INPUTFILE%) DO ( 
   
    @Echo =========================================================
    @Echo ��ʼ���� %%i ...
    @Echo %%i >> %RESULTFILE%

    @Echo �ļ����� %%~nxi
    @Echo �����־��  "%LOGPATH%\%%~ni.log"

    @Echo ��ʼ�� pdf �ļ�����Ԥ���� ...
    @Echo ����Ҫһ��ʱ�䣬�����ĵȺ�
    CALL "%GS%"  -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dDetectDuplicateImages=true -o "%PDFPATH%\%%~nxi" "%%i" >> "%LOGPATH%\%%~ni.log"
    If ERRORLEVEL 0 (
        @Echo Ԥ����ɹ����������ļ�����Ϊ %PDFPATH%\%%~nxi
        
        @Echo ��������ǰ 5 ҳ�� HTML �ļ�
        "%PDF2HMLT%" --last-page 5 "%PDFPATH%\%%~nxi" "%%~ni.html" >> "%LOGPATH%\%%~ni.log"
        
        If ERRORLEVEL 0 (
            MOVE /Y "%%~ni.html" "%HMTLPATH%"
            @Echo ���ɵ� HTML �ļ������� %HMTLPATH%\%%~ni.html
            
            SetLocal
            @Echo �л���·�� %MKEPUBPATH%
            CD /D "%MKEPUBPATH%"
            
            @Echo ��ʼ���� EPUB ...
            %MKEPUB% "%PDFPATH%\%%~nxi" >> "%LOGPATH%\%%~ni.log"
            If EXIST "%MKEPUB_OUTPUT%\%%~ni.epub" (
                @Echo %%~nxi >> "%PASSFILE%"
                @Echo EPUB �ļ��ɹ����ɣ������� "%MKEPUB_OUTPUT%\%%~ni.epub"
                Echo.
            ) Else (
                Echo.
                Echo ���� EPUB �ļ�ʧ��
                Echo.
                @Echo %%i >> "%FAILEDFILE%"
            )    
            EndLocal
        ) Else (
            Echo.
            Echo ���� HTML �ļ�ʧ��
            Echo.
            @Echo %%i >> "%FAILEDFILE%"            
        )            
    ) Else (
        Echo.
        Echo Ԥ����ʧ�ܣ��� PDF ��ʽ��������
        Echo.
        @Echo %%i >> "%FAILEDFILE%"
    )   
    
)

:END

EndLocal
Pause
