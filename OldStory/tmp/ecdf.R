o <- read.csv("original.csv", header = FALSE, stringsAsFactor = FALSE)
d <- read.csv("dropped.csv", header = FALSE, stringsAsFactor = FALSE)
o <- o$V1
d <- d$V1

fo <- ecdf(o)
fd <- ecdf(d)

mato <- cbind(unique(o), fo(unique(o)))
matd <- cbind(unique(d), fd(unique(d)))
write.csv(mato, file = "ecdf_original.csv")
write.csv(matd, file = "ecdf_dropped.csv")
