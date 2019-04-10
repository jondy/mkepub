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
Set OUTPUT=%~dp1

REM TODO: ���ñ༭��������·����Ĭ���ǵ�ǰ�ű����ڵ�·����������·��
Set MKEPUBPATH=%~dp1\..\..

REM TODO: ���� ghostscript �ű�
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
    Echo  �Ҳ��� %GS% �������ذ�װ http://yancloud.red/downloads/gs927w64.exe
    Echo.
    Goto END
)

If NOT EXIST "%INPUTFILE%" (
    Echo.
    Echo  �����ļ� %INPUTFILE% ������
    Echo.
    Goto END
)

If NOT EXIST "%MKEPUBPATH%\%MKEPUB%" (
    Echo.
    Echo  �Ҳ����༭���ߣ������ذ�װ http://yancloud.red/downloads/yanhong-editor.exe
    Echo.
    Goto END
)

FOR /F "" %i IN (%INPUTFILE%) DO (
    @Echo ��ʼ���� %i ...
    @Echo %filename% >> %RESULTFILE%
    
    Set filename=%~ni
    Set logfile=%LOGPATH%\%filename%.log
    
    @Echo �ļ����� %filename%
    @Echo �����־��  %logfile%
    
    @Echo ��ʼ�� pdf �ļ�����Ԥ���� ...
    %GS%  -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dDetectDuplicateImages=true -o %PDFPATH%/%filename% %filename% >> %logfile% 2>&1
    If NOT ERRORLEVEL 0 (
        Echo.
        Echo Ԥ����ʧ�ܣ��� PDF ��ʽ��������
        Echo.
        @Echo %filename% Ԥ����ʧ�� >> %FAILEDFILE%
        Goto END
    )
    @Echo Ԥ����ɹ����������ļ�����Ϊ %PDFPATH%/%filename%
    
    @Echo ��������ǰ 5 ҳ�� HTML �ļ�
    %PDF2HMLT% --last-page 5 %PDFPATH%/%filename% %filename%.html >> %logfile% 2>&1
    
    If NOT ERRORLEVEL 0 (
        Echo.
        Echo ���� HTML �ļ�ʧ��
        Echo.
        @Echo %filename% ���� HTML �ļ�ʧ�� >> %FAILEDFILE%
        Goto END
    )    
    MOVE /Y %filename%.html %HMTLPATH%
    @Echo ���ɵ� HTML �ļ������� %HMTLPATH%/%filename%.html
    
    SetLocal
        @Echo �л���·�� %MKEPUBPATH%
        CD /D %MKEPUBPATH%
        
        @Echo ��ʼ���� EPUB ...
        %MKEPUB% %PDFPATH%/%filename% >> %logfile% 2>&1
        If NOT ERRORLEVEL 0 (
            Echo.
            Echo ���� EPUB �ļ�ʧ��
            Echo.
            @Echo %filename% ���� EPUB �ļ�ʧ�� >> %FAILEDFILE%
            Goto END
        )    
        
        @Echo %filename% >> %PASSFILE%
        @Echo EPUB �ļ��ɹ����ɣ������� %MKEPUBPATH%/output
    
    EndLocal
)

:END

EndLocal
Pause
