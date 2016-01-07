## exam question: explain what happens here. 
splitlocation <- function(x) {
    coords <- data.frame(do.call(rbind, lapply(strsplit(as.character(x), "/"), as.numeric)))
    names(coords) <- c("long", "lat", "zoom")
    coords
}
