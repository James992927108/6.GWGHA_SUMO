set xlabel font ",16"
set ylabel font ",16"

set xlabel "Data sets"
set ylabel "Time (Second)"
# set ytics 0, 500
# set mytics 5
set output "Single_Multiprocess.png"

set grid
set boxwidth 0.9 absolute
set style fill solid 1.00 border -1
set style histogram clustered gap 1 title offset character 0, 0, 0
set style data histograms
set terminal png size 1024, 512 font "Times New Roman, 14"
set grid xtics ytics
set key outside right bottom horizontal Left reverse width -4
# set key box lw 1
# set key right top 
plot 'test.dat' using 2:xticlabels(1) title columnheader(2),\
      '' using 3:xticlabels(1) title columnheader(3),\
      '' using ($0-1.1):($2+20000):2 with labels title ' ', \
      '' using ($0-0.7):($3+20000):3 with labels title ' ', \