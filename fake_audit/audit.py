#!/usr/bin/env python
# 1649632953.109:5060707
# -pe: 原位编辑 -e execute comand in cmd line in instead of in scripts; -p: traverse file implicity, mean while print all lines
# (\d+): stand for number
# tail -f /var/log/audit/audit.log | sed -re 's/(^.+)([0-9]{10})(.+$)/echo "\1"`date -d @\2 +%Y-%m-%d_%H:%M:%S`"\3"/e'
# tail -f /var/log/audit/audit.log | perl -pe 's/(\d{10})/`echo -n \`date -d \@$1 +%Y-%m-%d_%H:%M:%S\``/e'
# tail -f /var/log/audit/audit.log | perl -pe 's/(\d+)/localtime($1)/e'
import os
from datetime import datetime
from datetime import timedelta
import random
import re
import io
class Getoutofloop(Exception):
    pass

regex = re.compile(r"audit\([\S]+:[\S]+\):", re.IGNORECASE)
date_input = '21/4/22 12:46:01'
aid = 17214346
fext = 1
max_size = 8 *1024 * 1024
aid_step = [1]+[0]*8
given_time = datetime.strptime(date_input, '%d/%m/%y %H:%M:%S')
end_time = given_time - timedelta(days=186) #6 months
print("The end_time is: \n",end_time)
try:
    t_count = 0
    for root, dirs, files in os.walk("audit", topdown=False):
        for name in files:
            sample_file = os.path.join(root, name)
            s_file = open(sample_file, 'r')
            lines = s_file.readlines()
            count = len(lines)
            target_file = os.path.join("output","audit.log.%d"%fext)
            f = open(target_file, 'a')
            for line in lines:
                m = random.randint(0, 0)
                n = random.randint(0, 3)
                final_time = given_time - timedelta(minutes=m,seconds=n)
                ts = final_time.timestamp() + random.uniform(0,1)
                aid = aid - random.choices(aid_step, k=1)[0]
                mo = "audit(%.2f:%d):"%(ts, aid)
                out_line = regex.sub(mo, line)
                # 开始写文件
                f.write(out_line)
                given_time = final_time
                t_count = t_count + 1
                count = count -1
                if f.tell() >= max_size:
                    print("end %s file %d %s"%(given_time,aid,target_file))
                    fext = fext + 1
                    break
                if given_time < end_time:
                    f.close()
                    stat = os.stat(target_file)
                    os.utime(target_file, times=(ts, ts))
                    raise Getoutofloop()
            f.close()
            stat = os.stat(target_file)
            os.utime(target_file, times=(ts, ts))
except Getoutofloop:
    print("end process")
