import os
import matplotlib.pyplot as plt
import numpy as np

def generate_performance_chart(output_path):
    plt.figure(figsize=(8, 5))
    
    # Data
    pool_sizes = [10, 50, 100, 500, 1000]
    processing_time = [0.8, 2.1, 4.3, 18.0, 35.0]
    
    # Plotting
    plt.plot(pool_sizes, processing_time, marker='o', linestyle='-', color='#0366d6', linewidth=2, markersize=6)
    
    # Styling
    plt.title('System Performance: Processing Time vs Pool Size', fontsize=12, pad=15)
    plt.xlabel('Resume Pool Size', fontsize=10)
    plt.ylabel('Processing Time (seconds)', fontsize=10)
    
    # Clean up borders
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    plt.grid(axis='y', linestyle='--', alpha=0.5, color='#dddddd')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()

def generate_results_chart(output_path):
    plt.figure(figsize=(10, 6))
    
    # Data
    factors = ["TF-IDF", "Keyword", "Semantic", "Experience", "Domain", "Education"]
    relevant = [0.41, 0.58, 0.72, 0.82, 0.65, 0.78]
    irrelevant = [0.08, 0.12, 0.51, 0.35, 0.15, 0.62]
    
    x = np.arange(len(factors))
    width = 0.35
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, relevant, width, label='Relevant', color='#28a745', alpha=0.9)
    rects2 = ax.bar(x + width/2, irrelevant, width, label='Irrelevant', color='#dc3545', alpha=0.8)
    
    # Styling
    ax.set_ylabel('Mean Score', fontsize=10)
    ax.set_title('6-Factor Discriminative Power', fontsize=12, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(factors, fontsize=10)
    ax.legend(frameon=False, loc='upper left')
    
    # Clean up borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.grid(axis='y', linestyle='--', alpha=0.5, color='#dddddd')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close('all')

if __name__ == "__main__":
    out_dir = r"d:\updated res\assets"
    os.makedirs(out_dir, exist_ok=True)
    
    perf_path = os.path.join(out_dir, "minimal_performance_chart.png")
    results_path = os.path.join(out_dir, "minimal_results_chart.png")
    
    generate_performance_chart(perf_path)
    generate_results_chart(results_path)
    
    print(f"Generated:\n{perf_path}\n{results_path}")
