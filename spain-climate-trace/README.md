# Spain Climate TRACE

This project downloads the Climate TRACE v4.6.0 country package for Spain and combines the included `country_emissions` files into a single long CSV.

## Dataset
- **Name:** Climate TRACE Country Package (Spain)
- **URL:** https://downloads.climatetrace.org/v4.6.0/country_packages/co2e_100yr/ESP.zip
- **Description:** Annual CO₂ equivalent (100‑year GWPs) emissions estimates for Spain across sectors and subsectors. The package contains 68 `*_country_emissions_v4_6_0.csv` files.

### Sectors and subsectors
- **agriculture**: crop-residues, cropland-fires, enteric-fermentation-cattle-operation, enteric-fermentation-cattle-pasture, enteric-fermentation-other, manure-applied-to-soils, manure-left-on-pasture-cattle, manure-management-cattle-operation, manure-management-other, other-agricultural-soil-emissions, rice-cultivation, synthetic-fertilizer-application
- **buildings**: non-residential-onsite-fuel-usage, other-onsite-fuel-usage, residential-onsite-fuel-usage
- **fluorinated gases**: fluorinated-gases
- **forestry and land use**: forest-land-clearing, forest-land-degradation, forest-land-fires, net-forest-land, net-shrubgrass, net-wetland, removals, shrubgrass-fires, water-reservoirs, wetland-fires
- **fossil fuel operations**: coal-mining, oil-and-gas-production, oil-and-gas-refining, oil-and-gas-transport, other-fossil-fuel-operations, other-solid-fuels
- **manufacturing**: aluminum, cement, chemicals, food-beverage-tobacco, glass, iron-and-steel, lime, other-chemicals, other-manufacturing, other-metals, petrochemical-steam-cracking, pulp-and-paper, textiles-leather-apparel, wood-and-wood-products
- **mineral extraction**: bauxite-mining, copper-mining, iron-mining, other-mining-quarrying, rock-quarrying, sand-quarrying
- **power**: electricity-generation, heat-plants, other-energy-use
- **transportation**: domestic-aviation, domestic-shipping, international-aviation, international-shipping, non-broadcasting-vessels, other-transport, railways, road-transportation
- **waste**: biological-treatment-of-solid-waste-and-biogenic, domestic-wastewater-treatment-and-discharge, incineration-and-open-burning-of-waste, industrial-wastewater-treatment-and-discharge, solid-waste-disposal

### Sample combined rows
```
iso3_country      sector      subsector          start_time            end_time        gas  emissions_quantity
ESP              agriculture  cropland-fires    2015-01-01 00:00:00 2015-12-31 00:00:00 co2e_100yr       189850.720326
ESP              agriculture  cropland-fires    2016-01-01 00:00:00 2016-12-31 00:00:00 co2e_100yr       189114.402035
ESP              agriculture  cropland-fires    2017-01-01 00:00:00 2017-12-31 00:00:00 co2e_100yr       113803.802150
ESP              agriculture  cropland-fires    2018-01-01 00:00:00 2018-12-31 00:00:00 co2e_100yr       129481.039371
ESP              agriculture  cropland-fires    2019-01-01 00:00:00 2019-12-31 00:00:00 co2e_100yr        78810.285269
```

## Usage
```
make -C spain-climate-trace data
```
The command downloads the Spain package and writes `esp_emissions_long.csv` in the project directory.
