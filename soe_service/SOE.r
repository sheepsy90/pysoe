library(loe)

args <- commandArgs(trailingOnly = TRUE)

hh <- paste(unlist(args),collapse=' ')
listoptions <- unlist(strsplit(hh,'--'))[-1]
options.args <- sapply(listoptions,function(x){
         unlist(strsplit(x, ' '))[-1]
        }, simplify=FALSE)
options.names <- sapply(listoptions,function(x){
  option <-  unlist(strsplit(x, ' '))[1]
})
names(options.args) <- unlist(options.names)

# Parsing the input parameters
N = strtoi(options.args$N)
max_iterations = strtoi(options.args$max_iterations)
dimensions = strtoi(options.args$dimensions)
data_filename = options.args$data_filename

# Loading the Data from the tmp directory
cat("Loading the input file ... \n")
expr = as.matrix(read.csv(data_filename, header=FALSE, sep = ",", blank.lines.skip = TRUE, as.is=TRUE, colClasses = "numeric", allowEscapes=TRUE))
cat("Finished. \n")

num_rows_input = nrow(expr)

cat("Number of Objects", N, "\n")
cat("File to use as input", data_filename, "\n")
cat("Number of Maximum Iterations:", max_iterations, "\n")
cat("Number of dimensions to embed in:", dimensions, "\n")
cat("Number of Rows in the Input:", num_rows_input, "\n")

# Call the SOE function
result <- SOE(CM=expr, N, p=dimensions, c=0.1, maxit=max_iterations, report=1, rnd=num_rows_input)

print("== BEGIN RESULT ==")
result$X
print("== END RESULT ==")