sshfs pi@192.168.0.150: ~/pi -o nonempty
rsync -avzh * /home/simonque/pi/BLAST_lab/ --exclude .git --exclude node_info.py
