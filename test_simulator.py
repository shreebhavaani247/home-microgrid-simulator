
import pandas as pd
from simulator import simulate_net_metering

# Load cleaned dataset
data = pd.read_csv("data/cleaned_dataset.csv")

# Run simulation
results = simulate_net_metering(
    data,
    import_tariff=8,
    export_tariff=3,
    installation_cost=180000
)

# Display simulation results
print("\nHOME MICROGRID SIMULATION RESULTS")
print("----------------------------------")

for key, value in results.items():

    if value is None:
        print(f"{key}: Not achieved")
    elif isinstance(value, (int, float)):
        print(f"{key}: {value:.2f}")
    else:
        print(f"{key}: {value}")

