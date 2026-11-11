
import pandas as pd


def simulate_net_metering(
    data,
    import_tariff=8,
    export_tariff=3,
    installation_cost=180000
):

    # 1. Calculate solar self-consumption
    data["self_consumption_kwh"] = data.apply(
        lambda row: min(
            row["household_consumption_kwh"],
            row["solar_generation_kwh"]
        ),
        axis=1
    )

    # 2. Calculate grid import
    data["grid_import_kwh"] = (
        data["household_consumption_kwh"]
        - data["solar_generation_kwh"]
    ).clip(lower=0)

    # 3. Calculate grid export
    data["grid_export_kwh"] = (
        data["solar_generation_kwh"]
        - data["household_consumption_kwh"]
    ).clip(lower=0)

    # 4. Calculate total energy values
    total_consumption = data["household_consumption_kwh"].sum()
    total_generation = data["solar_generation_kwh"].sum()

    total_import = data["grid_import_kwh"].sum()
    total_export = data["grid_export_kwh"].sum()

    total_self_consumption = data["self_consumption_kwh"].sum()

    # 5. Calculate net-metering units
    net_units = total_import - total_export

    # 6. Calculate electricity bill without solar
    original_bill = total_consumption * import_tariff

    # 7. Calculate electricity bill with solar
    if net_units >= 0:
        solar_bill = net_units * import_tariff
        export_credit = 0
    else:
        solar_bill = 0
        export_credit = abs(net_units) * export_tariff

    # 8. Calculate savings
    savings = original_bill - solar_bill

    # 9. Estimate annual savings
    annual_savings = savings * (365 / len(data))

    # 10. Calculate payback period
    if annual_savings > 0:
        payback_period = installation_cost / annual_savings
    else:
        payback_period = None

    # 11. Store all results
    results = {
        "Total Consumption (kWh)": total_consumption,
        "Total Solar Generation (kWh)": total_generation,
        "Grid Import (kWh)": total_import,
        "Grid Export (kWh)": total_export,
        "Solar Self-Consumption (kWh)": total_self_consumption,
        "Original Electricity Bill (Rs)": original_bill,
        "Solar Electricity Bill (Rs)": solar_bill,
        "Export Credit (Rs)": export_credit,
        "Savings (Rs)": savings,
        "Estimated Annual Savings (Rs)": annual_savings,
        "Installation Cost (Rs)": installation_cost,
        "Payback Period (Years)": payback_period
    }

    return results
