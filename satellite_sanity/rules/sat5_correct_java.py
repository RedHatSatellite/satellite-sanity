#!/usr/bin/env python
# -*- coding: UTF-8 -*-

tags = ['Satellite_5']
name = 'Correct Java JVM is used'

def main(data):
  if not data['alternatives_display_java'] is None:
    # Determine where link currently points to
    java_alternative = None
    for line in data['alternatives_display_java']:
      if line.startswith(' link currently points to '):
        java_alternative = line.split()[-1]
        break
    # Evaluate
    if java_alternative:
      if not java_alternative.startswith('/usr/lib/jvm/jre-1.6.0-ibm.'):
        return {'java_alternative': java_alternative}
    else:
      return {'error': 'No java installed or alternatives system missing/missbehaves?'}

def text(result):
  out = ""
  out += "Satellite 5 is supposed to use only IBM Java 1.6.0.\n"
  if 'java_alternative' in result:
    out += "You have '%s' instead.\n" % result['java_alternative']
  out += "Please make sure correct Java is installed and configured\n"
  out += "as default with alternatives system."
  return out
