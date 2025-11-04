"""
Comprehensive Single-Cell RNA-seq Analysis Pipeline
Performs QC, normalization, clustering, UMAP, differential expression, and marker gene analysis.
"""

import scanpy as sc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from loguru import logger
import warnings
warnings.filterwarnings('ignore')

# Set plotting parameters
sc.settings.verbosity = 3
sc.settings.set_figure_params(dpi=100, facecolor='white', figsize=(8, 6))
sc.settings.autoshow = False

# Create output directories
output_dir = Path("results/single_cell_analysis")
output_dir.mkdir(parents=True, exist_ok=True)
figures_dir = output_dir / "figures"
figures_dir.mkdir(exist_ok=True)

def load_data(data_path):
    """Load single-cell data."""
    logger.info(f"Loading data from {data_path}")
    adata = sc.read_h5ad(data_path)
    logger.info(f"Loaded {adata.n_obs} cells × {adata.n_vars} genes")
    return adata

def quality_control(adata):
    """Perform quality control analysis."""
    logger.info("=== Quality Control Analysis ===")
    
    # Calculate QC metrics
    adata.var['mt'] = adata.var_names.str.startswith('MT-')
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
    
    # Plot QC metrics
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Total counts
    sns.histplot(adata.obs['total_counts'], bins=100, kde=True, ax=axes[0, 0])
    axes[0, 0].set_xlabel('Total counts per cell')
    axes[0, 0].set_ylabel('Frequency')
    axes[0, 0].set_title('Distribution of Total Counts')
    
    # Genes per cell
    sns.histplot(adata.obs['n_genes_by_counts'], bins=100, kde=True, ax=axes[0, 1])
    axes[0, 1].set_xlabel('Genes per cell')
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Distribution of Detected Genes')
    
    # Mitochondrial percentage
    sns.histplot(adata.obs['pct_counts_mt'], bins=100, kde=True, ax=axes[0, 2])
    axes[0, 2].set_xlabel('Mitochondrial %')
    axes[0, 2].set_ylabel('Frequency')
    axes[0, 2].set_title('Mitochondrial Gene Percentage')
    
    # Scatter plots
    axes[1, 0].scatter(adata.obs['total_counts'], adata.obs['n_genes_by_counts'], alpha=0.3, s=1)
    axes[1, 0].set_xlabel('Total counts')
    axes[1, 0].set_ylabel('Genes detected')
    axes[1, 0].set_title('Total Counts vs Genes Detected')
    
    axes[1, 1].scatter(adata.obs['total_counts'], adata.obs['pct_counts_mt'], alpha=0.3, s=1)
    axes[1, 1].set_xlabel('Total counts')
    axes[1, 1].set_ylabel('Mitochondrial %')
    axes[1, 1].set_title('Total Counts vs Mitochondrial %')
    
    axes[1, 2].scatter(adata.obs['n_genes_by_counts'], adata.obs['pct_counts_mt'], alpha=0.3, s=1)
    axes[1, 2].set_xlabel('Genes detected')
    axes[1, 2].set_ylabel('Mitochondrial %')
    axes[1, 2].set_title('Genes Detected vs Mitochondrial %')
    
    plt.tight_layout()
    plt.savefig(figures_dir / "01_qc_metrics.png", dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ Saved QC metrics plot")
    
    # Print statistics
    logger.info(f"Total counts - Mean: {adata.obs['total_counts'].mean():.0f}, Median: {adata.obs['total_counts'].median():.0f}")
    logger.info(f"Genes detected - Mean: {adata.obs['n_genes_by_counts'].mean():.0f}, Median: {adata.obs['n_genes_by_counts'].median():.0f}")
    logger.info(f"Mitochondrial % - Mean: {adata.obs['pct_counts_mt'].mean():.2f}%, Median: {adata.obs['pct_counts_mt'].median():.2f}%")
    
    return adata

def filter_cells(adata, min_genes=200, max_genes=5000, max_mt_pct=20):
    """Filter cells based on QC metrics."""
    logger.info("=== Cell Filtering ===")
    logger.info(f"Before filtering: {adata.n_obs} cells")
    
    # Filter cells
    sc.pp.filter_cells(adata, min_genes=min_genes)
    adata = adata[adata.obs.n_genes_by_counts < max_genes, :]
    adata = adata[adata.obs.pct_counts_mt < max_mt_pct, :]
    
    logger.info(f"After filtering: {adata.n_obs} cells")
    logger.info(f"Removed {adata.n_obs} cells that didn't pass QC")
    
    # Filter genes
    sc.pp.filter_genes(adata, min_cells=3)
    logger.info(f"Genes after filtering: {adata.n_vars}")
    
    return adata

def normalize_and_scale(adata):
    """Normalize and scale the data."""
    logger.info("=== Normalization and Scaling ===")
    
    # Store raw counts
    adata.layers['counts'] = adata.X.copy()
    
    # Normalize to 10,000 counts per cell
    sc.pp.normalize_total(adata, target_sum=1e4)
    
    # Log transform
    sc.pp.log1p(adata)
    
    # Store normalized data
    adata.layers['log_normalized'] = adata.X.copy()
    
    # Identify highly variable genes
    sc.pp.highly_variable_genes(adata, n_top_genes=2000, flavor='seurat')
    logger.info(f"Highly variable genes: {adata.var['highly_variable'].sum()}")
    
    # Plot highly variable genes
    fig = sc.pl.highly_variable_genes(adata, show=False)
    plt.savefig(figures_dir / "02_highly_variable_genes.png", dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ Saved highly variable genes plot")
    
    # Scale data
    sc.pp.scale(adata, max_value=10)
    
    return adata

def dimensionality_reduction(adata):
    """Perform PCA and UMAP."""
    logger.info("=== Dimensionality Reduction ===")
    
    # PCA
    sc.tl.pca(adata, svd_solver='arpack', n_comps=50)
    
    # Plot PCA variance ratio
    fig = sc.pl.pca_variance_ratio(adata, log=True, n_pcs=50, show=False)
    plt.savefig(figures_dir / "03_pca_variance_ratio.png", dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ Saved PCA variance ratio plot")
    
    # Compute neighborhood graph
    sc.pp.neighbors(adata, n_neighbors=15, n_pcs=40)
    
    # UMAP
    sc.tl.umap(adata)
    logger.info("✓ Computed UMAP")
    
    return adata

def clustering_analysis(adata):
    """Perform clustering analysis."""
    logger.info("=== Clustering Analysis ===")
    
    # Leiden clustering at different resolutions
    resolutions = [0.4, 0.8, 1.2]
    for res in resolutions:
        sc.tl.leiden(adata, resolution=res, key_added=f'leiden_res_{res}')
        logger.info(f"Leiden clustering at resolution {res}: {adata.obs[f'leiden_res_{res}'].nunique()} clusters")
    
    # Plot UMAP with different resolutions
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    for i, res in enumerate(resolutions):
        sc.pl.umap(adata, color=f'leiden_res_{res}', ax=axes[i], show=False, 
                   title=f'Leiden (res={res}): {adata.obs[f"leiden_res_{res}"].nunique()} clusters')
    plt.tight_layout()
    plt.savefig(figures_dir / "04_clustering_resolutions.png", dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ Saved clustering comparison plot")
    
    # Use resolution 0.8 as default
    adata.obs['clusters'] = adata.obs['leiden_res_0.8']
    
    return adata

def find_marker_genes(adata):
    """Find marker genes for each cluster."""
    logger.info("=== Marker Gene Analysis ===")
    
    # Find marker genes using Wilcoxon rank-sum test
    sc.tl.rank_genes_groups(adata, 'clusters', method='wilcoxon')
    
    # Plot top marker genes
    fig = sc.pl.rank_genes_groups(adata, n_genes=20, sharey=False, show=False)
    plt.savefig(figures_dir / "05_marker_genes_ranking.png", dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ Saved marker genes ranking plot")
    
    # Get marker genes dataframe
    result = adata.uns['rank_genes_groups']
    groups = result['names'].dtype.names
    marker_df = pd.DataFrame({
        group + f'_{key}': result[key][group]
        for group in groups for key in ['names', 'scores', 'pvals_adj', 'logfoldchanges']
    })
    
    # Save marker genes
    marker_df.to_csv(output_dir / "marker_genes.csv", index=False)
    logger.info(f"✓ Saved marker genes to CSV")
    
    # Plot dotplot of top markers
    fig = sc.pl.rank_genes_groups_dotplot(adata, n_genes=5, show=False)
    plt.savefig(figures_dir / "06_marker_genes_dotplot.png", dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ Saved marker genes dotplot")
    
    # Plot heatmap of top markers
    fig = sc.pl.rank_genes_groups_heatmap(adata, n_genes=10, show=False, cmap='viridis')
    plt.savefig(figures_dir / "07_marker_genes_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"✓ Saved marker genes heatmap")
    
    return adata, marker_df

def cell_type_annotation(adata):
    """Annotate cell types based on known markers."""
    logger.info("=== Cell Type Annotation ===")
    
    # Known PBMC markers
    marker_genes = {
        'CD3D': 'T cells',
        'CD3E': 'T cells',
        'CD8A': 'CD8+ T cells',
        'CD4': 'CD4+ T cells',
        'CD19': 'B cells',
        'MS4A1': 'B cells',  # CD20
        'CD14': 'Monocytes',
        'LYZ': 'Monocytes',
        'FCGR3A': 'Monocytes',  # CD16
        'NKG7': 'NK cells',
        'GNLY': 'NK cells'
    }
    
    # Plot known markers on UMAP
    available_markers = [gene for gene in marker_genes.keys() if gene in adata.var_names]
    
    if available_markers:
        n_markers = len(available_markers)
        n_cols = 4
        n_rows = (n_markers + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
        
        for i, gene in enumerate(available_markers):
            sc.pl.umap(adata, color=gene, ax=axes[i], show=False, 
                      title=f'{gene} ({marker_genes[gene]})', cmap='viridis')
        
        # Hide empty subplots
        for i in range(len(available_markers), len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.savefig(figures_dir / "08_marker_gene_expression.png", dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"✓ Saved marker gene expression plot")
    
    return adata

def visualize_results(adata):
    """Create comprehensive visualization of results."""
    logger.info("=== Generating Final Visualizations ===")
    
    # UMAP with clusters
    fig = sc.pl.umap(adata, color='clusters', legend_loc='right margin', 
                     title='Cell Clusters', show=False, palette='tab20')
    plt.savefig(figures_dir / "09_umap_clusters.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # UMAP colored by QC metrics
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sc.pl.umap(adata, color='n_genes_by_counts', ax=axes[0], show=False, title='Genes Detected')
    sc.pl.umap(adata, color='total_counts', ax=axes[1], show=False, title='Total Counts')
    sc.pl.umap(adata, color='pct_counts_mt', ax=axes[2], show=False, title='Mitochondrial %')
    plt.tight_layout()
    plt.savefig(figures_dir / "10_umap_qc_metrics.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Cluster composition
    cluster_counts = adata.obs['clusters'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(10, 6))
    cluster_counts.plot(kind='bar', ax=ax, color='steelblue')
    ax.set_xlabel('Cluster')
    ax.set_ylabel('Number of Cells')
    ax.set_title('Cell Count per Cluster')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(figures_dir / "11_cluster_composition.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"✓ Saved all visualization plots")
    
def generate_report(adata, marker_df):
    """Generate analysis report with interactive HTML."""
    logger.info("=== Generating Analysis Report ===")
    
    report = {
        'dataset_info': {
            'total_cells': int(adata.n_obs),
            'total_genes': int(adata.n_vars),
            'highly_variable_genes': int(adata.var['highly_variable'].sum()),
            'clusters': int(adata.obs['clusters'].nunique())
        },
        'qc_metrics': {
            'mean_genes_per_cell': float(adata.obs['n_genes_by_counts'].mean()),
            'median_genes_per_cell': float(adata.obs['n_genes_by_counts'].median()),
            'mean_counts_per_cell': float(adata.obs['total_counts'].mean()),
            'median_counts_per_cell': float(adata.obs['total_counts'].median()),
            'mean_mt_percentage': float(adata.obs['pct_counts_mt'].mean()),
            'median_mt_percentage': float(adata.obs['pct_counts_mt'].median())
        },
        'cluster_composition': adata.obs['clusters'].value_counts().to_dict()
    }
    
    # Save JSON report
    import json
    with open(output_dir / "analysis_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"✓ Saved analysis report")
    
    # Generate interactive HTML report
    generate_html_report(report)
    
    # Save processed data
    adata.write_h5ad(output_dir / "processed_data.h5ad")
    logger.info(f"✓ Saved processed data")
    
    # Print summary
    print("\n" + "="*60)
    print("SINGLE-CELL ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total cells analyzed: {report['dataset_info']['total_cells']}")
    print(f"Total genes: {report['dataset_info']['total_genes']}")
    print(f"Highly variable genes: {report['dataset_info']['highly_variable_genes']}")
    print(f"Clusters identified: {report['dataset_info']['clusters']}")
    print(f"\nMean genes per cell: {report['qc_metrics']['mean_genes_per_cell']:.0f}")
    print(f"Mean counts per cell: {report['qc_metrics']['mean_counts_per_cell']:.0f}")
    print(f"Mean mitochondrial %: {report['qc_metrics']['mean_mt_percentage']:.2f}%")
    print("\nCluster composition:")
    for cluster, count in sorted(report['cluster_composition'].items()):
        print(f"  Cluster {cluster}: {count} cells")
    print(f"\nResults saved to: {output_dir}")
    print(f"Open: {output_dir}/interactive_report.html")
    print("="*60)

def generate_html_report(report):
    """Generate interactive HTML report with all plots."""
    import base64
    from pathlib import Path
    
    logger.info("Generating interactive HTML report...")
    
    # Get all figure files
    figures = sorted(figures_dir.glob("*.png"))
    
    # Convert images to base64
    def img_to_base64(img_path):
        with open(img_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    
    # HTML template
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Single-Cell RNA-seq Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }}
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }}
        .metric-label {{
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .content {{
            padding: 40px;
        }}
        .section {{
            margin-bottom: 50px;
        }}
        .section-title {{
            font-size: 1.8em;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        .plot-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .plot-title {{
            font-size: 1.2em;
            color: #333;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        .plot-container img {{
            width: 100%;
            height: auto;
            border-radius: 5px;
        }}
        .cluster-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        .cluster-table th {{
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }}
        .cluster-table td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        .cluster-table tr:hover {{
            background: #f5f5f5;
        }}
        .footer {{
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }}
        .badge {{
            display: inline-block;
            padding: 5px 15px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-size: 0.85em;
            margin: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧬 Single-Cell RNA-seq Analysis Report</h1>
            <p>PBMC 3k Dataset - Comprehensive Analysis Pipeline</p>
        </div>
        
        <div class="summary">
            <div class="metric-card">
                <div class="metric-label">Total Cells</div>
                <div class="metric-value">{report['dataset_info']['total_cells']:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Genes</div>
                <div class="metric-value">{report['dataset_info']['total_genes']:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">HV Genes</div>
                <div class="metric-value">{report['dataset_info']['highly_variable_genes']:,}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Clusters</div>
                <div class="metric-value">{report['dataset_info']['clusters']}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Mean Genes/Cell</div>
                <div class="metric-value">{report['qc_metrics']['mean_genes_per_cell']:.0f}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Mean Counts/Cell</div>
                <div class="metric-value">{report['qc_metrics']['mean_counts_per_cell']:.0f}</div>
            </div>
        </div>
        
        <div class="content">
"""
    
    # Add plots
    plot_sections = {
        "01_qc_metrics.png": ("Quality Control", "Distribution of QC metrics: total counts, genes detected, and mitochondrial percentage"),
        "02_highly_variable_genes.png": ("Highly Variable Genes", "Identification of 2,000 highly variable genes for downstream analysis"),
        "03_pca_variance_ratio.png": ("PCA Variance", "Variance explained by principal components"),
        "04_clustering_resolutions.png": ("Multi-Resolution Clustering", "Leiden clustering at resolutions 0.4, 0.8, and 1.2"),
        "05_marker_genes_ranking.png": ("Marker Gene Ranking", "Top marker genes for each cluster (Wilcoxon test)"),
        "06_marker_genes_dotplot.png": ("Marker Expression Dotplot", "Expression of top markers across clusters"),
        "07_marker_genes_heatmap.png": ("Marker Expression Heatmap", "Heatmap of top marker genes per cluster"),
        "08_marker_gene_expression.png": ("Known PBMC Markers", "Expression of known cell type markers on UMAP"),
        "09_umap_clusters.png": ("UMAP Clustering", "UMAP visualization colored by cluster assignment"),
        "10_umap_qc_metrics.png": ("UMAP QC Metrics", "UMAP colored by quality control metrics"),
        "11_cluster_composition.png": ("Cluster Composition", "Number of cells per cluster"),
    }
    
    for fig_file, (title, description) in plot_sections.items():
        fig_path = figures_dir / fig_file
        if fig_path.exists():
            img_base64 = img_to_base64(fig_path)
            html += f"""
            <div class="section">
                <h2 class="section-title">{title}</h2>
                <div class="plot-container">
                    <p style="color: #666; margin-bottom: 15px;">{description}</p>
                    <img src="data:image/png;base64,{img_base64}" alt="{title}">
                </div>
            </div>
"""
    
    # Add cluster composition table
    html += f"""
            <div class="section">
                <h2 class="section-title">Cluster Composition</h2>
                <table class="cluster-table">
                    <thead>
                        <tr>
                            <th>Cluster</th>
                            <th>Cell Count</th>
                            <th>Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
"""
    
    total_cells = report['dataset_info']['total_cells']
    for cluster, count in sorted(report['cluster_composition'].items()):
        percentage = (count / total_cells) * 100
        html += f"""
                        <tr>
                            <td><strong>Cluster {cluster}</strong></td>
                            <td>{count:,}</td>
                            <td>{percentage:.1f}%</td>
                        </tr>
"""
    
    html += """
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by Single-Cell RNA-seq Analysis Pipeline</p>
            <p style="margin-top: 5px; opacity: 0.7;">Powered by Scanpy, Python, and Docker</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML report
    with open(output_dir / "interactive_report.html", 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✓ Saved interactive HTML report")


def main():
    """Run complete single-cell analysis pipeline."""
    logger.info("Starting Single-Cell RNA-seq Analysis Pipeline")
    
    # Load data
    data_path = "data/raw/cancer_expression.h5ad"
    adata = load_data(data_path)
    
    # QC and filtering
    adata = quality_control(adata)
    adata = filter_cells(adata, min_genes=200, max_genes=5000, max_mt_pct=20)
    
    # Normalization and scaling
    adata = normalize_and_scale(adata)
    
    # Dimensionality reduction
    adata = dimensionality_reduction(adata)
    
    # Clustering
    adata = clustering_analysis(adata)
    
    # Marker gene analysis
    adata, marker_df = find_marker_genes(adata)
    
    # Cell type annotation
    adata = cell_type_annotation(adata)
    
    # Visualizations
    visualize_results(adata)
    
    # Generate report
    generate_report(adata, marker_df)
    
    logger.info("✓ Single-cell analysis pipeline completed successfully!")
    
if __name__ == "__main__":
    main()
