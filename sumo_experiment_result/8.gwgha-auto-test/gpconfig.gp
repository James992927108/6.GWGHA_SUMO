reset
set title font ",16"
set title "Taichung\-500"
set xlabel "Evaluation"
set ylabel "Seconds"
set xrange [0:30000]
set terminal pdf
set output "/mnt/c/GoogleDrive(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/8.gwgha-auto-test/taichung/500/taichung_500_waiting_time.pdf"
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
plot "/mnt/c/GoogleDrive(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/8.gwgha-auto-test/taichung/500/gwgha_025_waiting_time.dat" using 1:2 with linespoints title '   GWGHA-025'   ls 1,\
     "/mnt/c/GoogleDrive(FCU)/Github/school/gwgha-sumo/sumo_experiment_result/8.gwgha-auto-test/taichung/500/gwgha_auto_waiting_time.dat" using 1:2 with linespoints title '   GWGHA-AUTO-20'   ls 2,\
