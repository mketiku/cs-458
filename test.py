from __future__ import absolute_import
# import vigenere_b
import re


from vigenere_b import decrypt as vdecrypt

text = "JZOLGHA IVFI ITK ZS, TORX XPK DTZMY VY XPK VVIIT, INX BNL MVCK VGIA YATC, TORX EV UJMSXAZ HR GUBK JIIL."

text = re.sub('( )(,)','',text)

# text = text.replace(" ","")

print(text)

res = vdecrypt(text,"eight")
print(res)