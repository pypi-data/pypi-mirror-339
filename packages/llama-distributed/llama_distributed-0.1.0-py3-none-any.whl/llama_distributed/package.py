"""
llama_distributed: A cloud-native distributed query processor for llama_vector shards.

This package orchestrates llama_vector shards with MLX-accelerated collective communication,
using asyncio for concurrency, CRDTs for metadata synchronization, and advanced routing
and optimization capabilities.
"""

import asyncio
import hashlib
import json
import logging
import os
import random
import tempfile
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import aiohttp
import kubernetes
# 3rd party imports
import mlx.core as mx
import numpy as np
from cryptography.fernet import Fernet
from kubernetes import client as k8s_client
from kubernetes.client.rest import ApiException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("llama_distributed")

# Constants
DEFAULT_TIMEOUT = 30  # seconds
MAX_RETRY_ATTEMPTS = 3
DEFAULT_BATCH_SIZE = 32
DEFAULT_PORT = 8080


# Main package components
class ShardMetadata:
    """
    CRDT-based metadata for vector shards.
    
    This class implements a Conflict-free Replicated Data Type (CRDT) for 
    synchronizing metadata across distributed vector shards. It handles 
    additions, removals, and updates in a way that guarantees eventual 
    consistency across the system.
    
    Attributes:
        shard_id: Unique identifier for this shard
        vector_dims: Dimensionality of vectors in this shard
        vector_count: Number of vectors currently in this shard
        last_updated: Timestamp of the last update
        lamport_clock: Logical clock for establishing causality
        node_stats: Current resource statistics for the node
    """
    
    def __init__(self, shard_id: str, vector_dims: int):
        """
        Initialize a new ShardMetadata instance.
        
        Args:
            shard_id: Unique identifier for this shard
            vector_dims: Dimensionality of vectors in this shard
        """
        self.shard_id = shard_id
        self.vector_dims = vector_dims
        self.vector_count = 0
        self.last_updated = time.time()
        self.lamport_clock = 0
        self.tombstones = set()
        self.node_stats = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "gpu_usage": 0.0,
            "power_consumption": 0.0,
            "temperature": 0.0,
        }
    
    def update(self, other: 'ShardMetadata') -> None:
        """
        Merge with another ShardMetadata using CRDT principles.
        
        Args:
            other: Another ShardMetadata instance to merge with
        """
        if self.shard_id != other.shard_id:
            raise ValueError("Cannot merge metadata from different shards")
        
        # Use the higher logical clock
        if other.lamport_clock > self.lamport_clock:
            self.lamport_clock = other.lamport_clock
            self.vector_count = other.vector_count
            self.last_updated = other.last_updated
        
        # Merge tombstones (deleted items)
        self.tombstones = self.tombstones.union(other.tombstones)
        
        # Update node stats with most recent data
        if other.last_updated > self.last_updated:
            self.node_stats = other.node_stats.copy()
    
    def increment_vectors(self, count: int = 1) -> None:
        """
        Increment the vector count and update the clock.
        
        Args:
            count: Number of vectors to add
        """
        self.vector_count += count
        self.lamport_clock += 1
        self.last_updated = time.time()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert metadata to a dictionary for serialization.
        
        Returns:
            Dictionary representation of the metadata
        """
        return {
            "shard_id": self.shard_id,
            "vector_dims": self.vector_dims,
            "vector_count": self.vector_count,
            "last_updated": self.last_updated,
            "lamport_clock": self.lamport_clock,
            "tombstones": list(self.tombstones),
            "node_stats": self.node_stats,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ShardMetadata':
        """
        Create a ShardMetadata instance from a dictionary.
        
        Args:
            data: Dictionary representation of metadata
            
        Returns:
            A new ShardMetadata instance
        """
        metadata = cls(data["shard_id"], data["vector_dims"])
        metadata.vector_count = data["vector_count"]
        metadata.last_updated = data["last_updated"]
        metadata.lamport_clock = data["lamport_clock"]
        metadata.tombstones = set(data["tombstones"])
        metadata.node_stats = data["node_stats"]
        return metadata


class QueryOptimizer:
    """
    A learned query optimizer with heuristic fallbacks.
    
    This optimizer analyzes queries and determines the most efficient execution
    strategy based on machine learning models and heuristic rules. It adapts
    to changing shard conditions and query patterns.
    
    Attributes:
        model: The ML model for query optimization
        stats_history: Historical performance statistics
        feature_extractor: Function to extract features from queries
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the QueryOptimizer.
        
        Args:
            model_path: Path to a saved optimization model (optional)
        """
        self.stats_history = []
        self.feature_cache = {}
        
        # Load model if provided, otherwise use heuristics
        self.model = None
        if model_path and os.path.exists(model_path):
            try:
                # In a real implementation, this would load a trained model
                logger.info(f"Loading query optimizer model from {model_path}")
                # self.model = load_model(model_path)
                self.use_ml = True
            except Exception as e:
                logger.warning(f"Failed to load optimizer model: {e}")
                self.use_ml = False
        else:
            logger.info("Using heuristic query optimization")
            self.use_ml = False
    
    def extract_features(self, query: Dict[str, Any]) -> np.ndarray:
        """
        Extract features from a query for optimization.
        
        Args:
            query: The query specification
            
        Returns:
            Array of numerical features for the model
        """
        # Query hash for caching
        query_str = json.dumps(query, sort_keys=True)
        query_hash = hashlib.md5(query_str.encode()).hexdigest()
        
        if query_hash in self.feature_cache:
            return self.feature_cache[query_hash]
        
        # Extract features (in a real implementation, this would be more sophisticated)
        features = np.array([
            len(query.get("vector", [])),  # Vector dimensionality
            len(query.get("filters", [])),  # Number of filters
            query.get("k", 10),  # Number of results requested
            query.get("timeout", DEFAULT_TIMEOUT) / DEFAULT_TIMEOUT,  # Normalized timeout
        ])
        
        self.feature_cache[query_hash] = features
        return features
    
    def optimize(self, query: Dict[str, Any], shards: List[ShardMetadata]) -> Dict[str, Any]:
        """
        Optimize a query for execution across shards.
        
        Args:
            query: The query specification
            shards: Available shards metadata
            
        Returns:
            Optimized query plan
        """
        start_time = time.time()
        
        if self.use_ml and self.model:
            try:
                features = self.extract_features(query)
                # In a real implementation, this would use the model to predict
                # the optimal execution strategy
                # prediction = self.model.predict(features)
                # Using a placeholder prediction for demonstration
                prediction = {"parallel_factor": 0.8, "timeout_factor": 1.2}
            except Exception as e:
                logger.warning(f"ML optimization failed: {e}, falling back to heuristics")
                prediction = self._heuristic_optimize(query, shards)
        else:
            prediction = self._heuristic_optimize(query, shards)
        
        # Apply the optimization
        optimized_query = query.copy()
        optimized_query["_execution_plan"] = {
            "parallel_shards": max(1, int(len(shards) * prediction["parallel_factor"])),
            "timeout": query.get("timeout", DEFAULT_TIMEOUT) * prediction["timeout_factor"],
            "optimization_time": time.time() - start_time,
        }
        
        return optimized_query
    
    def _heuristic_optimize(self, query: Dict[str, Any], shards: List[ShardMetadata]) -> Dict[str, Any]:
        """
        Apply heuristic rules for query optimization.
        
        Args:
            query: The query specification
            shards: Available shards metadata
            
        Returns:
            Optimization parameters
        """
        # Simple heuristic rules
        vector_size = len(query.get("vector", []))
        result_count = query.get("k", 10)
        
        # Parallel factor increases with more shards and larger result sets
        parallel_factor = min(1.0, 0.3 + (result_count / 100) + (len(shards) / 20))
        
        # Timeout factor increases with vector size and filter complexity
        timeout_factor = 1.0 + (vector_size / 1000) + (len(query.get("filters", [])) * 0.1)
        
        return {
            "parallel_factor": parallel_factor,
            "timeout_factor": timeout_factor,
        }
    
    def record_stats(self, query: Dict[str, Any], execution_time: float, success: bool) -> None:
        """
        Record query execution statistics for learning.
        
        Args:
            query: The executed query
            execution_time: Time taken to execute
            success: Whether execution was successful
        """
        if len(self.stats_history) > 1000:
            self.stats_history.pop(0)  # Keep history bounded
            
        self.stats_history.append({
            "features": self.extract_features(query).tolist(),
            "execution_time": execution_time,
            "success": success,
            "timestamp": time.time(),
            "plan": query.get("_execution_plan", {}),
        })


class NeuralRouter:
    """
    A neural router for request distribution across shards.
    
    This router uses a neural network to make intelligent routing decisions
    based on shard state, query characteristics, and historical performance.
    It supports plan-based routing for complex query execution.
    
    Attributes:
        model: The routing model
        shard_stats: Performance statistics for each shard
        fallback_strategy: Strategy to use if model fails
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the NeuralRouter.
        
        Args:
            model_path: Path to a saved routing model (optional)
        """
        self.shard_stats = {}
        self.route_history = []
        
        # Fallback routing strategies
        self.fallback_strategies = {
            "random": self._random_routing,
            "round_robin": self._round_robin_routing,
            "least_loaded": self._least_loaded_routing,
        }
        self.current_fallback = "least_loaded"
        self.rr_index = 0
        
        # Load model if provided
        self.model = None
        if model_path and os.path.exists(model_path):
            try:
                # In a real implementation, this would load a trained model
                logger.info(f"Loading neural router model from {model_path}")
                # self.model = load_model(model_path)
                self.use_ml = True
            except Exception as e:
                logger.warning(f"Failed to load router model: {e}")
                self.use_ml = False
        else:
            logger.info("Using heuristic routing")
            self.use_ml = False
    
    def route(self, query: Dict[str, Any], shards: List[ShardMetadata]) -> List[str]:
        """
        Determine the optimal routing for a query.
        
        Args:
            query: The query to route
            shards: Available shards
            
        Returns:
            List of shard IDs in execution order
        """
        if not shards:
            return []
            
        # Extract the execution plan if available
        plan = query.get("_execution_plan", {})
        parallel_count = plan.get("parallel_shards", len(shards))
        
        if self.use_ml and self.model:
            try:
                # In a real implementation, this would use the model to predict routing
                # features = self._extract_routing_features(query, shards)
                # routing_scores = self.model.predict(features)
                
                # Use placeholder scores for demonstration
                routing_scores = {
                    shard.shard_id: random.random() for shard in shards
                }
                
                # Select top shards based on predicted scores
                selected_shards = sorted(
                    shards, 
                    key=lambda s: routing_scores.get(s.shard_id, 0.0), # Use 0.0 as default score
                    reverse=True
                )[:parallel_count]
                
                # Return the IDs of the selected shards
                return [s.shard_id for s in selected_shards]

            except Exception as e:
                logger.warning(f"Neural routing failed: {e}, using fallback strategy '{self.current_fallback}'")
                # Fall through to use the fallback strategy below if ML routing fails
                pass # Explicitly pass to indicate fallback
            
        # Fallback strategy if ML is not used or failed
        fallback_strategy_func = self.fallback_strategies.get(self.current_fallback, self._least_loaded_routing)
        return fallback_strategy_func(query, shards, parallel_count)
    
    def _random_routing(self, query: Dict[str, Any], shards: List[ShardMetadata], count: int) -> List[str]:
        """Random routing strategy."""
        selected = random.sample(shards, min(count, len(shards)))
        return [s.shard_id for s in selected]
    
    def _round_robin_routing(self, query: Dict[str, Any], shards: List[ShardMetadata], count: int) -> List[str]:
        """Round-robin routing strategy."""
        selected = []
        for _ in range(count):
            selected.append(shards[self.rr_index % len(shards)])
            self.rr_index += 1
        return [s.shard_id for s in selected]
    
    def _least_loaded_routing(self, query: Dict[str, Any], shards: List[ShardMetadata], count: int) -> List[str]:
        """Route to least loaded shards."""
        # Sort by CPU usage (lower is better)
        sorted_shards = sorted(shards, key=lambda s: s.node_stats["cpu_usage"])
        selected = sorted_shards[:count]
        return [s.shard_id for s in selected]
    
    def update_stats(self, shard_id: str, query_time: float, success: bool) -> None:
        """
        Update performance statistics for a shard.
        
        Args:
            shard_id: ID of the shard
            query_time: Time taken to process the query
            success: Whether the query was successful
        """
        if shard_id not in self.shard_stats:
            self.shard_stats[shard_id] = {
                "avg_query_time": query_time,
                "success_rate": 1.0 if success else 0.0,
                "query_count": 1,
                "last_failure": None if success else time.time(),
            }
        else:
            stats = self.shard_stats[shard_id]
            # Exponential moving average for query time
            stats["avg_query_time"] = (0.9 * stats["avg_query_time"]) + (0.1 * query_time)
            # Update success rate
            success_count = stats["success_rate"] * stats["query_count"]
            stats["query_count"] += 1
            stats["success_rate"] = (success_count + (1 if success else 0)) / stats["query_count"]
            # Update last failure
            if not success:
                stats["last_failure"] = time.time()
    
    def record_route(self, query: Dict[str, Any], selected_shards: List[str], execution_time: float) -> None:
        """
        Record routing decisions for learning.
        
        Args:
            query: The executed query
            selected_shards: Shards selected for this query
            execution_time: Time taken to execute
        """
        if len(self.route_history) > 1000:
            self.route_history.pop(0)  # Keep history bounded
            
        self.route_history.append({
            "query_hash": hashlib.md5(json.dumps(query, sort_keys=True).encode()).hexdigest(),
            "selected_shards": selected_shards,
            "execution_time": execution_time,
            "timestamp": time.time(),
        })


class FederatedRanker:
    """
    A federated ranker for merging and ranking results.
    
    This ranker combines results from multiple shards, ranks them according
    to relevance criteria, and optionally adds differential privacy noise
    for privacy protection.
    
    Attributes:
        ranking_method: Method used for ranking
        noise_scale: Scale of DP noise to add
        add_noise: Whether to add DP noise
    """
    
    class RankingMethod(Enum):
        DISTANCE = "distance"
        SCORE = "score"
        HYBRID = "hybrid"
        CUSTOM = "custom"
    
    def __init__(
        self, 
        ranking_method: str = "distance", 
        add_noise: bool = False, 
        noise_scale: float = 0.1,
        custom_ranking_fn: Optional[Callable] = None
    ):
        """
        Initialize the FederatedRanker.
        
        Args:
            ranking_method: Method for ranking ('distance', 'score', 'hybrid', 'custom')
            add_noise: Whether to add differential privacy noise
            noise_scale: Scale of noise to add (higher = more privacy)
            custom_ranking_fn: Custom ranking function (used if method is 'custom')
        """
        try:
            self.ranking_method = self.RankingMethod(ranking_method)
        except ValueError:
            logger.warning(f"Invalid ranking method {ranking_method}, using 'distance'")
            self.ranking_method = self.RankingMethod.DISTANCE
            
        self.add_noise = add_noise
        self.noise_scale = noise_scale
        self.custom_ranking_fn = custom_ranking_fn
    
    def merge_and_rank(
        self, 
        query: Dict[str, Any], 
        shard_results: List[Dict[str, Any]], 
        k: int
    ) -> List[Dict[str, Any]]:
        """
        Merge and rank results from multiple shards.
        
        Args:
            query: The original query
            shard_results: Results from each shard
            k: Number of results to return
            
        Returns:
            Ranked list of results
        """
        # Flatten results from all shards
        all_results = []
        for shard_result in shard_results:
            if "results" in shard_result:
                all_results.extend(shard_result["results"])
        
        # Check if we need to rank
        if not all_results:
            return []
        
        # Apply appropriate ranking
        if self.ranking_method == self.RankingMethod.DISTANCE:
            ranked_results = sorted(all_results, key=lambda x: x.get("distance", float('inf')))
        elif self.ranking_method == self.RankingMethod.SCORE:
            ranked_results = sorted(all_results, key=lambda x: x.get("score", 0), reverse=True)
        elif self.ranking_method == self.RankingMethod.HYBRID:
            # Normalize distances and scores to [0, 1]
            max_distance = max(r.get("distance", 0) for r in all_results) or 1
            max_score = max(r.get("score", 0) for r in all_results) or 1
            
            for r in all_results:
                r["_normalized_distance"] = r.get("distance", max_distance) / max_distance
                r["_normalized_score"] = r.get("score", 0) / max_score
                r["_hybrid_score"] = r["_normalized_score"] - r["_normalized_distance"]
            
            ranked_results = sorted(all_results, key=lambda x: x.get("_hybrid_score", -1), reverse=True)
        elif self.ranking_method == self.RankingMethod.CUSTOM and self.custom_ranking_fn:
            ranked_results = self.custom_ranking_fn(all_results, query)
        else:
            # Fallback to distance
            ranked_results = sorted(all_results, key=lambda x: x.get("distance", float('inf')))
        
        # Add differential privacy noise if requested
        if self.add_noise and self.noise_scale > 0:
            ranked_results = self._add_dp_noise(ranked_results)
            # Re-sort after adding noise
            if self.ranking_method == self.RankingMethod.DISTANCE:
                ranked_results = sorted(ranked_results, key=lambda x: x.get("distance", float('inf')))
            elif self.ranking_method == self.RankingMethod.SCORE:
                ranked_results = sorted(ranked_results, key=lambda x: x.get("score", 0), reverse=True)
            elif self.ranking_method == self.RankingMethod.HYBRID:
                ranked_results = sorted(ranked_results, key=lambda x: x.get("_hybrid_score", -1), reverse=True)
        
        # Remove temporary ranking fields
        for r in ranked_results:
            r.pop("_normalized_distance", None)
            r.pop("_normalized_score", None)
            r.pop("_hybrid_score", None)
        
        # Deduplicate by ID if present
        seen_ids = set()
        deduplicated_results = []
        for r in ranked_results:
            item_id = r.get("id")
            if item_id is None or item_id not in seen_ids:
                if item_id is not None:
                    seen_ids.add(item_id)
                deduplicated_results.append(r)
        
        # Return top k results
        return deduplicated_results[:k]
    
    def _add_dp_noise(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Add differential privacy noise to results.
        
        Args:
            results: List of result items
            
        Returns:
            Results with noise added
        """
        noisy_results = []
        for result in results:
            noisy_result = result.copy()
            
            # Add Laplace noise to distance
            if "distance" in noisy_result:
                noise = np.random.laplace(0, self.noise_scale)
                noisy_result["distance"] = max(0, noisy_result["distance"] + noise)
            
            # Add Laplace noise to score
            if "score" in noisy_result:
                noise = np.random.laplace(0, self.noise_scale)
                noisy_result["score"] = noisy_result["score"] + noise
            
            noisy_results.append(noisy_result)
        
        return noisy_results


class EnergyAwareLoadBalancer:
    """
    Energy-aware load balancer based on node statistics.
    
    This load balancer distributes workloads with consideration for energy
    efficiency, prioritizing nodes with lower power consumption while still
    maintaining performance.
    
    Attributes:
        energy_weight: Weight given to energy considerations
        performance_weight: Weight given to performance considerations
        node_stats: Current statistics for all nodes
    """
    
    def __init__(self, energy_weight: float = 0.3, performance_weight: float = 0.7):
        """
        Initialize the EnergyAwareLoadBalancer.
        
        Args:
            energy_weight: Weight for energy efficiency (0-1)
            performance_weight: Weight for performance (0-1)
        """
        if energy_weight + performance_weight != 1.0:
            logger.warning("Weights don't sum to 1.0, normalizing")
            total = energy_weight + performance_weight
            energy_weight /= total
            performance_weight /= total
            
        self.energy_weight = energy_weight
        self.performance_weight = performance_weight
        self.node_stats = {}
    
    def update_node_stats(self, node_id: str, stats: Dict[str, float]) -> None:
        """
        Update statistics for a node.
        
        Args:
            node_id: ID of the node
            stats: Current resource statistics
        """
        self.node_stats[node_id] = {
            "stats": stats,
            "last_updated": time.time(),
        }
    
    def get_node_ranking(self, shards: List[ShardMetadata]) -> List[Tuple[str, float]]:
        """
        Rank nodes based on energy efficiency and performance.
        
        Args:
            shards: List of available shards
            
        Returns:
            List of (shard_id, score) tuples, sorted by score (higher is better)
        """
        if not shards:
            return []
            
        scores = []
        for shard in shards:
            # Calculate energy score (lower power consumption is better)
            power = shard.node_stats.get("power_consumption", 0)
            temp = shard.node_stats.get("temperature", 0)
            energy_score = 1.0 - min(1.0, (power / 100.0 + temp / 80.0) / 2)
            
            # Calculate performance score (lower CPU/GPU usage is better)
            cpu = shard.node_stats.get("cpu_usage", 0)
            gpu = shard.node_stats.get("gpu_usage", 0)
            memory = shard.node_stats.get("memory_usage", 0)
            perf_score = 1.0 - min(1.0, (cpu + gpu + memory) / 3)
            
            # Combined score
            combined_score = (
                self.energy_weight * energy_score + 
                self.performance_weight * perf_score
            )
            
            scores.append((shard.shard_id, combined_score))
        
        # Sort by score (higher is better)
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def assign_workloads(self, workloads: List[Dict[str, Any]], shards: List[ShardMetadata]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Assign workloads to shards based on energy-aware ranking.
        
        Args:
            workloads: List of workload items to assign
            shards: Available shards
            
        Returns:
            Dictionary mapping shard IDs to assigned workloads
        """
        if not workloads or not shards:
            return {}
        
        # Get ranked list of shards
        ranked_shards = self.get_node_ranking(shards)
        if not ranked_shards:
            return {}
        
        # Distribute workloads proportionally to scores
        total_score = sum(score for _, score in ranked_shards)
        shard_allocations = {
            shard_id: max(1, int(len(workloads) * (score / total_score)))
            for shard_id, score in ranked_shards
        }
        
        # Adjust if total allocation doesn't match workload count
        total_allocated = sum(shard_allocations.values())
        diff = len(workloads) - total_allocated
        
        if diff > 0:
            # Need to allocate more
            for shard_id, _ in ranked_shards[:diff]:
                shard_allocations[shard_id] += 1
        elif diff < 0:
            # Need to allocate fewer
            for shard_id, _ in reversed(ranked_shards[:abs(diff)]):
                if shard_allocations[shard_id] > 1:  # Don't reduce to zero
                    shard_allocations[shard_id] -= 1
        
        # Distribute workloads
        result = {shard_id: [] for shard_id, _ in ranked_shards}
        workload_index = 0
        
        for shard_id, allocation in sorted(
            shard_allocations.items(), 
            key=lambda x: ranked_shards.index((x[0], 0))
        ):
            for _ in range(allocation):
                if workload_index < len(workloads):
                    result[shard_id].append(workloads[workload_index])
                    workload_index += 1
        
        return result


class KubernetesManager:
    """
    Kubernetes integration for KEDA-based autoscaling.
    
    This class manages Kubernetes resources for the distributed system,
    including deployment configuration, autoscaling with KEDA, and
    health monitoring.
    
    Attributes:
        namespace: Kubernetes namespace
        deployment_name: Name of the deployment
        k8s_client: Kubernetes API client
    """
    
    def __init__(self, namespace: str = "default", deployment_name: str = "llama-distributed"):
        """
        Initialize the KubernetesManager.
        
        Args:
            namespace: Kubernetes namespace
            deployment_name: Name of the deployment
        """
        self.namespace = namespace
        self.deployment_name = deployment_name
        
        # Initialize Kubernetes client
        try:
            kubernetes.config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes configuration")
        except kubernetes.config.ConfigException:
            try:
                kubernetes.config.load_kube_config()
                logger.info("Loaded local Kubernetes configuration")
            except kubernetes.config.ConfigException:
                logger.warning("Could not load Kubernetes configuration")
        
        self.apps_api = k8s_client.AppsV1Api()
        self.core_api = k8s_client.CoreV1Api()
        self.custom_api = k8s_client.CustomObjectsApi()
    
    def get_pod_status(self) -> List[Dict[str, Any]]:
        """
        Get status information for all pods in the deployment.
        
        Returns:
            List of pod status dictionaries
        """
        try:
            pods = self.core_api.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"app={self.deployment_name}"
            )
            
            result = []
            for pod in pods.items:
                status = {
                    "name": pod.metadata.name,
                    "status": pod.status.phase,
                    "ip": pod.status.pod_ip,
                    "start_time": pod.status.start_time,
                    "restarts": sum(cs.restart_count for cs in pod.status.container_statuses or [])
                }
                result.append(status)
            
            return result
        except ApiException as e:
            logger.error(f"Error getting pod status: {e}")
            return []

    def create_scaled_object(self, min_replicas: int = 1, max_replicas: int = 10) -> bool:
        """
        Create a KEDA ScaledObject for autoscaling.
        
        Args:
            min_replicas: Minimum number of replicas
            max_replicas: Maximum number of replicas
            
        Returns:
            True if successful, False otherwise
        """
        scaled_object = {
            "apiVersion": "keda.sh/v1alpha1",
            "kind": "ScaledObject",
            "metadata": {
                "name": f"{self.deployment_name}-scaler",
                "namespace": self.namespace,
            },
            "spec": {
                "scaleTargetRef": {
                    "name": self.deployment_name,
                    "kind": "Deployment",
                },
                "minReplicaCount": min_replicas,
                "maxReplicaCount": max_replicas,
                "triggers": [
                    {
                        "type": "prometheus",
                        "metadata": {
                            "serverAddress": "http://prometheus-server.monitoring.svc.cluster.local",
                            "metricName": "query_queue_length",
                            "threshold": "5",
                            "query": f'sum(llama_distributed_query_queue{{deployment="{self.deployment_name}"}})'
                        }
                    },
                    {
                        "type": "cpu",
                        "metadata": {
                            "type": "Utilization",
                            "value": "80"
                        }
                    }
                ]
            }
        }
        
        try:
            self.custom_api.create_namespaced_custom_object(
                group="keda.sh",
                version="v1alpha1",
                namespace=self.namespace,
                plural="scaledobjects",
                body=scaled_object
            )
            logger.info(f"Created KEDA ScaledObject for {self.deployment_name}")
            return True
        except ApiException as e:
            logger.error(f"Error creating ScaledObject: {e}")
            return False
    
    def update_deployment(self, image: str, replicas: int = 2, resources: Dict[str, Any] = None) -> bool:
        """
        Update the Kubernetes deployment.
        
        Args:
            image: Container image to use
            replicas: Number of replicas
            resources: Resource requests and limits
            
        Returns:
            True if successful, False otherwise
        """
        if resources is None:
            resources = {
                "requests": {
                    "cpu": "100m",
                    "memory": "256Mi"
                },
                "limits": {
                    "cpu": "1000m",
                    "memory": "1Gi"
                }
            }
        
        try:
            # Get current deployment
            deployment = self.apps_api.read_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace
            )
            
            # Update deployment
            deployment.spec.replicas = replicas
            deployment.spec.template.spec.containers[0].image = image
            deployment.spec.template.spec.containers[0].resources = resources
            
            # Apply changes
            self.apps_api.patch_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace,
                body=deployment
            )
            
            logger.info(f"Updated deployment {self.deployment_name}")
            return True
        except ApiException as e:
            if e.status == 404:
                # Deployment doesn't exist, create it
                return self._create_deployment(image, replicas, resources)
            logger.error(f"Error updating deployment: {e}")
            return False
    
    def _create_deployment(self, image: str, replicas: int = 2, resources: Dict[str, Any] = None) -> bool:
        """
        Create a new Kubernetes deployment.
        
        Args:
            image: Container image to use
            replicas: Number of replicas
            resources: Resource requests and limits
            
        Returns:
            True if successful, False otherwise
        """
        if resources is None:
            resources = {
                "requests": {
                    "cpu": "100m",
                    "memory": "256Mi"
                },
                "limits": {
                    "cpu": "1000m",
                    "memory": "1Gi"
                }
            }
        
        deployment = k8s_client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=k8s_client.V1ObjectMeta(
                name=self.deployment_name,
                namespace=self.namespace,
                labels={"app": self.deployment_name}
            ),
            spec=k8s_client.V1DeploymentSpec(
                replicas=replicas,
                selector=k8s_client.V1LabelSelector(
                    match_labels={"app": self.deployment_name}
                ),
                template=k8s_client.V1PodTemplateSpec(
                    metadata=k8s_client.V1ObjectMeta(
                        labels={"app": self.deployment_name}
                    ),
                    spec=k8s_client.V1PodSpec(
                        containers=[
                            k8s_client.V1Container(
                                name="llama-distributed",
                                image=image,
                                ports=[k8s_client.V1ContainerPort(container_port=DEFAULT_PORT)],
                                resources=resources,
                                env=[
                                    k8s_client.V1EnvVar(
                                        name="NAMESPACE",
                                        value=self.namespace
                                    ),
                                    k8s_client.V1EnvVar(
                                        name="POD_NAME",
                                        value_from=k8s_client.V1EnvVarSource(
                                            field_ref=k8s_client.V1ObjectFieldSelector(
                                                field_path="metadata.name"
                                            )
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        )
        
        try:
            self.apps_api.create_namespaced_deployment(
                namespace=self.namespace,
                body=deployment
            )
            logger.info(f"Created deployment {self.deployment_name}")
            
            # Create a service for the deployment
            service = k8s_client.V1Service(
                api_version="v1",
                kind="Service",
                metadata=k8s_client.V1ObjectMeta(
                    name=self.deployment_name,
                    namespace=self.namespace
                ),
                spec=k8s_client.V1ServiceSpec(
                    selector={"app": self.deployment_name},
                    ports=[k8s_client.V1ServicePort(port=DEFAULT_PORT)]
                )
            )
            
            self.core_api.create_namespaced_service(
                namespace=self.namespace,
                body=service
            )
            logger.info(f"Created service for {self.deployment_name}")
            
            return True
        except ApiException as e:
            logger.error(f"Error creating deployment: {e}")
            return False
    
    def get_deployment_metrics(self) -> Dict[str, Any]:
        """
        Get metrics for the deployment.
        
        Returns:
            Dictionary of metrics
        """
        try:
            # This would normally use the Metrics API
            # For now, just return basic information
            deployment = self.apps_api.read_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace
            )
            
            return {
                "desired_replicas": deployment.spec.replicas,
                "available_replicas": deployment.status.available_replicas or 0,
                "ready_replicas": deployment.status.ready_replicas or 0,
                "unavailable_replicas": deployment.status.unavailable_replicas or 0,
                "updated_replicas": deployment.status.updated_replicas or 0,
            }
        except ApiException as e:
            logger.error(f"Error getting deployment metrics: {e}")
            return {}