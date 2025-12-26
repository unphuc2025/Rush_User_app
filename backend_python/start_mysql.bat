@echo off
echo Starting MySQL Server on port 3308...
echo.
echo Please make sure MySQL is installed and configured to run on port 3308
echo.
echo If you're using XAMPP, start it from the XAMPP Control Panel
echo If you're using MySQL Workbench, start the MySQL service
echo.
echo After starting MySQL, press any key to test the connection...
pause

python check_mysql.py
