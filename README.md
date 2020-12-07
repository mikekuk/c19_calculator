# c19_calculator

This code was desgined to calculate the esitmated comunity spread of COVID-19 in the ABUHB region at the start of the COVID-19 pendemic. It used know data points to find the best fit of all avlible models, then caluclated the average error and used this to estimate the unknown values. 

At the time, the day 0 was still unkown, and there was insufficent testing to understad comunity spread.

Models only provided estimated data points each week. I used high order polynomials to caluclate day by day datapoints.

I now know this code has many erorrs, and stopped developing it. For furhter use, it all vlaues should ne normalised prior to caluclations. 