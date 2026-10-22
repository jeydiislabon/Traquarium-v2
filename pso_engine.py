"""
pso_engine.py
-------------
Particle Swarm Optimization (PSO) engine for multi-tank water change scheduling.

Based on the algorithm by:
    Kennedy, J., & Eberhart, R. (1995).
    Particle swarm optimization.
    Proceedings of ICNN'95 - International Conference on Neural Networks.

Objective:
    Minimize total water changed (litres) across all tanks while bringing
    every tank's projected post-change NH3 below the Safe threshold
    (0.02 mg/L).

Dilution model (single partial water change):
    NH3_after = NH3_before * (1 - c)
    where c ∈ [0, 1] is the fractional volume of water replaced.

PSO hyperparameters (from paper Section 2.1.2):
    Swarm size  : 30 particles
    Max iterations: 200
    Inertia weight (w)          : 0.7
    Cognitive coefficient (c1)  : 1.5
    Social coefficient    (c2)  : 1.5
    Penalty for unsafe tanks    : 1000 * excess_NH3
"""

import random
import time
from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
NH3_SAFE_THRESHOLD = 0.02   # mg/L — Safe level (Emerson et al., 1975)

# PSO hyperparameters
SWARM_SIZE     = 30
MAX_ITERATIONS = 200
W              = 0.7    # inertia weight
C1             = 1.5    # cognitive coefficient
C2             = 1.5    # social coefficient
PENALTY        = 1000.0 # penalty per mg/L of NH3 above threshold


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class TankReading:
    """Represents a single tank's current state for PSO input."""
    tank_name: str
    nh3: float          # current un-ionized NH3 in mg/L
    volume_litres: float  # tank volume in litres


@dataclass
class WaterChangeSchedule:
    """PSO output: recommended water change for each tank."""
    tank_name: str
    change_fraction: float   # fraction of tank volume to replace (0-1)
    change_litres: float     # absolute volume to change in litres
    nh3_before: float        # NH3 before change (mg/L)
    nh3_after: float         # projected NH3 after change (mg/L)
    is_safe_after: bool      # whether NH3 will be below threshold after change


@dataclass
class PSOResult:
    """Full result returned by PSOEngine.optimize()."""
    schedules: List[WaterChangeSchedule]
    total_change_litres: float
    iterations_run: int
    inference_ms: float
    converged: bool


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

class PSOEngine:
    """
    Stateless PSO engine. Call PSOEngine.optimize(tanks) directly.
    """

    @staticmethod
    def _fitness(positions: list, tanks: List[TankReading]) -> float:
        """
        Fitness function.
        Minimises total water changed (L) subject to a hard penalty for any
        tank still at or above NH3_SAFE_THRESHOLD after the change.

        Penalty is scaled relative to total tank volume so it always
        dominates the water-saving objective when a tank remains unsafe.

        Args:
            positions: List of change fractions, one per tank (0-1).
            tanks:     List of TankReading objects.

        Returns:
            Scalar fitness value (lower is better).
        """
        total_litres  = 0.0
        total_volume  = sum(t.volume_litres for t in tanks)
        penalty       = 0.0

        for c, tank in zip(positions, tanks):
            c          = max(0.0, min(1.0, c))
            nh3_after  = tank.nh3 * (1.0 - c)
            total_litres += c * tank.volume_litres

            if nh3_after >= NH3_SAFE_THRESHOLD:
                # Penalty >> any possible water saving
                excess   = nh3_after - NH3_SAFE_THRESHOLD
                penalty += PENALTY * total_volume * excess

        return total_litres + penalty

    @staticmethod
    def optimize(tanks: List[TankReading],
                 swarm_size: int = SWARM_SIZE,
                 max_iter: int = MAX_ITERATIONS) -> PSOResult:
        """
        Run PSO to find the minimal water change schedule that brings
        all tanks below NH3_SAFE_THRESHOLD.

        Args:
            tanks:      List of TankReading objects (one per tank).
            swarm_size: Number of particles in the swarm.
            max_iter:   Maximum number of iterations.

        Returns:
            PSOResult with the optimal schedule and performance metrics.
        """
        if not tanks:
            return PSOResult(
                schedules=[],
                total_change_litres=0.0,
                iterations_run=0,
                inference_ms=0.0,
                converged=True,
            )

        n_tanks = len(tanks)
        t_start = time.perf_counter()

        # ---- Initialise swarm ----------------------------------------
        # Each particle is a list of n_tanks change fractions in [0, 1]
        positions  = [[random.uniform(0.0, 1.0) for _ in range(n_tanks)]
                      for _ in range(swarm_size)]
        velocities = [[random.uniform(-0.5, 0.5) for _ in range(n_tanks)]
                      for _ in range(swarm_size)]

        # For tanks that are already safe, initialise near 0
        for i in range(swarm_size):
            for j, tank in enumerate(tanks):
                if tank.nh3 < NH3_SAFE_THRESHOLD:
                    positions[i][j]  = random.uniform(0.0, 0.05)
                    velocities[i][j] = random.uniform(-0.02, 0.02)

        p_best_pos = [pos[:] for pos in positions]
        p_best_fit = [PSOEngine._fitness(pos, tanks) for pos in positions]

        g_best_idx = p_best_fit.index(min(p_best_fit))
        g_best_pos = p_best_pos[g_best_idx][:]
        g_best_fit = p_best_fit[g_best_idx]

        # ---- Main loop -----------------------------------------------
        prev_best   = g_best_fit
        stagnation  = 0
        iterations_run = 0

        for iteration in range(max_iter):
            iterations_run = iteration + 1

            for i in range(swarm_size):
                for d in range(n_tanks):
                    r1 = random.random()
                    r2 = random.random()

                    # Velocity update
                    velocities[i][d] = (
                        W  * velocities[i][d]
                        + C1 * r1 * (p_best_pos[i][d] - positions[i][d])
                        + C2 * r2 * (g_best_pos[d]    - positions[i][d])
                    )

                    # Clamp velocity to [-1, 1]
                    velocities[i][d] = max(-1.0, min(1.0, velocities[i][d]))

                    # Position update
                    positions[i][d] += velocities[i][d]
                    positions[i][d]  = max(0.0, min(1.0, positions[i][d]))

                # Evaluate fitness
                fit = PSOEngine._fitness(positions[i], tanks)

                # Update personal best
                if fit < p_best_fit[i]:
                    p_best_fit[i] = fit
                    p_best_pos[i] = positions[i][:]

                # Update global best
                if fit < g_best_fit:
                    g_best_fit = fit
                    g_best_pos = positions[i][:]

            # Early stopping if converged (stagnation for 20 iterations)
            if abs(prev_best - g_best_fit) < 1e-9:
                stagnation += 1
            else:
                stagnation = 0
            prev_best = g_best_fit

            if stagnation >= 20:
                break

        t_end = time.perf_counter()
        inference_ms = (t_end - t_start) * 1000.0

        # ---- Build result schedules ----------------------------------
        schedules = []
        total_litres = 0.0

        for j, tank in enumerate(tanks):
            c          = max(0.0, min(1.0, g_best_pos[j]))
            nh3_after  = tank.nh3 * (1.0 - c)
            litres     = c * tank.volume_litres
            total_litres += litres

            schedules.append(WaterChangeSchedule(
                tank_name      = tank.tank_name,
                change_fraction= round(c, 4),
                change_litres  = round(litres, 2),
                nh3_before     = round(tank.nh3, 6),
                nh3_after      = round(nh3_after, 6),
                is_safe_after  = nh3_after < NH3_SAFE_THRESHOLD,
            ))

        # A result is converged if all tanks are projected to be safe
        converged = all(s.is_safe_after for s in schedules)

        return PSOResult(
            schedules          = schedules,
            total_change_litres= round(total_litres, 2),
            iterations_run     = iterations_run,
            inference_ms       = round(inference_ms, 3),
            converged          = converged,
        )
