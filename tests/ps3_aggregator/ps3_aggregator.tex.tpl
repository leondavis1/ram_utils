\documentclass[a4paper]{article}

\usepackage{graphicx,multirow}
\usepackage{subfigure,amsmath}

\addtolength{\oddsidemargin}{-.675in} 
\addtolength{\evensidemargin}{-.675in} 
\addtolength{\textwidth}{1.7in} 
\addtolength{\topmargin}{-.55in} 
\addtolength{\textheight}{1.55in} 

\usepackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\lhead{PS3 Aggregate Report v 1.0}
\chead{PS3}
\rhead{Date created: <DATE>}
\begin{document}

\section*{\hfil PS3 Region $\times$ Burst Frequency Analysis \hfil}

\begin{figure}[!h]
\centering
\subfigure{\includegraphics[scale=0.4]{<FREQUENCY_PLOT_FILE>}}
\end{figure}

\begin{figure}[!h]
\centering
\subfigure{\includegraphics[scale=0.4]{<FREQUENCY_PROJECTION_PLOT_FILE>}}
\end{figure}

\textbf{\hfil Experiment count \hfil}

\begin{tabular}{|l|c|c|c|c|c|c|}
<REGION_FREQUENCY_EXPERIMENT_COUNT_TABLE>
\end{tabular}

\clearpage

\section*{\hfil Number of collected PS3 sessions per region \hfil}

\begin{tabular}{|l|r|}
\hline Region & \# of sessions \\
\hline <REGION_SESSION_TOTAL_DATA>
\hline
\end{tabular}


\end{document}
