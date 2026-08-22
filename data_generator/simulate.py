import json
import math
import os
import random
import time
from datetime import datetime

# Directory where incoming telemetry files land
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "incoming")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_telemetry(step: int, prev_fluid_temp: float) -> tuple[dict, float]:
    """Generates realistic datacenter server telemetry with baseline sine patterns,

    random noise, and thermal inertia physics.
    """
    # 1. Base sinusoidal workload (simulating diurnal or batch cycle)
    base_load = 45.0 + 25.0 * math.sin(step * 0.1)

    # 2. Add random noise
    cpu_util = base_load + random.uniform(-5.0, 5.0)
    gpu_util = (base_load * 1.1) + random.uniform(-8.0, 8.0)

    # 3. Simulate intermittent high-load spikes (10% chance)
    if random.random() < 0.10:
        cpu_util += random.uniform(20.0, 30.0)
        gpu_util += random.uniform(25.0, 40.0)

    # Clamp percentages between 0 and 100
    cpu_util = round(max(5.0, min(100.0, cpu_util)), 2)
    gpu_util = round(max(5.0, min(100.0, gpu_util)), 2)

    # 4. Approximate power draw in Watts
    # Idle power ~100W + dynamic load up to ~450W
    power_draw_watts = round(
        100.0 + (cpu_util * 1.5) + (gpu_util * 2.0) + random.uniform(-5, 5), 2
    )

    # 5. Thermal physics: Fluid temperature lags behind power draw
    # Target equilibrium temp proportional to power draw
    target_temp = 30.0 + (power_draw_watts / 450.0) * 45.0
    # Thermal inertia (0.05 step change per tick)
    current_fluid_temp = round(
        prev_fluid_temp + 0.05 * (target_temp - prev_fluid_temp)
        + random.uniform(-0.1, 0.1),
        2,
    )

    record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "cpu_utilization": cpu_util,
        "gpu_utilization": gpu_util,
        "power_draw_watts": power_draw_watts,
        "current_fluid_temp": current_fluid_temp,
    }

    return record, current_fluid_temp


def run_stream(interval_seconds: float = 2.0):
    print(f"🚀 Telemetry stream started. Writing to: {OUTPUT_DIR}")
    step = 0
    fluid_temp = 35.0  # Starting ambient fluid temp in Celsius

    try:
        while True:
            record, fluid_temp = generate_telemetry(step, fluid_temp)

            # Unique filename per message based on timestamp
            file_id = int(time.time() * 1000)
            file_path = os.path.join(OUTPUT_DIR, f"telemetry_{file_id}.json")

            with open(file_path, "w") as f:
                json.dump(record, f)

            print(
                f"[{record['timestamp']}] CPU: {record['cpu_utilization']}% | GPU: {record['gpu_utilization']}% | Power: {record['power_draw_watts']}W | Temp: {record['current_fluid_temp']}°C"
            )

            step += 1
            time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\n🛑 Telemetry generation stopped.")


if __name__ == "__main__":
    run_stream(interval_seconds=2.0)