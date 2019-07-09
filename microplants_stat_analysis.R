scrupped<-read.csv(file.choose(),header=TRUE)
#I read in scruppedData which is the output of our cleaning file
scrupped<-as.data.frame(scrupped)
data=scrupped[,7:9]
attach(data)
factor(age_group)
factor(validity)
good_kid=sum(validity=="Good" & age_group=="10 and Under" & in_time_range=="In")
bad_kid=sum(validity=="Bad" & age_group=="10 and Under" & in_time_range=="In")
good_teen=sum(validity=="Good" & age_group=="11-17 years" & in_time_range=="In")
bad_teen=sum(validity=="Bad" & age_group=="11-17 years" & in_time_range=="In")
good_adult=sum(validity=="Good" & age_group=="18+" & in_time_range=="In")
bad_adult=sum(validity=="Bad" & age_group=="18+" & in_time_range=="In")

data.df<-as.data.frame(matrix(,nrow=6,ncol=3))
split_age_lev=strsplit(levels(age_group),"\t")
split_age_lev<-split_age_lev[-4]
split_valid_lev=strsplit(levels(validity),"\t")

#input data into a dataframe with the appropriate structure to run a binomial test
data.df<-as.data.frame(matrix(,nrow=3,ncol=3))
freq=c(good_kid, bad_kid, good_teen, bad_teen, good_adult,bad_adult)
names(data.df)=c("Ages","Good","Bad")
f_count=1
for (i in 1:length(split_age_lev))
{
  data.df[i,1]=split_age_lev[[i]]
  for (j in 2:3)
  {
    data.df[i,j]=freq[f_count]
    f_count=f_count+1
  }
}
attach(data.df)
output=glm(formula=cbind(Good,Bad)~Ages, family=binomial)
summary(output)

#computing the odds ratio
c_t=exp(0.45647)-1
c_a=exp(1.0861)-1
t_a=exp(1.0861-.45647)-1
c_t
c_a
t_a
