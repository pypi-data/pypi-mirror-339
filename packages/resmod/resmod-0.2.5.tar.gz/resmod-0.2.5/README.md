# resmod: A package for deriving orthogonalized interaction terms, reporting interaction analyses, and visualization of interactions

## Overview
**resmod** is a Python package to assist with deriving interactions and visualizing interactions. For deriving interactions - this package uses residual centering to orthogonalize the interaction from the items used to derive the interaction. Where traditional interaction approaches induce residual dependence that violate assumptions of regression and requires the user to estimate a model with and without the interaction, the approach taken with 'resmod' is an interaction term that does not violate assumptions of regression based approaches (no residual dependence). 

Why would you want to orthogonalize your interaction term by residual centering? Beyond retaining data properties that fit the assumptions of your analytic approach, this improves the ease of analysis as well as providing proper context to analyses that are preregistered. 

An example - you preregister an interaction that has strong theoretical support,  you run your analysis and find your interaction is statistically meaninful! Now it is time to interpret - a traditional approach would guide the analyst to forget about the direct estimates and only interpret the interaction... the problem is those direct effects are what guided you to your research question and proposing the interaction in the first place. 'resmod' allows you to leave your interaction term in your model, show your hypothesis test for the interaction, while also connecting to the literature in your field by being able to interpret direct effects. It would be critical to not only intprepret the interaction but also direct effects that has substantially more literautre support inorder to contextualize your results. 

A second example - your preregistered interaction is not statitically menaingful. A traditional approach would guide you to remove the interaction and move forward with interpreting direct effects... the problem with this approach is you had a strong theoretical reasoning for that interaction  and to remove it would undercut the main reason for conducting the analysis in the first place. 'resmod' allows you to leave that interaction term in the model so you can show your hypothesis test for the theoretically supported interaction term while interpretating direct effects to connect with the literature. 

Another common problem is writing code to plot these interactions and obtaining slope estimates at the points of interaction. 'resmod' provides basic plotting functions to visualize interactions as well as calculating simple slopes for two-way and three-way interactions for inspection or publication. 

In short 'resmod' provides tools for more robust interaction analysis that are more theoretically consistent without having to run multiple models on the same outcome and knowningly introducing assumption violations.  

## What is resmod? 
**resmod** is a Python package that provides the ability to quickly create orthogonalized interaction terms by centering residuals. This approach to testing interaction prevents the user from violating basic assumptions of regression -- specificaly that there should be no correlated residuals. Because the interaction term is orthogonalized from the model, you are able to interpret both direct effects and interaction terms in the same model. Not only is this convienient but it reduces the number of test run on your data. **resmod** also provides functionality to visualize two-way or three-way interactions for one or two interactions. Specifically, 'resmod.plotting.interact_plot()' uses the Bauer & Curran (2005) "pick a point" procedure (+1SD, mean, -1SD) for continuous variables (or chosen point values by the user) and points relevant for categorical or dichotomous values.     

## Whats next?
For the next version of **resmod** we are working on functions for bootstrapping of confidence intervals and deriving Johnson-Neyman intervals as well as related figures for evaluating/report for these approaches. 

## Tutorial
- [Collab Notebook](https://colab.research.google.com/drive/11wag0el3kHMiDKBE0ioyE2K8jLbW5hdJ?usp=sharing)

## Citations:
- Aiken, L. S., & West, S. G. (1991). *Multiple Regression: Testing and Interpreting Interactions*. Newbury Park, CA: Sage.
- Bauer, D. J., & Curran, P. J. (2005). Probing interactions in fixed and multilevel regression: Inferential and graphical techniques. Multivariate behavioral research, 40(3), 373-400.
- Cohen, J., Cohen, P., West, S. G., & Aiken, L. S. (2003). *Applied Multiple Regression/Correlation Analysis for the Behavioral Sciences* (3rd ed.). Mahwah, NJ: Lawrence Erlbaum Associates.
- Hayes, A. F. (2013). *Introduction to Mediation, Moderation, and Conditional Process Analysis: A Regression-Based Approach*. Guilford Press. 
- Little, T. D., Card, N. A., Bovaird, J. A., Preacher, K. J., & Crandall, C. S. (2007). Structural equation modeling of mediation and moderation with contextual factors. Modeling contextual effects in longitudinal studies, 1, 207-230.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.
- Wilkinson, L., & Friendly, M. (2009). The History of the Cluster Heat Map. *The American Statistician*, 63(2), 179–184.

### Functions
- **residual_center** 
	- Two-way orthogonalized interaction that can be use in any regression-based model
- **three_center** 
	- Three-way orthogonalized interaction that can be used in any regression-based model
- **orthogonalize** 
	- Multiple orthogonalized interactions to be used in latent SEM interaction modeling
- **interact_plot**
    - A visualization tool for plotting two-way and three-way interactions 
- **simple_slopes**
    - Simple slopes calculated for two-way and three-way interactions

### Installation

```
# git
git clone https://github.com/drewwint/resmod.git
cd resmod
pip install . 

```

```
# PyPi
pip install resmod

```

### Dependencies
- [NumPy](https://www.numpy.org)
- [pandas](https://pandas.pydata.org)
- [statsmodels](https://www.statsmodels.org)
- [SciPy](https://scipy.org/)
- [matplotlib](https://matplotlib.org/)
- [patsy](https://patsy.readthedocs.io/en/latest/)

### Usage 

```
# residual_center: Orthogonalizing single two-way interaction from Ducan data
  ## Packages
    from resmod.single import residual_center         # for orthogonalizing 
    import statsmodels.formula.api as smf             # for estimation 
    import statsmodels as sms             
    from statsmodels import datasets                  # for importing data
    import numpy as np                                # for data structring
    import pandas as pd                               # for dataframe 
    
  ## Getting data
    duncan_prestige = sms.datasets.get_rdataset("Duncan", "carData")
    income = duncan_prestige.data.income
    education = duncan_prestige.data.education
    
  ## Creating dataframe
    v1 = np.array(income)                             # ensure v1 is an array
    v2 = np.array(education)                          # ensure v2 is an array 
    dat = pd.DataFrame({"income": v1, "education" : v2})
  
  ## Estimation 
    residual_center(dat.income, dat.education)
  
  ## Returns
    #array([ 63.11264837,    229.8491846,    741.28285426,  -191.61545996,  143.13497759, 
    #       -1522.02012271,  250.49755451,   1222.03876523,  281.50598242,  463.22429449,  
    #       -657.16077574,   951.3190848 ,   923.98157381,  -761.79683046, -500.35610126,  
    #       -798.28161848,  -474.82578368,  -357.03501052,  -457.2861054 ,  585.94123821,
    #       -981.98093767,  -476.50649685,  -312.02816875,  -549.40617942,  165.39170698,  
    #       -458.91783728,  -1052.25086135, -293.40322494,   169.06536061, -372.67648496,   
    #        101.34978524,   1153.8352266,  -337.3613032,    599.90768769,  386.69161908,   
    #        248.37917402,   182.34841689,   117.02343887,   679.23266571,  360.97604371,
    #        115.6538024,    194.02207051,   612.22286945,  -485.36288933,  98.28416593]
    #        )
```

```
# orthogonalize: Orthogonalizing two list of variables from Duncan data
   ### Output could be used for multiple orthogonalized interactions or
   ### to create interactions of all observed variables to be used in a latent interaction

 ## Packages
      from resmod.sem import orthogonalize
      import statsmodels.formula.api as smf
      import statsmodels as sms
      from statsmodels import datasets
      import numpy as np
      import pandas as pd

 ## Getting data
      duncan_prestige = sms.datasets.get_rdataset("Duncan", "carData")
      income = duncan_prestige.data.income
      education = duncan_prestige.data.education

 ## Creating dataframe
      income = np.array(duncan_prestige.data.income)
      education = np.array(duncan_prestige.data.education)
      prestige = np.array(duncan_prestige.data.prestige)
      dat = pd.DataFrame({"income": income, "education": education, "prestige": prestige})

 ## Creating lists of column names for interactions 
    ## You could include any number variables in each list for your purposes 
      l1 = ["income"]
      l2 = ["education", "prestige"]


 ## Estimation
      r = orthogonalize(l1, l2, dat)
      r.head()

 ## Returns 
   # Dataframe
   #     income.education  income.prestige
   #  0         63.112648        34.246807
   #  1        229.849185       399.315757
   #  2        741.282854       732.789351
   #  3       -191.615460      -277.473163
   #  4        143.134978       276.041595

```

### Comparative testing
In addition to each functions testing files, we replicated results from functions in r packages including:
- [rockchalk](https://cran.r-project.org/web/packages/rockchalk/rockchalk.pdf)
- [semTools](https://cran.r-project.org/web/packages/semTools/semTools.pdf)
- [interactions](https://doi.org/10.32614/CRAN.package.interactions)


### Contributing to resmod

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

