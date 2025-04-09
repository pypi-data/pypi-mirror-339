#!/usr/bin/python3


def simple_slopes(outcome, pred, modx, data, controls=None, mod2=None, 
                  modx_values=None, modx_legend_labels=None,
                  mod2_values=None, alpha=0.05, 
                  p_value_method="perm", n_boot =1000, n_perm =1000, round_dec = 4):
    """
    Calculate simple slopes for an interaction model along with bootstrapped confindence intervals
    as well as compute p–values using one of four methods: 
      - permutation testing 
      - nonparametric bootstrap (via residual resampling) 
      - Satterthwaite correction
      - Satterthwaite correction on bootstrapped parameters

    The moderated regression model is specified as:
        outcome ~ pred * modx [+ controls]
    For a continuous moderator (modx), if modx_values is not supplied the slopes are
    computed at [mean – SD, mean, mean + SD] (with default row labels "-1SD", "Mean", "+1SD").
    For categorical moderators, the sorted unique values are used.

    If a second moderator (mod2) is provided, the data are sub‐set by mod2 and the simple
    slopes are computed separately for each level. A column "at_mod2_value" is added to
    indicate the mod2 level, and the results from all levels are concatenated into one DataFrame.

    Author
    ------
    Drew E. Winters, PhD. <drewEwinters@gmail.com>

    Parameters
    ----------
    outcome : str
        The outcome variable name.
    pred : str
        The focal predictor variable name.
    modx : str
        The moderator variable name.
    data : pd.DataFrame
        DataFrame containing the data.
    controls : list of str, optional
        List of additional control variable names to include in the model.
    mod2 : str, optional
        A second moderator variable. If provided, simple slopes are computed for each level.
    modx_values : array-like, optional
        Values of modx at which to compute simple slopes. For continuous modx, defaults to
        [mean – SD, mean, mean + SD]; for categorical moderators, defaults to sorted unique values.
    modx_legend_labels : list of str, optional
        Custom labels for the modx conditions. Defaults to ["-1SD", "Mean", "+1SD"] for continuous moderators.
    mod2_values : array-like, optional
        Specific values of mod2 at which to compute simple slopes. If not provided, uses the unique sorted values in data.
    alpha : float, default 0.05
        Significance level (for confidence intervals).
    p_value_method : str, default "perm"
        Method for p–value estimation. Options are:
          - "perm" for permutation testing,
          - "bootstrap" for a nonparametric residual bootstrapping method,
          - "satt" for a Satterthwaite correction.
          - "boot_satt" for bootstrapped parametes used for Satterthwaite correction
    n_perm : int, default 1000
        Number of permutations if p_value_method is "perm".
    n_boot : int, default 1000
    round_dec : int, default 4
        Number of decimal points to round to in the output
        
    Returns
    -------
    result : pd.DataFrame
        A DataFrame with columns:
          - "at_mod2_value" (if mod2 is provided),
          - modx (the modx value at which the slope is computed),
          - "slope", "se", "t", "p", 
          - bootstrapped confidence intervals "ci_lower", "ci_upper",
          - and an additional column for the method-specific p–value:
            "p_perm", "p_boot", or "p_satt" (depending on p_value_method).
        The DataFrame's row index is set according to modx_legend_labels.
    
    Methodology is based on standard moderated regression approaches
    (Aiken & West, 1991; Cohen et al., 2003).
    
    Citations:
      - Aiken, L. S., & West, S. G. (1991). Multiple Regression: Testing and Interpreting Interactions. Sage.
      - Cohen, J., Cohen, P., West, S. G., & Aiken, L. S. (2003). Applied Multiple Regression/Correlation Analysis for the Behavioral Sciences (3rd ed.). Lawrence Erlbaum Associates.
      - Satterthwaite, F.E. (1946), An Approximate Distribution of Variance Components, Biometrics Bulletin, 2: 110-114
    """
    # Required packages import checking
    try:
        import numpy as np
        import pandas as pd
        import statsmodels.formula.api as smf
        import scipy.stats as st
    except ImportError as e:
        raise ImportError(f"Missing required package: {e.name}. Install it using `pip install {e.name}`")
    
    # Helper: Compute simple slopes from a fitted model given a moderator value.
    def compute_slopes(fit, modx_val):
        try:
            b_pred = fit.params[pred]
            b_int = fit.params[f"{pred}:{modx}"]
        except KeyError:
            b_pred = fit.params[pred]
            b_int = fit.params[f"{modx}:{pred}"]
        
        cov = fit.cov_params()
        var_pred = cov.loc[pred, pred]
        if f"{pred}:{modx}" in cov.index:
            var_int = cov.loc[f"{pred}:{modx}", f"{pred}:{modx}"]
            cov_pred_int = cov.loc[pred, f"{pred}:{modx}"]
        else:
            var_int = cov.loc[f"{modx}:{pred}", f"{modx}:{pred}"]
            cov_pred_int = cov.loc[pred, f"{modx}:{pred}"]
        
        slope = b_pred + modx_val * b_int
        se = np.sqrt(var_pred + (modx_val ** 2) * var_int + 2 * modx_val * cov_pred_int)
        # Compute conventional t-value
        t_val = slope / se
        # Use the default degrees of freedom from the fitted model (df_resid) initially.
        df_resid = fit.df_resid
        p_val = 2 * (1 - st.t.cdf(np.abs(t_val), df=df_resid))
        t_crit = st.t.ppf(1 - alpha/2, df=df_resid)
        ci_lower = slope - t_crit * se
        ci_upper = slope + t_crit * se
        return slope, se, t_val, p_val, ci_lower, ci_upper, var_pred, var_int, cov_pred_int, df_resid

    # Determine modx values and corresponding labels.
    if data[modx].dtype.kind in 'biufc' and data[modx].nunique() > 2:
        if modx_values is None:
            modx_mean = data[modx].mean()
            modx_std = data[modx].std()
            modx_values = [modx_mean - modx_std, modx_mean, modx_mean + modx_std]
            if modx_legend_labels is None:
                modx_legend_labels = ["-1SD", "Mean", "+1SD"]
        else:
            if modx_legend_labels is None:
                modx_legend_labels = [str(val) for val in modx_values]
    else:
        if modx_values is None:
            modx_values = sorted(data[modx].unique())
        if modx_legend_labels is None:
            modx_legend_labels = [str(val) for val in modx_values]
    
    # Build model formula.
    formula = f"{outcome} ~ {pred} * {modx}"
    if controls is not None and len(controls) > 0:
        formula += " + " + " + ".join(controls)
    
    # Define inner function to process a data subset and return a DataFrame.
    def process_data(df):
        fit = smf.ols(formula, data=df).fit()
        rows = []
        for val in modx_values:
            slope, se, t_val, p_val, ci_lower, ci_upper, var_pred, var_int, cov_pred_int, df0 = compute_slopes(fit, val)
            boot_slopes = []
            boot_ts = []
            boot_var_pred = []
            boot_var_int = []
            boot_cov_pred_int = []
            # Use nonparametric residual resampling:
            fitted_vals = fit.fittedvalues
            residuals = fit.resid
            n_obs = len(residuals)
            count = 0
            for i in range(n_boot):
                resampled = np.random.choice(residuals, size=n_obs, replace=True)
                boot_outcome = fitted_vals + resampled
                boot_df = df.copy()
                boot_df[outcome] = boot_outcome
                fit_boot = smf.ols(formula, data=boot_df).fit()
                slope_boot, _, t_boot, _, _, _, var_pred_boot, var_int_boot, cov_pred_int_boot, _ = compute_slopes(fit_boot, val)
                boot_slopes.append(slope_boot)
                boot_ts.append(t_boot)
                boot_var_pred.append(var_pred_boot)
                boot_var_int.append(var_int_boot)
                boot_cov_pred_int.append(cov_pred_int_boot)
            boot_slopes = np.array(boot_slopes)
            boot_ts = np.array(boot_ts)
            boot_var_preds = np.array(boot_var_pred)
            boot_var_ints = np.array(boot_var_int)
            boot_cov_pred_ints = np.array(boot_cov_pred_int)
            ci_lower = np.percentile(boot_slopes, alpha/2 * 100)
            ci_upper = np.percentile(boot_slopes, (1 - alpha/2) * 100)
            # Compute method-specific p–value.
            if p_value_method == "perm":
                count = 0
                for i in range(n_perm):
                    perm_df = df.copy()
                    perm_df[outcome] = np.random.permutation(perm_df[outcome].values)
                    fit_perm = smf.ols(formula, data=perm_df).fit()
                    slope_perm, _, _, _, _, _, _, _, _, _ = compute_slopes(fit_perm, val)
                    if np.abs(slope_perm) >= np.abs(slope):
                        count += 1
                p_method = (count + 1) / (n_perm + 1)
                p_label = "p_perm"
            elif p_value_method == "bootstrap":
                boot_slopes_centered = ((boot_slopes - np.mean(boot_slopes)))
                p_method = np.mean(np.abs(boot_slopes_centered) >= np.abs(slope))
                p_label = "p_boot"
            elif p_value_method == "satt":
                # Compute V and then the Satterthwaite degrees of freedom.
                V = var_pred + (val**2)*var_int + 2*val*cov_pred_int
                df_satt = df0 * (V**2) / ((var_pred)**2 + (val**4)*(var_int)**2 + 4*(val**2)*(cov_pred_int)**2)
                p_method = 2 * (1 - st.t.cdf(np.abs(t_val), df=df_satt))
                p_label = "p_satt"
            elif p_value_method == "boot_satt":
                # Compute V and then the Satterthwaite degrees of freedom.
                V = np.mean(boot_var_preds) + (val**2)*np.mean(boot_var_ints) + 2*val*np.mean(boot_cov_pred_ints)
                df_satt = df0 * (V**2) / ((np.mean(boot_var_preds))**2 + (val**4)*(np.mean(boot_var_ints))**2 + 4*(val**2)*(np.mean(boot_cov_pred_ints))**2)
                p_method = 2 * (1 - st.t.cdf(np.mean(np.abs(boot_ts)), df=df_satt))
                p_label = "p_boot_satt"
            else:
                p_method = np.nan
                p_label = "p_method"


            if np.isnan(p_method) == True:
                rows.append({
                      modx: val,
                      'B': slope,
                      'se': se,
                      't': t_val,
                      'p': p_val,
                      'ci_lower': ci_lower,
                      'ci_upper': ci_upper
                  })
            else:
                rows.append({
                    modx: val,
                    'B': slope,
                    'se': se,
                    't': t_val,
                    p_label: p_method,
                    'ci_lower': ci_lower,
                    'ci_upper': ci_upper
                })
        result_df = pd.DataFrame(rows)
        result_df.index = modx_legend_labels
        return result_df.round(round_dec)

    # Process data with or without a second moderator.
    if mod2 is not None:
        if mod2_values is None:
            mod2_levels = sorted(data[mod2].unique())
        else:
            mod2_levels = mod2_values
        all_dfs = []
        for level in mod2_levels:
            subset = data[data[mod2] == level]
            df_level = process_data(subset)
            df_level.insert(0, "at_mod2_val", level)
            all_dfs.append(df_level)
        result_df = pd.concat(all_dfs, axis=0)
        return round(result_df,round_dec)
    else:
        return round(process_data(data),round_dec)



