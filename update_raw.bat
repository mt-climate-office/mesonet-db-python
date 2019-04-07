@echo on
call conda activate mesonet
call python C:\MCO\Mesonet\py\Mesonet-DB\update_raw.py
call conda deactivate
