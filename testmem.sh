ps -fu $USER|grep "flask run"|grep -v grep|awk '{print $2}'|./testmem.py
