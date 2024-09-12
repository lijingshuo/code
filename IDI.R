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

setwd("D:/7R")
log<-read.spss("my file.sav",to.data.frame = T)
str(log)

model<- glm(LP~tumor diameter+clusterlabel, data=log, family='binomial'(link = "logit"),x=T)
log$premodel<-predict(newdata=log,model,"response")
#View(log)
model2<- glm(LP~tumor diameter+clusterlabel+radiomicslabel, data=log, family='binomial'(link = "logit"),x=T)
log$premodel2<-predict(newdata=log,model2,"response")
#View(log)


pold<- model$fitted.values

pnew<-model2$fitted.values

reclassification(data = log,cOutcome = 1,predrisk1 = pold,predrisk2 = pnew,cutoff = c(0,033,1))









