"""
SparkMetricsLogger - Automated Spark Performance Metrics Logger

This module provides a logger to capture Spark execution metrics and save them to CSV.

Example:
    logger = SparkMetricsLogger(spark.sparkContext, "metrics.csv")
    
    logger.start()
    # ... Spark operations ...
    logger.end(run_id="run001", task_name="my_task", notes="params...")
"""

import csv
import requests
from datetime import datetime, timezone
from pathlib import Path
from time import time
from typing import Dict, Any, Optional


class SparkMetricsLogger:
    """
    Automated logger for capturing Spark job metrics.
    
    Attributes:
        sc: SparkContext instance
        output_path: Path to CSV file for logging
    """
    
    def __init__(self, spark_context, output_path: str):
        """
        Initialize the metrics logger.
        
        Args:
            spark_context: SparkContext instance
            output_path: Path where CSV logs will be saved
        """
        self.sc = spark_context
        self.output_path = Path(output_path)
        self.start_time = None
        self.end_time = None
        self._init_csv()
    
    def _init_csv(self):
        """Initialize CSV file with headers if it doesn't exist."""
        if not self.output_path.exists():
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'run_id', 'timestamp_utc', 'task', 
                    'files_read', 'size_read_MB', 'shuffle_read_MB', 'shuffle_write_MB',
                    'execution_time_sec', 'notes'
                ])
            print(f"✓ CSV log file initialized: {self.output_path}")
    
    def start(self):
        """Start the execution timer."""
        self.start_time = time()
    
    def end(self, run_id: str, task_name: str, notes: str = ""):
        """
        Log metrics for end of task execution.
        
        Args:
            run_id: Unique identifier for this run
            task_name: Name of the task/query
            notes: Optional notes about the run (parameters, config, etc.)
        """
        self.end_time = time()
        metrics = self._extract_metrics()
        self._save_metrics(run_id, task_name, metrics, notes)
    
    def _extract_metrics(self) -> Dict[str, Any]:
        """
        Extract Spark metrics from Spark UI REST API.
        
        Returns:
            Dictionary with keys: files_read, size_read_MB, shuffle_read_MB, 
                                  shuffle_write_MB, execution_time_sec
        """
        try:
            shuffle_read = 0.0
            shuffle_write = 0.0
            size_read = 0.0
            
            try:
                # Query Spark UI REST API
                response = requests.get("http://localhost:4040/api/v1/applications", timeout=2)
                if response.status_code == 200:
                    apps = response.json()
                    if apps:
                        app_id = apps[0]['id']
                        
                        # Get stages information
                        stages_response = requests.get(
                            f"http://localhost:4040/api/v1/applications/{app_id}/stages",
                            timeout=2
                        )
                        stages = stages_response.json()
                        
                        if stages:
                            # Get the last/most recent stage
                            last_stage = max(stages, key=lambda s: s.get('stageId', -1))
                            shuffle_read = last_stage.get('shuffleReadBytes', 0) / (1024**2)
                            shuffle_write = last_stage.get('shuffleWriteBytes', 0) / (1024**2)
                            size_read = last_stage.get('inputBytes', 0) / (1024**2)
            
            except requests.exceptions.RequestException as e:
                print(f"⚠ Warning: Could not connect to Spark UI ({e})")
            except (KeyError, IndexError, ValueError) as e:
                print(f"⚠ Warning: Could not parse Spark UI response ({e})")
            
            execution_time = self.end_time - self.start_time if self.start_time else 0
            
            return {
                'files_read': 0,
                'size_read_MB': round(size_read, 2),
                'shuffle_read_MB': round(shuffle_read, 2),
                'shuffle_write_MB': round(shuffle_write, 2),
                'execution_time_sec': round(execution_time, 2)
            }
        
        except Exception as e:
            print(f"⚠ Error extracting metrics: {e}")
            return {
                'files_read': 0,
                'size_read_MB': 0,
                'shuffle_read_MB': 0,
                'shuffle_write_MB': 0,
                'execution_time_sec': 0
            }
    
    def _save_metrics(self, run_id: str, task_name: str, metrics: Dict[str, Any], notes: str):
        """Save metrics to CSV file."""
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        with open(self.output_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                run_id,
                timestamp,
                task_name,
                metrics['files_read'],
                metrics['size_read_MB'],
                metrics['shuffle_read_MB'],
                metrics['shuffle_write_MB'],
                metrics['execution_time_sec'],
                notes
            ])
        
        print(f"✓ Logged: {run_id:<20} | {task_name:<30} | {metrics['execution_time_sec']:>6.2f}s")
    
    def summary(self, df_module=None) -> Optional[Any]:
        """
        Display summary of all logged metrics.
        
        Args:
            df_module: pandas module (if available, displays as DataFrame)
        
        Returns:
            pandas DataFrame if df_module provided, else None
        """
        try:
            if df_module is None:
                import pandas as pd
                df_module = pd
            
            df = df_module.read_csv(self.output_path)
            print("\n" + "="*100)
            print("METRICS SUMMARY")
            print("="*100)
            print(df.to_string(index=False))
            print("="*100)
            return df
        except ImportError:
            print("pandas not available, reading raw CSV...")
            with open(self.output_path, 'r') as f:
                print(f.read())
            return None


# Convenience function for quick setup
def create_logger(spark_context, output_dir: str = "outputs") -> SparkMetricsLogger:
    """
    Create a SparkMetricsLogger with default settings.
    
    Args:
        spark_context: SparkContext instance
        output_dir: Directory for log files
    
    Returns:
        Configured SparkMetricsLogger instance
    """
    log_path = Path(output_dir) / "spark_metrics_log.csv"
    return SparkMetricsLogger(spark_context, str(log_path))


if __name__ == "__main__":
    print("SparkMetricsLogger module loaded successfully")
