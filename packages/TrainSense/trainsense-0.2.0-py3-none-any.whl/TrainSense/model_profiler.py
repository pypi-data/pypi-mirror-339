# TrainSense/model_profiler.py
import torch
import torch.nn as nn
import time
import logging
from typing import Tuple, Dict, Any, Optional, Union, Callable, Iterable # Added Callable, Iterable
# Corrected import: Removed KinetoEvent, keep others
from torch.profiler import profile, record_function, ProfilerActivity, schedule
# Added imports needed for training step profiling
from torch.optim import Optimizer
from torch.utils.data import DataLoader

from .utils import format_bytes, format_time, validate_positive_integer

logger = logging.getLogger(__name__)

class ModelProfiler:
    def __init__(self, model: nn.Module, device: Optional[Union[str, torch.device]] = None):
        if not isinstance(model, nn.Module):
            raise TypeError("Input 'model' must be an instance of torch.nn.Module.")

        self.model = model
        self.device = self._resolve_device(device)
        self.model.to(self.device)
        logger.info(f"ModelProfiler initialized for model {type(model).__name__} on device '{self.device}'")

    def _resolve_device(self, device: Optional[Union[str, torch.device]]) -> torch.device:
        if device:
            return torch.device(device)
        elif torch.cuda.is_available():
            return torch.device("cuda")
        else:
             return torch.device("cpu")

    def _generate_dummy_input(self, input_shape: Tuple[int, ...]) -> torch.Tensor:
        logger.debug(f"Generating dummy input tensor with shape: {input_shape}")
        try:
            # Basic tensor creation, assumes float32
            # Consider adding dtype parameter if needed
            return torch.randn(*input_shape, device=self.device)
        except Exception as e:
            logger.error(f"Failed to create dummy tensor with shape {input_shape} on device {self.device}: {e}", exc_info=True)
            raise ValueError(f"Failed to create dummy input with shape {input_shape}: {e}") from e

    def _generate_dummy_target(self, output: torch.Tensor, criterion: nn.Module) -> torch.Tensor:
        """Generates a dummy target compatible with the output and criterion."""
        target_shape = output.shape
        try:
            # Handle common loss types
            if isinstance(criterion, (nn.CrossEntropyLoss, nn.NLLLoss)):
                # Requires class indices (long) for classification
                num_classes = output.shape[-1]
                # Create random indices within batch size, ensure correct shape
                if len(output.shape) == 2: # Simple (batch, classes) output
                     return torch.randint(0, num_classes, (target_shape[0],), device=self.device, dtype=torch.long)
                else: # Might be segmentation or other task, needs more specific handling
                     logger.warning(f"Automatic target generation for criterion {type(criterion).__name__} with output shape {output.shape} is complex. Using zeros. Provide target_generator if needed.")
                     return torch.zeros(target_shape[0], *target_shape[2:], device=self.device, dtype=torch.long) # Guess spatial target
            elif isinstance(criterion, (nn.MSELoss, nn.L1Loss, nn.BCELoss, nn.BCEWithLogitsLoss)):
                # Requires target with same shape and type as output (usually float)
                return torch.randn_like(output)
            else:
                # Fallback: create zeros with same shape
                 logger.warning(f"Unsupported criterion type {type(criterion).__name__} for automatic target generation. Using zeros. Provide target_generator if needed.")
                 return torch.zeros_like(output)
        except Exception as e:
            logger.error(f"Failed to generate dummy target for output shape {output.shape} and criterion {type(criterion).__name__}: {e}", exc_info=True)
            raise ValueError("Failed to generate dummy target.") from e

    # --- profile_model method remains the same as before ---
    def profile_model(self,
                      input_shape: Tuple[int, ...],
                      iterations: int = 50,
                      warmup: int = 10,
                      use_torch_profiler: bool = True,
                      profiler_activities: Optional[list] = None,
                      profiler_sort_by: str = "self_cpu_time_total",
                      profiler_row_limit: int = 10
                     ) -> Dict[str, Any]:
        # ... (keep the existing implementation from the previous corrected version) ...
        validate_positive_integer(iterations, "Profiling iterations")
        validate_positive_integer(warmup, "Profiling warmup iterations", allow_zero=True)

        if not isinstance(input_shape, tuple) or not all(isinstance(d, int) and d > 0 for d in input_shape):
            raise ValueError(f"input_shape must be a tuple of positive integers, got {input_shape}.")

        logger.info(f"[Inference Profiling] Starting: input_shape={input_shape}, iterations={iterations}, warmup={warmup}, device={self.device}, use_torch_profiler={use_torch_profiler}")

        self.model.eval() # Set to evaluation mode for inference profiling
        dummy_input = self._generate_dummy_input(input_shape)
        results: Dict[str, Any] = {
            "profiling_type": "inference",
            "input_shape": input_shape,
            "device": str(self.device),
            "iterations": iterations,
            "warmup": warmup,
            "use_torch_profiler": use_torch_profiler,
        }

        if self.device.type == 'cuda':
            torch.cuda.reset_peak_memory_stats(self.device)
            torch.cuda.empty_cache()

        try:
             with torch.no_grad(): # No gradients needed for inference
                 logger.debug("[Inference Profiling] Running warmup...")
                 for _ in range(warmup):
                     _ = self.model(dummy_input)
                 if self.device.type == 'cuda':
                     torch.cuda.synchronize(self.device)
                 logger.debug("[Inference Profiling] Warmup complete.")

                 logger.debug("[Inference Profiling] Running timed iterations...")
                 start_time = time.perf_counter()
                 for _ in range(iterations):
                     _ = self.model(dummy_input)
                 if self.device.type == 'cuda':
                     torch.cuda.synchronize(self.device)
                 end_time = time.perf_counter()

                 total_time_sec = end_time - start_time
                 avg_total_time_sec = total_time_sec / iterations if iterations > 0 else 0
                 throughput = iterations / total_time_sec if total_time_sec > 0 else float('inf')

                 results["avg_total_time_ms"] = avg_total_time_sec * 1000
                 results["throughput_samples_per_sec"] = throughput
                 results["total_timed_duration_sec"] = total_time_sec
                 logger.info(f"[Inference Profiling] Basic timing complete: Avg time={results['avg_total_time_ms']:.2f} ms, Throughput={throughput:.2f} samples/sec")

                 if use_torch_profiler:
                     logger.info("[Inference Profiling] Running detailed profiling with torch.profiler...")
                     # (Profiler setup and execution logic as before)
                     if profiler_activities is None:
                          profiler_activities = [ProfilerActivity.CPU]
                          if self.device.type == 'cuda':
                               profiler_activities.append(ProfilerActivity.CUDA)
                     profile_iterations = min(iterations, 10)
                     profile_warmup = min(warmup, 5)
                     wait = 1
                     prof_schedule = schedule(wait=wait, warmup=profile_warmup, active=profile_iterations, repeat=1)
                     num_profiler_steps = wait + profile_warmup + profile_iterations

                     try:
                         with profile(activities=profiler_activities, record_shapes=True, profile_memory=True, with_stack=False, schedule=prof_schedule) as prof:
                             for i in range(num_profiler_steps):
                                 with record_function(f"inference_iteration_{i}"):
                                     _ = self.model(dummy_input)
                                 prof.step()
                         logger.info("[Inference Profiling] Torch profiler run complete. Analyzing results...")
                         # (Analysis logic as before - calculating combined time, percentages, memory, top ops)
                         key_averages = prof.key_averages()
                         total_avg = key_averages.total_average()
                         results["profiler_total_events_averaged"] = len(key_averages)
                         cuda_time_total_us = getattr(total_avg, 'cuda_time_total', 0)
                         combined_time_us = total_avg.cpu_time_total + cuda_time_total_us
                         results["avg_cpu_time_total_ms"] = total_avg.cpu_time_total / 1000
                         results["avg_self_cpu_time_total_ms"] = total_avg.self_cpu_time_total / 1000
                         results["avg_cpu_time_percent"] = (total_avg.cpu_time_total / combined_time_us * 100) if combined_time_us > 0 else 0
                         if self.device.type == 'cuda' and cuda_time_total_us > 0:
                             results["avg_cuda_time_total_ms"] = cuda_time_total_us / 1000
                             results["avg_self_cuda_time_total_ms"] = getattr(total_avg, 'self_cuda_time_total', 0) / 1000
                             results["avg_gpu_time_percent"] = (cuda_time_total_us / combined_time_us * 100) if combined_time_us > 0 else 0
                         else: # Assign defaults if no CUDA time
                             results["avg_cuda_time_total_ms"] = 0
                             results["avg_self_cuda_time_total_ms"] = 0
                             results["avg_gpu_time_percent"] = 0
                         # Memory stats...
                         results["profiler_avg_cpu_memory_usage_b"] = getattr(total_avg, 'cpu_memory_usage', 0)
                         results["profiler_avg_self_cpu_memory_usage_b"] = getattr(total_avg, 'self_cpu_memory_usage', 0)
                         results["profiler_avg_cpu_memory_usage_formatted"] = format_bytes(results["profiler_avg_cpu_memory_usage_b"])
                         if self.device.type == 'cuda':
                            results["profiler_avg_gpu_memory_usage_b"] = getattr(total_avg, 'cuda_memory_usage', 0)
                            results["profiler_avg_self_gpu_memory_usage_b"] = getattr(total_avg, 'self_cuda_memory_usage', 0)
                            results["profiler_avg_gpu_memory_usage_formatted"] = format_bytes(results["profiler_avg_gpu_memory_usage_b"])
                         # Top ops table...
                         sort_by_key = profiler_sort_by if profiler_sort_by else "self_cpu_time_total"
                         try:
                            results["profiler_top_ops_summary"] = key_averages.table(sort_by=sort_by_key, row_limit=profiler_row_limit)
                            logger.info(f"[Inference Profiling] Top {profiler_row_limit} operators by {sort_by_key}:\n{results['profiler_top_ops_summary']}")
                         except KeyError as ke:
                             logger.warning(f"Could not sort profiler table by '{sort_by_key}' (KeyError: {ke}). Defaulting to 'self_cpu_time_total'.")
                             try: # Try default sort key
                                 results["profiler_top_ops_summary"] = key_averages.table(sort_by="self_cpu_time_total", row_limit=profiler_row_limit)
                                 logger.info(f"[Inference Profiling] Top {profiler_row_limit} operators by self_cpu_time_total:\n{results['profiler_top_ops_summary']}")
                             except Exception as table_err_fallback:
                                 logger.error(f"Could not generate profiler table with default sort key: {table_err_fallback}", exc_info=True)
                                 results["profiler_top_ops_summary"] = f"Error generating table: {table_err_fallback}"
                         except Exception as table_err:
                             logger.error(f"Could not generate profiler table sorted by '{sort_by_key}': {table_err}", exc_info=True)
                             results["profiler_top_ops_summary"] = f"Error generating table: {table_err}"


                     except Exception as prof_err:
                          logger.error(f"[Inference Profiling] Failed during torch.profiler execution or analysis: {prof_err}", exc_info=True)
                          results["profiler_error"] = f"Profiler run/analysis failed: {str(prof_err)}"

                 # Capture peak memory overall after the run
                 if self.device.type == 'cuda':
                     results["max_memory_allocated_b"] = torch.cuda.max_memory_allocated(self.device)
                     results["max_memory_allocated_mb"] = results["max_memory_allocated_b"] / (1024**2)
                     results["max_memory_allocated_formatted"] = format_bytes(results["max_memory_allocated_b"])
                     results["max_memory_reserved_b"] = torch.cuda.max_memory_reserved(self.device)
                     results["max_memory_reserved_formatted"] = format_bytes(results["max_memory_reserved_b"])
                 else:
                     # Best estimate for CPU peak from profiler if available
                     results["max_memory_allocated_b"] = results.get("profiler_avg_cpu_memory_usage_b")
                     if results["max_memory_allocated_b"] is not None:
                          results["max_memory_allocated_mb"] = results["max_memory_allocated_b"] / (1024**2)
                          results["max_memory_allocated_formatted"] = format_bytes(results["max_memory_allocated_b"]) + " (estimated peak based on profiler avg)"
                     else:
                          results["max_memory_allocated_mb"] = None
                          results["max_memory_allocated_formatted"] = "N/A (CPU Peak requires profiler or external tool)"


        except torch.cuda.OutOfMemoryError as oom_err:
            logger.error(f"[Inference Profiling] CUDA OOM: {oom_err}", exc_info=False)
            results["error"] = "CUDA OutOfMemoryError"
            # ... (OOM memory capture logic as before) ...
            if self.device.type == 'cuda':
                try:
                     results["max_memory_allocated_b"] = torch.cuda.max_memory_allocated(self.device)
                     results["max_memory_allocated_mb"] = results["max_memory_allocated_b"] / (1024**2)
                     results["max_memory_allocated_formatted"] = format_bytes(results["max_memory_allocated_b"])
                     results["memory_required_at_oom_approx_mb"] = results["max_memory_allocated_mb"]
                except Exception: pass # Ignore errors getting stats after OOM
                finally: torch.cuda.empty_cache()
        except Exception as e:
            logger.error(f"[Inference Profiling] Error: {e}", exc_info=True)
            results["error"] = f"General profiling error: {str(e)}"

        return results


    # --- NEW METHOD: profile_training_step ---
    def profile_training_step(self,
                              data_loader: Iterable, # Can be DataLoader or just an iterator yielding batches
                              criterion: nn.Module,
                              optimizer: Optimizer,
                              # Optional generator for targets if they can't be inferred
                              target_generator: Optional[Callable[[torch.Tensor], torch.Tensor]] = None,
                              iterations: int = 10, # Profile fewer steps for training
                              warmup: int = 3,
                              use_torch_profiler: bool = True,
                              profiler_activities: Optional[list] = None,
                              profiler_sort_by: str = "self_cpu_time_total",
                              profiler_row_limit: int = 15 # Show a few more ops for training
                             ) -> Dict[str, Any]:
        """Profiles a full training step (data loading, forward, loss, backward, optimizer step)."""

        validate_positive_integer(iterations, "Training profiling iterations", allow_zero=False)
        validate_positive_integer(warmup, "Training profiling warmup", allow_zero=True)

        logger.info(f"[Training Profiling] Starting: iterations={iterations}, warmup={warmup}, device={self.device}, use_torch_profiler={use_torch_profiler}")

        self.model.train() # Set model to training mode
        criterion.to(self.device) # Ensure criterion is on the correct device

        # Get an iterator from the data loader
        data_iter = iter(data_loader)

        results: Dict[str, Any] = {
            "profiling_type": "training_step",
            "device": str(self.device),
            "iterations": iterations,
            "warmup": warmup,
            "use_torch_profiler": use_torch_profiler,
            "optimizer_type": type(optimizer).__name__,
            "criterion_type": type(criterion).__name__,
        }

        if self.device.type == 'cuda':
            torch.cuda.reset_peak_memory_stats(self.device)
            torch.cuda.empty_cache()

        # Store times for basic analysis
        step_times_sec = []
        data_load_times_sec = []
        forward_times_sec = []
        loss_times_sec = []
        backward_times_sec = []
        optimizer_times_sec = []

        try:
            # --- Warmup Phase (Training Mode) ---
            logger.debug("[Training Profiling] Running warmup...")
            for _ in range(warmup):
                 try:
                     batch = next(data_iter)
                 except StopIteration:
                     logger.error("[Training Profiling] DataLoader exhausted during warmup.")
                     results["error"] = "DataLoader exhausted during warmup."
                     return results

                 # Basic training step without profiling timing
                 if isinstance(batch, (list, tuple)):
                      inputs = batch[0].to(self.device)
                      targets = batch[1].to(self.device) # Assume standard (input, target) structure
                 else:
                      inputs = batch.to(self.device)
                      # Need to generate or get targets
                      outputs_tmp = self.model(inputs) # Need output shape for target gen
                      targets = target_generator(outputs_tmp) if target_generator else self._generate_dummy_target(outputs_tmp, criterion)
                      targets = targets.to(self.device)


                 optimizer.zero_grad()
                 outputs = self.model(inputs)
                 loss = criterion(outputs, targets)
                 loss.backward()
                 optimizer.step()

            if self.device.type == 'cuda':
                torch.cuda.synchronize(self.device)
            logger.debug("[Training Profiling] Warmup complete.")

            # --- Timed/Profiled Iterations ---
            logger.debug(f"[Training Profiling] Running {iterations} profiled iterations...")

            # Configure profiler if used
            prof = None
            if use_torch_profiler:
                if profiler_activities is None:
                    profiler_activities = [ProfilerActivity.CPU]
                    if self.device.type == 'cuda':
                        profiler_activities.append(ProfilerActivity.CUDA)
                # For training step, profile fewer active steps
                profile_active = min(iterations, 5) # Profile just a few steps in detail
                profile_warmup = 1 # Minimal warmup within profiler
                wait = 0
                prof_schedule = schedule(wait=wait, warmup=profile_warmup, active=profile_active, repeat=1)
                num_profiler_steps = wait + profile_warmup + profile_active
                logger.info(f"[Training Profiling] Profiler schedule: wait={wait}, warmup={profile_warmup}, active={profile_active}")
                profiler_instance = profile(activities=profiler_activities, record_shapes=True, profile_memory=True, with_stack=False, schedule=prof_schedule)
                prof = profiler_instance.__enter__() # Manually enter context

            total_start_time = time.perf_counter()

            for i in range(iterations):
                iter_start_time = time.perf_counter()

                # --- Data Loading ---
                t0 = time.perf_counter()
                try:
                    with record_function("data_loading"): # Mark data loading
                         batch = next(data_iter)
                except StopIteration:
                    logger.error(f"[Training Profiling] DataLoader exhausted after {i} iterations.")
                    results["error"] = f"DataLoader exhausted after {i} valid iterations."
                    iterations = i # Record how many iterations actually ran
                    break # Stop profiling loop
                t1 = time.perf_counter()
                data_load_times_sec.append(t1 - t0)

                # --- Data Preparation & Move to Device ---
                # Handle common tuple/list format or single tensor
                try:
                    with record_function("data_prep_move"):
                        if isinstance(batch, (list, tuple)):
                            inputs = batch[0].to(self.device, non_blocking=True) # Use non_blocking?
                            # Generate or get targets
                            if len(batch) > 1:
                                targets_cpu = batch[1] # Keep target on CPU initially if generating? Depends.
                            else: # Only inputs provided
                                logger.warning("Batch has only one element, assuming it's input. Generating dummy target.")
                                outputs_tmp = self.model(inputs) # Forward pass needed to get shape
                                targets_cpu = target_generator(outputs_tmp) if target_generator else self._generate_dummy_target(outputs_tmp, criterion)

                            targets = targets_cpu.to(self.device, non_blocking=True)
                        else: # Assume batch is input tensor
                            inputs = batch.to(self.device, non_blocking=True)
                            # Generate targets after getting output shape
                            outputs_tmp = self.model(inputs) # Need output shape
                            targets_cpu = target_generator(outputs_tmp) if target_generator else self._generate_dummy_target(outputs_tmp, criterion)
                            targets = targets_cpu.to(self.device, non_blocking=True)
                except Exception as data_err:
                     logger.error(f"Error processing batch {i}: {data_err}", exc_info=True)
                     results["error"] = f"Error processing batch {i}: {data_err}"
                     iterations = i
                     break


                # --- Forward Pass ---
                t2 = time.perf_counter()
                with record_function("forward_pass"):
                    outputs = self.model(inputs)
                t3 = time.perf_counter()
                forward_times_sec.append(t3 - t2)

                # --- Loss Calculation ---
                with record_function("loss_calculation"):
                    loss = criterion(outputs, targets)
                t4 = time.perf_counter()
                loss_times_sec.append(t4 - t3)

                # --- Backward Pass ---
                optimizer.zero_grad() # Zero gradients before backward
                with record_function("backward_pass"):
                    loss.backward()
                t5 = time.perf_counter()
                backward_times_sec.append(t5 - t4)

                # --- Optimizer Step ---
                with record_function("optimizer_step"):
                    optimizer.step()
                t6 = time.perf_counter()
                optimizer_times_sec.append(t6 - t5)

                if self.device.type == 'cuda':
                    torch.cuda.synchronize(self.device)

                iter_end_time = time.perf_counter()
                step_times_sec.append(iter_end_time - iter_start_time)

                # Step the profiler if active
                if prof and i < num_profiler_steps:
                    prof.step()

            total_end_time = time.perf_counter()

            # Exit profiler context if used
            if prof:
                 profiler_instance.__exit__(None, None, None)
                 logger.info("[Training Profiling] Torch profiler run complete. Analyzing results...")
                 # (Analysis logic - similar to inference, but now contains backward/optimizer ops)
                 try:
                      key_averages = prof.key_averages()
                      total_avg = key_averages.total_average()
                      results["profiler_total_events_averaged"] = len(key_averages)
                      cuda_time_total_us = getattr(total_avg, 'cuda_time_total', 0)
                      combined_time_us = total_avg.cpu_time_total + cuda_time_total_us
                      results["profiler_avg_cpu_time_total_ms"] = total_avg.cpu_time_total / 1000
                      results["profiler_avg_self_cpu_time_total_ms"] = total_avg.self_cpu_time_total / 1000
                      results["profiler_avg_cpu_time_percent"] = (total_avg.cpu_time_total / combined_time_us * 100) if combined_time_us > 0 else 0
                      if self.device.type == 'cuda' and cuda_time_total_us > 0:
                          results["profiler_avg_cuda_time_total_ms"] = cuda_time_total_us / 1000
                          results["profiler_avg_self_cuda_time_total_ms"] = getattr(total_avg, 'self_cuda_time_total', 0) / 1000
                          results["profiler_avg_gpu_time_percent"] = (cuda_time_total_us / combined_time_us * 100) if combined_time_us > 0 else 0
                      else:
                          results["profiler_avg_cuda_time_total_ms"] = 0
                          results["profiler_avg_self_cuda_time_total_ms"] = 0
                          results["profiler_avg_gpu_time_percent"] = 0
                      # Memory stats...
                      results["profiler_avg_cpu_memory_usage_b"] = getattr(total_avg, 'cpu_memory_usage', 0)
                      results["profiler_avg_gpu_memory_usage_b"] = getattr(total_avg, 'cuda_memory_usage', 0) if self.device.type == 'cuda' else 0
                      results["profiler_avg_cpu_memory_usage_formatted"] = format_bytes(results["profiler_avg_cpu_memory_usage_b"])
                      results["profiler_avg_gpu_memory_usage_formatted"] = format_bytes(results["profiler_avg_gpu_memory_usage_b"]) if self.device.type == 'cuda' else "N/A"
                      # Top ops table...
                      sort_by_key = profiler_sort_by if profiler_sort_by else "self_cpu_time_total"
                      try:
                         results["profiler_top_ops_summary"] = key_averages.table(sort_by=sort_by_key, row_limit=profiler_row_limit)
                         logger.info(f"[Training Profiling] Top {profiler_row_limit} operators by {sort_by_key}:\n{results['profiler_top_ops_summary']}")
                      except KeyError as ke:
                          logger.warning(f"Could not sort profiler table by '{sort_by_key}' (KeyError: {ke}). Defaulting to 'self_cpu_time_total'.")
                          try: # Try default sort key
                              results["profiler_top_ops_summary"] = key_averages.table(sort_by="self_cpu_time_total", row_limit=profiler_row_limit)
                              logger.info(f"[Training Profiling] Top {profiler_row_limit} operators by self_cpu_time_total:\n{results['profiler_top_ops_summary']}")
                          except Exception as table_err_fallback:
                              logger.error(f"Could not generate profiler table with default sort key: {table_err_fallback}", exc_info=True)
                              results["profiler_top_ops_summary"] = f"Error generating table: {table_err_fallback}"
                      except Exception as table_err:
                          logger.error(f"Could not generate profiler table sorted by '{sort_by_key}': {table_err}", exc_info=True)
                          results["profiler_top_ops_summary"] = f"Error generating table: {table_err}"

                 except Exception as prof_err:
                      logger.error(f"[Training Profiling] Failed during torch.profiler analysis: {prof_err}", exc_info=True)
                      results["profiler_error"] = f"Profiler analysis failed: {str(prof_err)}"


            # --- Basic Timing Analysis ---
            if iterations > 0: # Ensure we ran at least one iteration
                results["total_profiled_duration_sec"] = total_end_time - total_start_time
                results["avg_step_time_ms"] = (sum(step_times_sec) / iterations) * 1000 if step_times_sec else 0
                results["avg_data_load_time_ms"] = (sum(data_load_times_sec) / iterations) * 1000 if data_load_times_sec else 0
                results["avg_forward_time_ms"] = (sum(forward_times_sec) / iterations) * 1000 if forward_times_sec else 0
                results["avg_loss_time_ms"] = (sum(loss_times_sec) / iterations) * 1000 if loss_times_sec else 0
                results["avg_backward_time_ms"] = (sum(backward_times_sec) / iterations) * 1000 if backward_times_sec else 0
                results["avg_optimizer_time_ms"] = (sum(optimizer_times_sec) / iterations) * 1000 if optimizer_times_sec else 0

                # Calculate percentages based on average step time
                if results["avg_step_time_ms"] > 0:
                    results["percent_time_data_loading"] = (results["avg_data_load_time_ms"] / results["avg_step_time_ms"]) * 100
                    results["percent_time_forward"] = (results["avg_forward_time_ms"] / results["avg_step_time_ms"]) * 100
                    results["percent_time_loss"] = (results["avg_loss_time_ms"] / results["avg_step_time_ms"]) * 100
                    results["percent_time_backward"] = (results["avg_backward_time_ms"] / results["avg_step_time_ms"]) * 100
                    results["percent_time_optimizer"] = (results["avg_optimizer_time_ms"] / results["avg_step_time_ms"]) * 100
                else:
                    results["percent_time_data_loading"] = 0
                    results["percent_time_forward"] = 0
                    results["percent_time_loss"] = 0
                    results["percent_time_backward"] = 0
                    results["percent_time_optimizer"] = 0


                logger.info(f"[Training Profiling] Basic timing breakdown (avg ms): "
                            f"Step={results['avg_step_time_ms']:.2f}, "
                            f"DataLoad={results['avg_data_load_time_ms']:.2f} ({results['percent_time_data_loading']:.1f}%), "
                            f"Forward={results['avg_forward_time_ms']:.2f} ({results['percent_time_forward']:.1f}%), "
                            f"Loss={results['avg_loss_time_ms']:.2f} ({results['percent_time_loss']:.1f}%), "
                            f"Backward={results['avg_backward_time_ms']:.2f} ({results['percent_time_backward']:.1f}%), "
                            f"Optimizer={results['avg_optimizer_time_ms']:.2f} ({results['percent_time_optimizer']:.1f}%)")

            # Capture overall peak memory after the run
            if self.device.type == 'cuda':
                results["max_memory_allocated_b"] = torch.cuda.max_memory_allocated(self.device)
                results["max_memory_allocated_mb"] = results["max_memory_allocated_b"] / (1024**2)
                results["max_memory_allocated_formatted"] = format_bytes(results["max_memory_allocated_b"])
                results["max_memory_reserved_b"] = torch.cuda.max_memory_reserved(self.device)
                results["max_memory_reserved_formatted"] = format_bytes(results["max_memory_reserved_b"])
            else:
                # Estimate CPU peak from profiler if available
                results["max_memory_allocated_b"] = results.get("profiler_avg_cpu_memory_usage_b")
                if results["max_memory_allocated_b"] is not None:
                    results["max_memory_allocated_mb"] = results["max_memory_allocated_b"] / (1024**2)
                    results["max_memory_allocated_formatted"] = format_bytes(results["max_memory_allocated_b"]) + " (estimated peak based on profiler avg)"
                else:
                    results["max_memory_allocated_mb"] = None
                    results["max_memory_allocated_formatted"] = "N/A (CPU Peak requires profiler or external tool)"


        except torch.cuda.OutOfMemoryError as oom_err:
            logger.error(f"[Training Profiling] CUDA OOM: {oom_err}", exc_info=False)
            results["error"] = "CUDA OutOfMemoryError"
            results["error_details"] = str(oom_err)
            # ... (OOM memory capture logic) ...
            if self.device.type == 'cuda':
                try:
                     results["max_memory_allocated_b"] = torch.cuda.max_memory_allocated(self.device)
                     results["max_memory_allocated_mb"] = results["max_memory_allocated_b"] / (1024**2)
                     results["max_memory_allocated_formatted"] = format_bytes(results["max_memory_allocated_b"])
                     results["memory_required_at_oom_approx_mb"] = results["max_memory_allocated_mb"]
                except Exception: pass
                finally: torch.cuda.empty_cache()
        except Exception as e:
            logger.error(f"[Training Profiling] Error: {e}", exc_info=True)
            results["error"] = f"General training profiling error: {str(e)}"
        finally:
            # Ensure model is returned to eval mode if that's the default expectation
            self.model.eval()

        return results