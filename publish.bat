cd D:\CodeAndDrive\

rmdir /S /Q .sass-cache
rmdir /S /Q _site
mkdir _site

"C:\Program Files\7-Zip\7z.exe" a -r -y ..\CodeAndDrive.zip *

call jekyll build

move ..\CodeAndDrive.zip _site/.
xcopy _site\* D:\git\soolek.github.io\. /E /C /H /R /Y

cd D:\git\soolek.github.io
git add .
git commit -m %date%
git push
cd D:\CodeAndDrive\