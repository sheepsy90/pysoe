# pysoe

This is a wrapper for the Soft Ordinal Embedding written in python.

\begin{center}
	\tiny{
		\begin{tabular}{|p{4cm}|p{7cm}|p{2cm}|}
			\hline
			\textbf{URI}                    & /soe/schedule   &\\\hline
			\textbf{Method}                 & POST            &\\\hline\hline
			\textbf{Parameter}              & \textbf{Meaning}                                   & default value \\\hline
			\verb|comparison_file|          & Path to a file where the comparisons are stored    & \textit{necessary}\\
			\verb|object_count|             & The number of objects that should be embedded      & \textit{necessary}\\
			\verb|embedding_dimensions|     & The dimensionionality that should be embedded to   & 2 \\
			\verb|max_iterations|           & The maximum number of iterations                   & 1000 \\\hline\hline
			\textbf{Returns}                & \textbf{Meaning}                                   \\\hline
			\verb|job_id|                   & The id with which the job is being registered \\\hline\hline
			\textbf{Error Codes}            &&\\
			\verb|202_ACCEPTED|                & &\\
			\verb|405_METHOD_NOT_ALLOWED|      & &\\
			\verb|412_PRECONDITION_FAILED|     & &\\
			\verb|415_UNSUPPORTED_MEDIA_TYPE|  & &\\
			\verb|503_SERVICE_UNAVAILABLE|     & &\\\hline
		\end{tabular}
	}
	\\[2ex]
	\tiny{
		\begin{tabular}{|p{4cm}|p{7cm}|p{2cm}|}
			\hline
			\textbf{URI}                    & /soe/\verb|schedule_state|/\verb|<string:process_id>|   &\\\hline
			\textbf{Method}                 & GET                                       &\\\hline\hline
			\textbf{Parameter}              & \textbf{Meaning}                                          & default value \\\hline
			\verb|<string:process_id>|      & The job id that was returned when the job was scheduled   & \textit{necessary}\\\hline\hline
			\textbf{Returns}                & \textbf{Meaning}                                      \\\hline
			\verb|success|                  & Is \textbf{true} if the computing was without errors          \\
			\verb|error_message|            & Holds the error message if present                            \\
			\verb|embedding_file|           & The path to the file holding the embedding result             \\
			\verb|iterations_file|          & The path to the file holding the algorithm iteration steps    \\\hline\hline
			\textbf{Error Codes}            &   &\\\hline
			\verb|201_CREATED|              &   &\\
			\verb|204_NO_CONTENT|           &   &\\
			\verb|404_NOT_FOUND|            &   &\\
			\verb|405_METHOD_NOT_ALLOWED|   &   &\\\hline
		\end{tabular}
	}
\end{center}
