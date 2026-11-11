# Home Microgrid / Net-Metering Simulator

## 1. Project Overview

The Home Microgrid / Net-Metering Simulator is a Python-based application developed to analyse whether installing rooftop solar panels with net metering can be financially beneficial for a household.

The system uses household electricity consumption and estimated solar generation data over a 14-day period to simulate grid electricity imports, exports, electricity billing, savings and solar installation payback period.

The application provides an interactive dashboard with financial calculations and graphical representations of energy usage.

## 2. Objectives

- Analyse daily household electricity consumption.
- Estimate rooftop solar energy generation.
- Calculate electricity imported from and exported to the grid.
- Simulate simplified net-metering billing.
- Estimate electricity bill savings.
- Calculate the simple payback period of a solar installation.
- Understand the environmental benefits of rooftop solar energy.

## 3. Technologies Used

| Technology | Purpose               |
| ---------- | --------------------- |
| Python     | Core programming      |
| Pandas     | Dataset processing    |
| Streamlit  | Interactive dashboard |
| Matplotlib | Data visualisation    |
| CSV        | Dataset storage       |

## 4. Project Structure

```text
home-microgrid-simulator/
│
├── data/
│   ├── raw_dataset.csv
│   └── cleaned_dataset.csv
│
├── outputs/
│
├── clean_data.py
├── simulator.py
├── test_simulator.py
├── app.py
└── README.md
```

## 5. Dataset Description

The project uses an illustrative 14-day dataset containing:

- Date
- Household electricity consumption (kWh)
- Solar energy generation (kWh)
- Weather condition

The raw dataset contains intentionally introduced data-quality issues, including a missing consumption value and an invalid negative solar-generation value.

The cleaning program uses median imputation to handle these issues and generates a cleaned dataset.

**Note:** The dataset contains synthetic sample observations and does not represent actual household meter readings.

## 6. Methodology

### Step 1: Data Collection

A sample dataset containing 14 days of household electricity consumption and solar generation potential is prepared.

### Step 2: Data Cleaning

Missing and invalid observations are identified and corrected using Python and Pandas.

### Step 3: Energy Calculation

The simulator calculates:

**Solar Self-Consumption**

Self-consumption = Minimum of household consumption and solar generation.

**Grid Import**

Grid Import = Maximum of (Consumption - Generation, 0).

**Grid Export**

Grid Export = Maximum of (Generation - Consumption, 0).

### Step 4: Net-Metering Billing

The simulator calculates total grid imports and exports over the sample billing period.

Net Units = Total Grid Import - Total Grid Export.

Positive net units are charged at the grid import tariff. If exports exceed imports, the remaining surplus receives export credit.

### Step 5: Financial Analysis

The application calculates:

- Electricity bill without solar.
- Electricity bill with solar.
- Export credit.
- Estimated savings.
- Annual savings.
- Solar installation payback period.

**Annual Savings**

Annual Savings = Sample Period Savings × (365 / Number of Sample Days).

**Payback Period**

Payback Period = Solar Installation Cost / Estimated Annual Savings.

### Step 6: Visualisation

The Streamlit dashboard displays energy consumption, solar generation, grid imports, exports, financial results and daily simulation data.

## 7. Sample Simulation Results

The following results are obtained using the default simulation assumptions:

| Parameter                 |      Value |
| ------------------------- | ---------: |
| Household Consumption     | 186.60 kWh |
| Solar Generation          | 210.70 kWh |
| Grid Import               |   6.50 kWh |
| Grid Export               |  30.60 kWh |
| Solar Self-Consumption    | 180.10 kWh |
| Original Electricity Bill |  ₹1,492.80 |
| Solar Electricity Bill    |      ₹0.00 |
| Export Credit             |     ₹72.30 |
| 14-Day Savings            |  ₹1,492.80 |
| Estimated Annual Savings  | ₹38,919.43 |
| Installation Cost         |  ₹1,80,000 |
| Estimated Payback Period  | 4.62 years |

These are illustrative outputs under the default assumptions.

## 8. How to Run the Project

### Prerequisites

- Python 3.10 or above
- pip package manager

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the project directory

```bash
cd home-microgrid-simulator
```

### Step 3: Install dependencies

```bash
python -m pip install pandas streamlit matplotlib
```

### Step 4: Generate the cleaned dataset

```bash
python clean_data.py
```

### Step 5: Test the simulation engine

```bash
python test_simulator.py
```

### Step 6: Launch the application

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

http://localhost:8501

## 9. Dashboard Features

- Energy consumption and solar generation overview.
- Grid electricity import and export analysis.
- Electricity bill comparison.
- Solar installation investment analysis.
- Estimated annual savings and payback period.
- Daily energy simulation results table.
- Downloadable simulation results in CSV format.
- Configurable electricity tariffs and installation costs.

## 10. Limitations

- The project uses illustrative synthetic data rather than actual household measurements.
- Only 14 days of observations are available.
- Annual savings are estimated by extrapolating the 14-day results, assuming the sample is representative of the year.
- Actual electricity consumption and solar generation vary seasonally.
- The billing model uses simplified net-metering assumptions.
- Actual electricity tariffs, fixed charges, export compensation and net-metering policies vary by electricity distribution company.
- Maintenance, financing, solar panel degradation and inverter replacement costs are not included in the payback calculation.

## 11. Conclusion

The Home Microgrid / Net-Metering Simulator demonstrates how rooftop solar energy generation and net metering can influence household electricity bills.

By analysing energy consumption, solar generation, grid interaction and financial savings, the application provides an educational framework for understanding the potential economic benefits of residential solar installations.

The simulator can be extended in the future using real-time smart meter readings, location-specific solar generation estimates and actual electricity tariff structures.

---

**Project:** Home Microgrid / Net-Metering Simulator

**Course:** Sustainable Energy Engineering
