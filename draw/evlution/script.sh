#"""first, need to clear origin date"""
# cd ..
# find evlution/ -name *.dat |xargs rm -rf
# find evlution/ -name *.pdf |xargs rm -rf
# cd evlution
# """second, change name, only to once"""

# python change_name.py

# """finally, generate gnuplot fig"""
python get_gnuplot.py
