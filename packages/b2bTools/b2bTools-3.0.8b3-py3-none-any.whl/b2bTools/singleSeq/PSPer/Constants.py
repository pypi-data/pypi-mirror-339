import os
import warnings
import subprocess

hmmbuild_bin = 'hmmbuild'
hmmscan_bin = 'hmmsearch'

try:
  from b2bTools.singleSeq.PSPer.localConstants import hmmbuild_bin
  from b2bTools.singleSeq.PSPer.localConstants import hmmscan_bin
except:
  pass

# NOTE: this will not work on Windows, fix this to be more generic
which_hmmbuild_returncode = subprocess.call(['which', hmmbuild_bin], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

if which_hmmbuild_returncode != 0:
  warnings.warn("""
PSPer can only run if HMMER is installed.
Please install it from http://hmmer.org on your computer, and refer to this installation in the
   b2bTools/python/b2bTools/singleSeq/PSPer/Constant.py
file by pointing the hmmbuild_bin and hmmscan_bin variables at the binaries.""")