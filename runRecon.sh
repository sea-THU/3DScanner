cd recode
python3 train.py --group=web --model=barf --yaml=barf_myphone --name=web --data.scene=web --barf_c2f=[0.1,0.5]
python3 evaluate.py --group=web --model=barf --yaml=barf_myphone --name=web --data.scene=web --resume
