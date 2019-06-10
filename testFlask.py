# -*- coding: utf-8 -*-

import re
text = "Please contact us at contact@tutorialspoint.com for further information."+\
        " You can also give feedbacl at feedback.hntv@tp.com or 0358949730"
text2 = "xe con bán\n \
        Giá: 10000 không thiếu\n \
        liên hệ: 0358949730"


emails = re.findall(r"[\w\.-]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
phoness = re.findall(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", text)
gia = re.findall(r"giá: \b\d+\b", text2.lower())
print(emails[0])
print(gia[0])
print(phoness[0])