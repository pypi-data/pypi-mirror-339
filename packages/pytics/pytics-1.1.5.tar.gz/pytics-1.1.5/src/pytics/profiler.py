"""
Core profiling functionality
"""
from typing import Optional, List, Literal, Dict, Any, Union
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path
from jinja2 import Environment, PackageLoader
from xhtml2pdf import pisa
import os
import builtins
from .visualizations import _convert_to_static_image
from io import StringIO

# Initialize Jinja2 environment with PackageLoader
env = Environment(loader=PackageLoader('pytics', 'templates'))
env.globals['len'] = builtins.len

class ProfilerError(Exception):
    """Base exception for data profiler errors"""
    pass

class DataSizeError(ProfilerError):
    """Exception raised when data size exceeds limits"""
    pass

def _calculate_overview_stats(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate overview statistics for the DataFrame"""
    total_cells = df.size
    missing_cells = df.isna().sum().sum()
    duplicate_rows = df.duplicated().sum()
    
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB",
        'duplicate_rows': duplicate_rows,
        'duplicate_rows_pct': f"{(duplicate_rows / len(df)) * 100:.2f}",
        'missing_cells': missing_cells,
        'missing_cells_pct': f"{(missing_cells / total_cells) * 100:.2f}",
        'avg_record_size': f"{df.memory_usage(deep=True).sum() / len(df) / 1024:.2f} KB"
    }

def _analyze_variable(df: pd.DataFrame, column: str, target: Optional[str] = None, return_static: bool = False, output_format: str = 'html') -> Dict[str, Any]:
    """
    Analyze a single variable/column
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze
    column : str
        The column name to analyze
    target : str, optional
        Name of the target variable for supervised learning tasks
    return_static : bool, default False
        If True, return static images instead of interactive plots
    output_format : str, default 'html'
        The output format ('html' or 'pdf')
        
    Returns
    -------
    Dict[str, Any]
        Dictionary containing analysis results
    """
    series = df[column]
    total_count = len(series)
    missing_count = series.isna().sum()
    distinct_count = series.nunique()
    
    var_stats = {
        'name': column,
        'type': str(series.dtype),
        'distinct_count': distinct_count,
        'distinct_pct': f"{(distinct_count / total_count) * 100:.2f}",
        'missing_count': missing_count,
        'missing_pct': f"{(missing_count / total_count) * 100:.2f}"
    }
    
    # Add numeric statistics if applicable
    if series.dtype in ['int64', 'float64']:
        desc = series.describe()
        var_stats.update({
            'mean': f"{desc['mean']:.2f}",
            'std': f"{desc['std']:.2f}",
            'min': f"{desc['min']:.2f}",
            'q1': f"{desc['25%']:.2f}",
            'median': f"{desc['50%']:.2f}",
            'q3': f"{desc['75%']:.2f}",
            'max': f"{desc['max']:.2f}"
        })
        
        # Distribution plot
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=series.dropna(), name=column))
        fig.add_trace(go.Box(x=series.dropna(), name=column, yaxis='y2'))
        fig.update_layout(
            title=f"{column} Distribution",
            yaxis2=dict(overlaying='y', side='right')
        )
        
        if return_static:
            var_stats['distribution_plot'] = _convert_to_static_image(fig, format=output_format)
        else:
            var_stats['distribution_plot'] = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # Target relationship plot if target exists
        if target and target in df.columns:
            if df[target].dtype in ['int64', 'float64']:
                fig = px.scatter(df, x=column, y=target, title=f"{column} vs {target}")
            else:
                fig = px.box(df, x=column, y=target, title=f"{column} by {target}")
            
            if return_static:
                var_stats['target_plot'] = _convert_to_static_image(fig, format=output_format)
            else:
                var_stats['target_plot'] = fig.to_html(full_html=False, include_plotlyjs='cdn')
    else:
        # For categorical variables
        value_counts = series.value_counts()
        var_stats['mode'] = value_counts.index[0] if not value_counts.empty else None
        
        # Distribution plot
        fig = px.bar(
            x=value_counts.index[:20],  # Show top 20 categories
            y=value_counts.values[:20],
            title=f"{column} Distribution (Top 20 Categories)"
        )
        
        if return_static:
            var_stats['distribution_plot'] = _convert_to_static_image(fig, format=output_format)
        else:
            var_stats['distribution_plot'] = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # Target relationship plot if target exists
        if target and target in df.columns and df[target].dtype in ['int64', 'float64']:
            fig = px.box(df, x=column, y=target, title=f"{target} by {column}")
            
            if return_static:
                var_stats['target_plot'] = _convert_to_static_image(fig, format=output_format)
            else:
                var_stats['target_plot'] = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    return var_stats

def _create_summary_plots(df: pd.DataFrame, target: Optional[str] = None, theme: str = 'light', return_static: bool = False, output_format: str = 'html') -> Dict[str, Any]:
    """
    Create summary plots for the DataFrame
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze
    target : str, optional
        Name of the target variable
    theme : str, default 'light'
        Color theme for plots
    return_static : bool, default False
        If True, return static images instead of interactive plots
    output_format : str, default 'html'
        The output format ('html' or 'pdf')
        
    Returns
    -------
    Dict[str, Any]
        Dictionary containing plot HTML strings or static images
    """
    plotly_template = 'plotly_white' if theme == 'light' else 'plotly_dark'
    
    # Types and missing values plot
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=df.dtypes.value_counts().index.astype(str),
        y=df.dtypes.value_counts().values,
        name='Types'
    ))
    fig1.add_trace(go.Bar(
        x=df.dtypes.value_counts().index.astype(str),
        y=df.isna().sum().values,
        name='Missing'
    ))
    fig1.update_layout(
        title='Variable Types and Missing Values',
        template=plotly_template
    )
    
    # Correlations plot for numeric columns
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        fig2 = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu'
        ))
        fig2.update_layout(
            title='Correlation Matrix',
            template=plotly_template
        )
        correlations_plot = _convert_to_static_image(fig2, format=output_format) if return_static else fig2.to_html(full_html=False, include_plotlyjs='cdn')
    else:
        correlations_plot = None
    
    return {
        'types_missing': _convert_to_static_image(fig1, format=output_format) if return_static else fig1.to_html(full_html=False, include_plotlyjs='cdn'),
        'correlations': correlations_plot
    }

def _analyze_duplicates(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Analyze duplicate rows in the DataFrame"""
    if df.duplicated().sum() == 0:
        return []
    
    dup_counts = df.groupby(list(df.columns)).size()
    dup_counts = dup_counts[dup_counts > 1].sort_values(ascending=False)
    
    return [
        {'count': count, 'rows': ', '.join(map(str, df[df.duplicated(keep=False)].index[:5]))}
        for count in dup_counts[:10]  # Show top 10 duplicate patterns
    ]

def profile(
    df: pd.DataFrame,
    target: Optional[str] = None,
    output_file: Optional[str] = None,
    output_format: str = 'html',
    title: str = "Data Profile Report",
    theme: str = "light",
    return_context: bool = False
) -> Union[str, Dict[str, Any], None]:
    """
    Generate a profile report for a pandas DataFrame.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to analyze
    target : str, optional
        Name of the target variable for supervised learning tasks
    output_file : str, optional
        Path to save the report. If not provided, returns the report content
    output_format : str, default 'html'
        Output format ('html' or 'pdf')
    title : str, default "Data Profile Report"
        Title for the report
    theme : str, default "light"
        Color theme for plots ('light' or 'dark')
    return_context : bool, default False
        If True, returns the context dictionary instead of the rendered report
        
    Returns
    -------
    Union[str, Dict[str, Any], None]
        If output_file is None: returns the report content as string
        If return_context is True: returns the context dictionary
        If output_file is provided: returns the output file path
    """
    # Check data size limits
    if len(df) > 1_000_000:
        raise DataSizeError("DataFrame exceeds 1 million rows limit")
    if len(df.columns) > 1000:
        raise DataSizeError("DataFrame exceeds 1000 columns limit")
    
    # Determine if we need static images for PDF output
    is_pdf_output = output_format == 'pdf' or output_file and output_file.lower().endswith('.pdf')
    
    # Calculate all statistics and generate plots
    overview = _calculate_overview_stats(df)
    variables_list = [_analyze_variable(df, col, target, return_static=is_pdf_output, output_format=output_format) for col in df.columns if col != target]
    # Convert variables list to dictionary with column names as keys
    variables = {var['name']: var for var in variables_list}
    
    # Generate plots with appropriate format
    plots = _create_summary_plots(df, target, theme, return_static=is_pdf_output, output_format=output_format)
    duplicates = _analyze_duplicates(df)
    
    # Generate DataFrame summary data
    info_buffer = StringIO()
    df.info(buf=info_buffer, max_cols=None, memory_usage=True, show_counts=True)
    info_str = info_buffer.getvalue()
    
    # Generate split describe outputs
    describe_num = df.describe(include=[np.number])
    describe_num_str = describe_num.to_string() if not describe_num.empty else None
    
    describe_obj = df.describe(include=['object', 'category', 'bool'])
    describe_obj_str = describe_obj.to_string() if not describe_obj.empty else None
    
    head_html = df.head(5).to_html(
        classes='table table-striped',
        float_format=lambda x: f'{x:.2f}' if isinstance(x, float) else x
    )
    
    tail_html = df.tail(5).to_html(
        classes='table table-striped',
        float_format=lambda x: f'{x:.2f}' if isinstance(x, float) else x
    )
    
    # Add DataFrame summary data to context
    dataframe_summary_data = {
        'info_str': info_str,
        'describe_num_str': describe_num_str,
        'describe_obj_str': describe_obj_str,
        'head_html': head_html,
        'tail_html': tail_html,
        'n': 5  # Number of rows shown in head/tail
    }
    
    # Target variable analysis if specified
    target_analysis = None
    if target and target in df.columns:
        target_analysis = _analyze_variable(df, target, return_static=is_pdf_output, output_format=output_format)
        if target_analysis.get('distribution_plot'):
            # The distribution_plot is already in the correct format (HTML string or base64)
            target_analysis['plot'] = target_analysis['distribution_plot']
    
    # Process variables for template
    for var in variables.values():
        if var.get('distribution_plot'):
            # The distribution_plot is already in the correct format (HTML string or base64)
            var['plot'] = var['distribution_plot']
    
    # Prepare template context
    context = {
        'title': title,
        'theme': theme,
        'is_pdf_output': is_pdf_output,
        # Flatten overview stats into the root context
        'n_vars': len(df.columns),
        'n_obs': len(df),
        'n_missing': df.isna().sum().sum(),
        'missing_percent': (df.isna().sum().sum() / (len(df) * len(df.columns)) * 100).round(2),
        'n_duplicates': df.duplicated().sum(),
        'duplicates_percent': (df.duplicated().sum() / len(df) * 100).round(2),
        'n_numeric': len(df.select_dtypes(include=['int64', 'float64']).columns),
        'n_categorical': len(df.select_dtypes(include=['object', 'category']).columns),
        'n_boolean': len(df.select_dtypes(include=['bool']).columns),
        'n_date': len(df.select_dtypes(include=['datetime64']).columns),
        'n_text': len(df.select_dtypes(include=['string']).columns),
        # Add overview stats
        'overview': overview,
        # Process variables to match template expectations
        'variables': {
            name: {
                'type': var['type'],
                'missing': var['missing_count'],
                'missing_percent': var['missing_pct'],
                'unique': var['distinct_count'],
                'unique_percent': var['distinct_pct'],
                'mean': var.get('mean', ''),
                'std': var.get('std', ''),
                'min': var.get('min', ''),
                'q1': var.get('q1', ''),
                'median': var.get('median', ''),
                'q3': var.get('q3', ''),
                'max': var.get('max', ''),
                'plot': var.get('distribution_plot', '')  # Already in correct format
            }
            for name, var in variables.items()
        },
        # Add plots directly to root context - already in correct format
        'correlation_plot': plots.get('correlations', ''),
        'missing_plot': plots.get('types_missing', ''),
        'duplicates_plot': plots.get('duplicates', ''),
        # Add other context data
        'plots': plots,
        'duplicates': duplicates,
        'target': target_analysis,
        'dataframe_summary_data': dataframe_summary_data
    }
    
    # Load and render template
    template = env.get_template('report_template.html.j2')
    
    # Return context if requested (for testing)
    if return_context:
        return context
        
    html_report = template.render(**context)
    
    # If no output file is specified, return the HTML for display in notebooks
    if not output_file:
        return html_report
    
    # Save the report
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if output_format == 'html' or output_path.suffix.lower() == '.html':
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_report)
    else:  # pdf
        pdf_path = output_path.with_suffix('.pdf')
        result_file = open(pdf_path, "w+b")
        pisa_status = pisa.CreatePDF(html_report, dest=result_file)
        result_file.close()
        
        if pisa_status.err:
            raise ProfilerError("Error generating PDF report")
    
    return output_file

def compare(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    name1: str = "DataFrame 1",
    name2: str = "DataFrame 2",
    output_file: Optional[str] = None,
    n_bins: int = 30,
    theme: str = "light"
) -> Dict[str, Any]:
    """
    Compare two pandas DataFrames and analyze their differences.

    Parameters
    ----------
    df1 : pandas.DataFrame
        First DataFrame to compare
    df2 : pandas.DataFrame
        Second DataFrame to compare
    name1 : str, default "DataFrame 1"
        Name to identify the first DataFrame in the comparison
    name2 : str, default "DataFrame 2"
        Name to identify the second DataFrame in the comparison
    output_file : str, optional
        Path to save the comparison report
    n_bins : int, default 30
        Number of bins to use for numeric column histograms
    theme : str, default "light"
        Theme for the report ('light' or 'dark')

    Returns
    -------
    Dict[str, Any]
        Dictionary containing comparison results and report path if generated
    """
    # Get column sets
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)

    # Find unique and common columns
    columns_only_in_df1 = sorted(list(cols1 - cols2))
    columns_only_in_df2 = sorted(list(cols2 - cols1))
    common_columns = sorted(list(cols1 & cols2))

    # Analyze dtype differences for common columns
    dtype_differences = {}
    for col in common_columns:
        dtype1 = str(df1[col].dtype)
        dtype2 = str(df2[col].dtype)
        if dtype1 != dtype2:
            dtype_differences[col] = (dtype1, dtype2)

    # Statistical comparison and distribution data for common columns
    variable_comparison = {}
    plots = {}
    for col in common_columns:
        series1 = df1[col]
        series2 = df2[col]
        
        # Common statistics for all types
        total_count1 = len(series1)
        total_count2 = len(series2)
        missing_count1 = series1.isna().sum()
        missing_count2 = series2.isna().sum()
        unique_count1 = series1.nunique()
        unique_count2 = series2.nunique()
        
        stats = {
            'count': {'df1': total_count1, 'df2': total_count2},
            'missing_count': {'df1': missing_count1, 'df2': missing_count2},
            'missing_percent': {
                'df1': f"{(missing_count1 / total_count1) * 100:.2f}",
                'df2': f"{(missing_count2 / total_count2) * 100:.2f}"
            },
            'unique_count': {'df1': unique_count1, 'df2': unique_count2},
            'unique_percent': {
                'df1': f"{(unique_count1 / total_count1) * 100:.2f}",
                'df2': f"{(unique_count2 / total_count2) * 100:.2f}"
            }
        }
        
        # Type-specific statistics and distribution data
        if str(series1.dtype) in ['int64', 'float64'] and str(series2.dtype) in ['int64', 'float64']:
            # Numeric statistics
            desc1 = series1.describe()
            desc2 = series2.describe()
            
            stats.update({
                'mean': {'df1': f"{desc1['mean']:.2f}", 'df2': f"{desc2['mean']:.2f}"},
                'std': {'df1': f"{desc1['std']:.2f}", 'df2': f"{desc2['std']:.2f}"},
                'min': {'df1': f"{desc1['min']:.2f}", 'df2': f"{desc2['min']:.2f}"},
                'q1': {'df1': f"{desc1['25%']:.2f}", 'df2': f"{desc2['25%']:.2f}"},
                'median': {'df1': f"{desc1['50%']:.2f}", 'df2': f"{desc2['50%']:.2f}"},
                'q3': {'df1': f"{desc1['75%']:.2f}", 'df2': f"{desc2['75%']:.2f}"},
                'max': {'df1': f"{desc1['max']:.2f}", 'df2': f"{desc2['max']:.2f}"}
            })
            
            # Calculate histogram data
            # Use the same bins for both series to make them comparable
            min_val = min(series1.min(), series2.min())
            max_val = max(series1.max(), series2.max())
            bins = np.linspace(min_val, max_val, n_bins + 1)
            
            hist1, _ = np.histogram(series1.dropna(), bins=bins)
            hist2, _ = np.histogram(series2.dropna(), bins=bins)
            
            # Calculate KDE points
            kde1 = series1.dropna().plot.kde(ind=100)
            x1, y1 = kde1.get_lines()[0].get_data()
            kde1.clear()
            
            kde2 = series2.dropna().plot.kde(ind=100)
            x2, y2 = kde2.get_lines()[0].get_data()
            kde2.clear()
            
            distribution_data = {
                'type': 'numeric',
                'histogram': {
                    'bins': bins.tolist(),
                    'df1_counts': hist1.tolist(),
                    'df2_counts': hist2.tolist()
                },
                'kde': {
                    'df1': {'x': x1.tolist(), 'y': y1.tolist()},
                    'df2': {'x': x2.tolist(), 'y': y2.tolist()}
                }
            }
        else:
            # Categorical statistics
            value_counts1 = series1.value_counts()
            value_counts2 = series2.value_counts()
            
            stats.update({
                'top_values_df1': [
                    {'value': str(value), 'count': count, 'percentage': f"{(count / total_count1) * 100:.2f}"}
                    for value, count in value_counts1.head(5).items()
                ],
                'top_values_df2': [
                    {'value': str(value), 'count': count, 'percentage': f"{(count / total_count2) * 100:.2f}"}
                    for value, count in value_counts2.head(5).items()
                ]
            })
            
            # Store full value counts for distribution visualization
            distribution_data = {
                'type': 'categorical',
                'value_counts': {
                    'df1': {str(k): int(v) for k, v in value_counts1.items()},
                    'df2': {str(k): int(v) for k, v in value_counts2.items()}
                }
            }
        
        variable_comparison[col] = {
            'stats': stats,
            'distribution_data': distribution_data
        }
        
        # Generate plot for this column
        from .visualizations import create_distribution_comparison_plot
        plots[col] = create_distribution_comparison_plot(
            distribution_data,
            name1=name1,
            name2=name2,
            theme=theme
        )

    results = {
        'columns_only_in_df1': columns_only_in_df1,
        'columns_only_in_df2': columns_only_in_df2,
        'common_columns': common_columns,
        'dtype_differences': dtype_differences,
        'variable_comparison': variable_comparison,
        'df1': df1,  # Add DataFrame references to context
        'df2': df2
    }

    if output_file:
        # Load and render the template
        template = env.get_template('compare_report_template.html.j2')
        
        html_content = template.render(
            name1=name1,
            name2=name2,
            theme=theme,
            plots=plots,
            **results
        )
        
        # Save the report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        results['report_path'] = output_file

    return results 