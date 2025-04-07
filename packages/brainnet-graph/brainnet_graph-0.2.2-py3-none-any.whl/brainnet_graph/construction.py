import argparse
import os
import pandas as pd
import torch
import numpy as np
from torch_geometric.data import Data
from .methods import *
# from .methods import (
#     pearson_correlation,
#     cosine_similarity,
#     partial_correlation,
#     correlation_matrix_to_graph_data,
# )

SUPPORTED_METHODS = {
    "pearson_correlation": pearson_correlation,
    "cosine_similarity": cosine_similarity,
    "partial_correlation": partial_correlation,
    "correlations_correlation": correlations_correlation,
    "associated_high_order_fc": associated_high_order_fc,
    "euclidean_distance": euclidean_distance,
    "knn_graph": knn_graph,
    "spearman_correlation": spearman_correlation,
    "kendall_correlation": kendall_correlation,
    "mutual_information": mutual_information,
    "cross_correlation": cross_correlation,
    "granger_causality": granger_causality,
    "generalised_synchronisation_matrix": generalised_synchronisation_matrix, # very slow
    "patels_conditional_dependence_measures_kappa": patels_conditional_dependence_measures_kappa,
    "patels_conditional_dependence_measures_tau": patels_conditional_dependence_measures_tau,
    "lingam": lingam, # very slow
}

def load_data(input_path: str) -> pd.DataFrame:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    ext = os.path.splitext(input_path)[-1].lower()
    if ext == ".csv":
        df = pd.read_csv(input_path)
    elif ext == ".tsv":
        df = pd.read_csv(input_path, sep="\t")
    elif ext == ".pkl":
        df = pd.read_pickle(input_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
    return df

def validate_data(df: pd.DataFrame):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")
    if df.empty:
        raise ValueError("Input data is empty.")
    if df.shape[1] < 2:
        raise ValueError("Input must contain at least 2 ROIs (columns).")
    if df.shape[0] < 5:
        raise ValueError("Too few time points (rows).")

def construct_graph(df: pd.DataFrame, method_name: str) -> Data:
    if method_name not in SUPPORTED_METHODS:
        raise ValueError(f"Unsupported method '{method_name}'. Choose from: {list(SUPPORTED_METHODS)}")
    matrix = SUPPORTED_METHODS[method_name](df)
    graph = correlation_matrix_to_graph_data(matrix)
    return graph

def save_graph(graph: Data, output_path: str, fmt: str = "csv"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if fmt == "pt":
        torch.save(graph, output_path)
        print(f"Graph (PyTorch Geometric) saved to: {output_path}")
    elif fmt == "csv":
        edge_index = graph.edge_index.cpu().numpy()
        edge_attr = graph.edge_attr.cpu().numpy() if graph.edge_attr is not None else None
        df_edges = pd.DataFrame({
            "source": edge_index[0],
            "target": edge_index[1],
            "weight": edge_attr.flatten() if edge_attr is not None else 1.0
        })
        df_edges.to_csv(output_path, index=False)
        print(f"Graph edges saved as CSV to: {output_path}")
    else:
        raise ValueError(f"Unsupported format: {fmt}")

def run_demo(output_path: str, fmt: str, method: str):
    time_points = 100
    num_rois = 10
    rng = np.random.RandomState(42)
    data = rng.rand(time_points, num_rois)
    df = pd.DataFrame(data, columns=[f"ROI_{i}" for i in range(num_rois)])

    print("Running demo with simulated BOLD signal.")
    validate_data(df)
    graph = construct_graph(df, method)
    save_graph(graph, output_path, fmt=fmt)
    print("Demo completed.")

def main():
    parser = argparse.ArgumentParser(description="Construct a graph from BOLD signal data.")
    parser.add_argument("--input", "-i", type=str, help="Path to input BOLD signal data (.csv/.tsv/.pkl)")
    parser.add_argument("--output", "-o", type=str, help="Path to save the output graph")
    parser.add_argument("--method", "-m", type=str, default="pearson_correlation", help="Graph construction method")
    parser.add_argument("--format", "-f", type=str, choices=["csv", "pt"], default="csv", help="Output format")
    parser.add_argument("--demo", action="store_true", help="Run in demo mode with simulated data")

    args = parser.parse_args()

    if args.demo:
        output_path = args.output if args.output else "./demo_graph." + args.format
        run_demo(output_path, fmt=args.format, method=args.method)
        return

    if not args.input or not args.output:
        parser.error("--input and --output are required unless running --demo")

    df = load_data(args.input)
    validate_data(df)
    graph = construct_graph(df, args.method)
    save_graph(graph, args.output, fmt=args.format)

if __name__ == "__main__":
    main()
