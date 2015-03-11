# some model
library(e1071)
library(dplyr)
library(pipeR)

hh <- read.csv('hicre4andric.csv')
names(hh)[5] <- "group"
hh2 <- hh[,5:31]

#tune.hh <- tune(svm, group~., data=hh2, kernel="polynomial", ranges=list(cost=c(.001,.01,1,10,100)))
#tune.hh <- tune(svm, group~., data=hh2, ranges=list((cost=c(.001,.01,1,10,100)), kernel=c("polynomial", "sigmoid", "radial")))

train = sample(1:dim(hh2)[1],dim(hh2)[1]/2)


tune.hh <- tune(svm, group~., data=hh2[train,], ranges=list((cost=c(.001,.01,1,10,100)), kernel=c("polynomial", "sigmoid", "radial"), gamma=c(.01,.1,.5,1,2)))
bestmod <- tune.hh$best.model

svm.hh <- svm(group~., data=hh2, kernel="sigmoid", cost=1, cross=5)


hdf <- tbl_df(hh2)
filter(hdf, group=='CB')[,2:27] %>>% unlist() %>>% plot(,col=2)
filter(hdf, group=='LB')[,2:27] %>>% unlist() %>>% points(,col=3)
filter(hdf, group=='scb')[,2:27] %>>% unlist() %>>% points(,col=4)
filter(hdf, group=='slb')[,2:27] %>>% unlist() %>>% points(,col=5)


