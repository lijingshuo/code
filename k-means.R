library(foreign)
library(rms)
library(tableone)
library(broom)
library(pROC)
library(regplot)
library(ResourceSelection)
library(nricens)
library(PredictABEL)
library(ggDCA)
library(caret)
library(survivalROC)
library(nomogramFormula)
library(ggplot2)
library(factoextra)
library(cluster)
 
library(fpc)

setwd("D:/7R")
log<-read.spss("my file.sav",to.data.frame = T)
str(log)


log <- scale(log)


fviz_nbclust(log, kmeans, method = "silhouette")



#make this example reproducible
set.seed(1)

#perform k-means clustering with k = 4 clusters
km <- kmeans(log, centers = 2, nstart = 25)

#view results
km

#plot results of final k-means model
fviz_cluster(km, data = log,
             palette = c("#00AFBB", "#ED7D31"),
             ellipse.type = "euclid",
             star.plot = TRUE,
             repel = TRUE,
             ggtheme = theme_minimal()
)
#add cluster assigment to original data
final_data <- cbind(log, cluster = km$cluster)

#view final data
head(final_data)



