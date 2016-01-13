## solution for miniproject shootings
# (c) 2016 David A. van Leeuwen

read.shootings <- function(file="counted.csv") {
    x <- read.csv(file)
    x
}

## painfull function, data is weirdly encoded
read.votes <- function(file="gevotesbyparty.csv") {
    x <- read.csv(file, skip=3, nrows=56)
    names(x)[1] <- "state" ## for merge later
    ## fix weird "," as 1000-separator in number strings
    for (i in 2:4) {
        x[,i] <- as.numeric(gsub(",", "", x[,i]))
    }
    x
}

shootings <- read.shootings()
## count shootings and convert to dataframe
## nshootings <- as.data.frame(table(state=shootings$state), responseName="nshootings")
nshootings <- data.frame(table(shootings$state))
names(nshootings) <- c("state", "nshootings")
votes <- read.votes()

## database join

m <- merge(nshootings, votes, by="state")
