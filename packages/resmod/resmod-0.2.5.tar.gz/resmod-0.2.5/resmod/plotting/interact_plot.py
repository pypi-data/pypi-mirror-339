#!/usr/bin/python3


def interact_plot(outcome, pred, modx, data, controls=None,
                  mod2=None, 
                  modx_values=None, modx_legend_labels=None,
                  mod2_values=None,
                  plot_points=False, points_per_facet=100,
                  interval=False, int_width=0.95,
                  x_label=None, y_label=None, colors=None, 
                  line_thickness=2, jitter=0, point_size=50, n_sim=100,
                  n_grid=None,
                  x_jitter=0.2, y_jitter=0.2,
                  **kwargs):
  """
  Estimate a regression model (or models, if faceting by a second moderator) and 
  simulate predictions to plot interaction effects.

  For a single model (no mod2), the model is estimated using the formula:
      outcome ~ pred * modx [+ controls]
  For a second moderator (mod2), separate models are estimated for each facet 
  (i.e. for each unique or specified value of mod2).

  The focal predictor (pred) is standardized (z‐scored) if continuous. For a continuous 
  moderator (modx) with >2 unique values, if modx_values is not supplied then default values 
  are set at (mean – SD, mean, mean + SD) with legend labels "-1SD", "Mean", "+1SD".
  For categorical moderators, the unique sorted levels are used.

  At each grid point (n_grid points along pred), n_sim simulated coefficient draws are used 
  to compute predicted values. The mean (and if requested, a simulated interval) is plotted 
  for each moderator level.
  
  **Simulated Data Points:**  
  In addition, if plot_points=True, then for each modx level the function selects one simulated 
  prediction per grid point (using the simulated beta draws) so that the total number of points 
  per line is equal to n_grid. These simulated points are overplotted using the same color as the 
  corresponding line and with an alpha of 0.5. The x– and y–positions of these points can be jittered 
  using the parameters x_jitter and y_jitter.
  
  When faceting by mod2, n_grid defaults to 50 (i.e. 50 points per line, so if there are three modx levels, 
  each facet gets ~150 points). Otherwise, n_grid defaults to 100.
  
  Parameters
  ----------
  outcome : str
      Name of the outcome variable.
  pred : str
      Name of the focal predictor variable.
  modx : str
      Name of the moderator variable.
  data : pd.DataFrame
      DataFrame containing the data.
  controls : list of str, optional
      List of additional control variable names to include in the model.
  mod2 : str, optional
      Name of a second moderator variable for faceting. If provided, separate models 
      will be estimated for each unique or specified mod2 value.
  modx_values : array-like, optional
      Values of the moderator (modx) at which to simulate predictions. If None and modx
      is continuous, defaults to [mean-SD, mean, mean+SD].
  modx_legend_labels : list of str, optional
      Custom legend labels for the modx levels. For continuous modx, defaults to
      ["-1SD", "Mean", "+1SD"].
  mod2_values : array-like, optional
      Values of mod2 for which to estimate separate models. If None, unique sorted values 
      of mod2 in the data are used.
  plot_points : bool, default False
      If True, simulated points are overplotted.
  points_per_facet : int, default 100
      If faceting by mod2 and plot_points is True, this many observed points will be 
      sampled for display (if used; see below).
  interval : bool, default False
      If True, a ribbon is drawn for a simulated confidence interval.
  int_width : float, default 0.95
      Confidence level for the interval.
  x_label : str, optional
      Label for the x-axis.
  y_label : str, optional
      Label for the y-axis.
  colors : list, optional
      List of colors to use for the different modx levels.
  line_thickness : float, default 2
      Line width.
  jitter : float, default 0
      Amount of horizontal jitter to add to observed data points (if used).
  point_size : float, default 50
      Size of the observed data points.
  n_sim : int, default 100
      Number of simulation draws for the coefficient estimates.
  n_grid : int, optional
      Number of grid points for simulation (and simulated points per line). 
      Defaults to 100 if mod2 is not provided, or 50 if mod2 is provided.
  x_jitter : float, default 0.20
      Jitter added to the x–coordinate of simulated points.
  y_jitter : float, default 0.20
      Jitter added to the y–coordinate of simulated points.
  **kwargs :
      Other keyword arguments.

  Returns
  -------
  ax or axes : matplotlib Axes
      The axis (or axes, if faceted) containing the plot.
  """
  # Require packages import checking
  try:
      import numpy as np
      import pandas as pd
      import matplotlib.pyplot as plt
      import statsmodels.formula.api as smf
      import patsy
  except ImportError as e:
      raise ImportError(f"Missing required package: {e.name}. Install it using `pip install {e.name}`")
  
  # Set default colors if not provided.
  if colors is None:
      colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

  # Determine if the focal predictor is continuous (with >2 unique values).
  if np.issubdtype(data[pred].dtype, np.number) and data[pred].nunique() > 2:
      is_pred_cont = True
      pred_mean = data[pred].mean()
      pred_std = data[pred].std()
  else:
      is_pred_cont = False

  # Set the grid length (number of x-values). If n_grid not supplied, use 100 (non-faceted) or 50 (faceted).
  if n_grid is None:
      n_grid = 100 if mod2 is None else 50

  # Create grid for the focal predictor.
  if is_pred_cont:
      grid_raw = np.linspace(data[pred].min(), data[pred].max(), n_grid)
      grid_plot = (grid_raw - pred_mean) / pred_std
  else:
      grid_raw = np.sort(data[pred].unique())
      grid_plot = grid_raw

  # Determine if moderator modx is continuous.
  if np.issubdtype(data[modx].dtype, np.number) and data[modx].nunique() > 2:
      is_modx_cont = True
  else:
      is_modx_cont = False

  # Set default modx values and legend labels.
  if is_modx_cont:
      if modx_values is None:
          modx_mean = data[modx].mean()
          modx_std = data[modx].std()
          modx_values = [modx_mean - modx_std, modx_mean, modx_mean + modx_std]
          if modx_legend_labels is None:
              modx_legend_labels = ["-1SD", "Mean", "+1SD"]
      else:
          if modx_legend_labels is None:
              modx_legend_labels = [f"{modx} = {val}" for val in modx_values]
  else:
      if modx_values is None:
          modx_values = np.sort(data[modx].unique())
      if modx_legend_labels is None:
          modx_legend_labels = [f"{modx} = {val}" for val in modx_values]

  # For mod2, if provided, get its values.
  if mod2 is not None:
      if mod2_values is None:
          mod2_values = np.sort(data[mod2].unique())

  # Build regression formula.
  formula = f"{outcome} ~ {pred} * {modx}"
  if controls is not None and len(controls) > 0:
      formula += " + " + " + ".join(controls)

  # For controls not explicitly set, use their mean value.
  controls_means = {}
  if controls is not None:
      for var in controls:
          controls_means[var] = data[var].mean()

  # Helper: complete prediction DataFrame with any missing predictors.
  def complete_df(df, model_exog):
      for col in model_exog:
          if col not in df.columns:
              if col.lower() in ['const', 'intercept']:
                  df[col] = 1
              else:
                  if col in data.columns:
                      df[col] = data[col].mean()
                  else:
                      df[col] = 0
      return df

  # Single Model (no mod2)
  if mod2 is None:
      mod = smf.ols(formula, data=data).fit()
      design_info = patsy.dmatrix(mod.model.data.design_info, data.iloc[:1],
                                  return_type='dataframe').design_info

      fig, ax = plt.subplots(figsize=(8,6))
      for i, modx_val in enumerate(modx_values):
          df_pred = pd.DataFrame({pred: grid_raw, modx: modx_val})
          for var, mean_val in controls_means.items():
              df_pred[var] = mean_val
          df_pred = complete_df(df_pred, mod.model.exog_names)
          X = patsy.dmatrix(design_info, df_pred, return_type='dataframe')
          # Simulate coefficient draws.
          coef_sim = np.random.multivariate_normal(mod.params, mod.cov_params(), size=n_sim)
          sim_preds = X.values.dot(coef_sim.T)  # shape: (n_grid, n_sim)
          mean_preds = sim_preds.mean(axis=1)
          if interval:
              lower = np.percentile(sim_preds, (1-int_width)/2*100, axis=1)
              upper = np.percentile(sim_preds, (1+int_width)/2*100, axis=1)
          color = colors[i % len(colors)]
          label = modx_legend_labels[i] if i < len(modx_legend_labels) else f"{modx} = {modx_val}"
          ax.plot(grid_plot, mean_preds, label=label, color=color, linewidth=line_thickness)
          if interval:
              ax.fill_between(grid_plot, lower, upper, color=color, alpha=0.3)
          # For simulated points: for each grid point, randomly pick one draw.
          if plot_points:
              # For each grid point, choose one simulation (along axis=1).
              sim_points = np.array([np.random.choice(sim_preds[j, :]) for j in range(len(grid_plot))])
              # Add jitter.
              sim_points = sim_points + np.random.uniform(-y_jitter, y_jitter, size=len(sim_points))
              x_points = grid_plot + np.random.uniform(-x_jitter, x_jitter, size=len(grid_plot))
              ax.scatter(x_points, sim_points, color=color, s=point_size, alpha=0.5, zorder=3)

      ax.set_xlabel(x_label if x_label is not None else (f"Standardized {pred}" if is_pred_cont else pred))
      ax.set_ylabel(y_label if y_label is not None else outcome)
      ax.legend(title=modx)
      plt.tight_layout()
      return ax

  # Faceted Models by mod2
  else:
      n_facets = len(mod2_values)
      fig, axes = plt.subplots(1, n_facets, figsize=(6*n_facets, 6), sharey=True)
      if n_facets == 1:
          axes = [axes]
      for j, mod2_val in enumerate(mod2_values):
          facet_data = data[data[mod2] == mod2_val]
          mod_facet = smf.ols(formula, data=facet_data).fit()
          design_info = patsy.dmatrix(mod_facet.model.data.design_info, facet_data.iloc[:1],
                                      return_type='dataframe').design_info

          ax = axes[j]
          for i, modx_val in enumerate(modx_values):
              df_pred = pd.DataFrame({pred: grid_raw, modx: modx_val, mod2: mod2_val})
              for var, mean_val in controls_means.items():
                  df_pred[var] = mean_val
              df_pred = complete_df(df_pred, mod_facet.model.exog_names)
              X = patsy.dmatrix(design_info, df_pred, return_type='dataframe')
              coef_sim = np.random.multivariate_normal(mod_facet.params, mod_facet.cov_params(), size=n_sim)
              sim_preds = X.values.dot(coef_sim.T)
              mean_preds = sim_preds.mean(axis=1)
              if interval:
                  lower = np.percentile(sim_preds, (1-int_width)/2*100, axis=1)
                  upper = np.percentile(sim_preds, (1+int_width)/2*100, axis=1)
              color = colors[i % len(colors)]
              label = modx_legend_labels[i] if i < len(modx_legend_labels) else f"{modx} = {modx_val}"
              ax.plot(grid_plot, mean_preds, label=label, color=color, linewidth=line_thickness)
              if interval:
                  ax.fill_between(grid_plot, lower, upper, color=color, alpha=0.3)
              if plot_points:
                  sim_points = np.array([np.random.choice(sim_preds[j, :]) for j in range(len(grid_plot))])
                  sim_points = sim_points + np.random.uniform(-y_jitter, y_jitter, size=len(sim_points))
                  x_points = grid_plot + np.random.uniform(-x_jitter, x_jitter, size=len(grid_plot))
                  ax.scatter(x_points, sim_points, color=color, s=point_size, alpha=0.5, zorder=3)
          
          ax.set_title(f"{mod2} = {mod2_val}")
          ax.set_xlabel(x_label if x_label is not None else (f"Standardized {pred}" if is_pred_cont else pred))
      axes[0].set_ylabel(y_label if y_label is not None else outcome)
      axes[0].legend(title=modx)
      plt.tight_layout()
      return axes


