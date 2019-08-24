set key right top Left reverse width 0 box 3
set xlabel "Data sets"
set ylabel "Time"
# set ytics 0, 500
# set mytics 5
set output "Time.png"

set grid
set boxwidth 0.9 absolute
set style fill solid 1.00 border -1
set style histogram clustered gap 1 title offset character 0, 0, 0
set style data histograms
set terminal png size 1024, 512 font "Times New Roman, 12"
# set key box
set key outside horizontal center bottom Left reverse
# set key spacing 1
# set key width 2

plot 'test.dat' using 2:xtic(1) title col,\
      '' u 3 title col,\
      '' u 4 title col,\
      '' u 5 title col,\
      '' u 6 title col
