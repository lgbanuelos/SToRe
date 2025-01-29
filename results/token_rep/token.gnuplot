set boxwidth 0.5
set style fill solid

set terminal postscript color size 17cm,10cm
set output "tr_clear.ps"

#set xlabel "Approach" font "cmr10,21"
set ylabel "Time (millisecons.)"	font "cmr10,21"
#set xrange [0:8]
set yrange [0:5]

set style data histogram
set style histogram cluster gap 1
set style fill solid
set boxwidth 0.9
set xtics format ""
set grid ytics
#set key left
set grid
set key font "cmr10,21"
set term pdfcairo font "cmr10,21

red = "#FF0000"; green = "#80BF80"; blue = "#0000FF"; skyblue = "#87CEEB";

plot "results_clear.dat" using 2:xtic(1) title "Token Replay" linecolor rgb green

