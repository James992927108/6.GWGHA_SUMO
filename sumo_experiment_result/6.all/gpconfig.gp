reset
set title font ",16"
set title "Taipei\-500"
set xlabel "Evaluation"
set ylabel "Seconds"
set xrange [0:30000]
set terminal pdf
set output "/mnt/f/GoogleDriver(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/6.all/30_750_40/taipei/500/taipei_500_waiting_time.pdf"
set size 1.0,1.0
set pointsize 0.2
set ylabel offset character 1,0,0
set grid xtics ytics
set key outside horizontal center bottom Left reverse
set key spacing 1
set key width 2
set terminal pdf font "Times New Roman, 12"
set style line 1 lc rgb 'blue'     lt 1 lw 1 pt 7 pi -5000 ps 1
set style line 2 lc rgb 'red'      lt 1 lw 1 pt 2 pi -5000 ps 1
set style line 3 lc rgb 'green'    lt 1 lw 1 pt 4 pi -5000 ps 1
set style line 4 lc rgb 'black'    lt 1 lw 1 pt 6 pi -5000 ps 1
set style line 5 lc rgb 'orange'   lt 1 lw 1 pt 8 pi -5000 ps 1
plot "/mnt/f/GoogleDriver(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/6.all/30_750_40/taipei/500/gwgha_025_waiting_time.dat" using 1:2 with linespoints title '   GWGHA'   ls 1,\
     "/mnt/f/GoogleDriver(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/6.all/30_750_40/taipei/500/gwo_waiting_time.dat" using 1:2 with linespoints title '   GWO'   ls 2,\
     "/mnt/f/GoogleDriver(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/6.all/30_750_40/taipei/500/pso_TL_waiting_time.dat" using 1:2 with linespoints title '   PSO\_TL'   ls 3,\
     "/mnt/f/GoogleDriver(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/6.all/30_750_40/taipei/500/spso2011_waiting_time.dat" using 1:2 with linespoints title '   SPSO2011'   ls 4,\
     "/mnt/f/GoogleDriver(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/6.all/30_750_40/taipei/500/vector_goa_waiting_time.dat" using 1:2 with linespoints title '   GOA'   ls 5,\
