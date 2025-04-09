// Copyright (C) 2023-2024 National Center for Atmospheric Research, University of Illinois at Urbana-Champaign
//
// SPDX-License-Identifier: Apache-2.0

#pragma once

#include <string>
#include <vector>

namespace mechanism_configuration
{
  namespace v1
  {
    namespace validation
    {
      const struct Keys
      {
        // Shared, but also Mechanism
        const std::string version = "version";
        const std::string name = "name";

        // Configuration
        const std::string species = "species";
        const std::string phases = "phases";
        const std::string reactions = "reactions";

        // Species
        const std::string absolute_tolerance = "absolute tolerance";
        const std::string diffusion_coefficient = "diffusion coefficient [m2 s-1]";
        const std::string molecular_weight = "molecular weight [kg mol-1]";
        const std::string henrys_law_constant_298 = "HLC(298K) [mol m-3 Pa-1]";
        const std::string henrys_law_constant_exponential_factor = "HLC exponential factor [K]";
        const std::string phase = "phase";
        const std::string n_star = "N star";
        const std::string density = "density [kg m-3]";
        const std::string tracer_type = "tracer type";
        const std::string third_body = "THIRD_BODY";

        // Reactions
        const std::string reactants = "reactants";
        const std::string products = "products";
        const std::string type = "type";
        const std::string gas_phase = "gas phase";

        // Reactant and product
        const std::string species_name = "species name";
        const std::string coefficient = "coefficient";

        // Arrhenius
        const std::string Arrhenius_key = "ARRHENIUS";
        const std::string A = "A";
        const std::string B = "B";
        const std::string C = "C";
        const std::string D = "D";
        const std::string E = "E";
        const std::string Ea = "Ea";

        // Condensed Phase Arrhenius
        const std::string CondensedPhaseArrhenius_key = "CONDENSED_PHASE_ARRHENIUS";
        const std::string aerosol_phase_water = "aerosol-phase water";
        // also these
        // aerosol phase
        // A
        // B
        // C
        // D
        // E
        // Ea

        // Troe
        const std::string Troe_key = "TROE";
        const std::string k0_A = "k0_A";
        const std::string k0_B = "k0_B";
        const std::string k0_C = "k0_C";
        const std::string kinf_A = "kinf_A";
        const std::string kinf_B = "kinf_B";
        const std::string kinf_C = "kinf_C";
        const std::string Fc = "Fc";
        const std::string N = "N";

        // Branched
        const std::string Branched_key = "BRANCHED_NO_RO2";
        const std::string X = "X";
        const std::string Y = "Y";
        const std::string a0 = "a0";
        const std::string n = "n";
        const std::string nitrate_products = "nitrate products";
        const std::string alkoxy_products = "alkoxy products";

        // Tunneling
        const std::string Tunneling_key = "TUNNELING";
        // also these, but they are defined above
        // A
        // B
        // C

        // Surface
        const std::string Surface_key = "SURFACE";
        const std::string reaction_probability = "reaction probability";
        const std::string gas_phase_species = "gas-phase species";
        const std::string gas_phase_products = "gas-phase products";
        const std::string aerosol_phase = "aerosol phase";

        // Photolysis
        const std::string Photolysis_key = "PHOTOLYSIS";
        const std::string scaling_factor = "scaling factor";

        // Condensed Phae Photolysis
        const std::string CondensedPhasePhotolysis_key = "CONDENSED_PHASE_PHOTOLYSIS";
        // also
        // scaling factor
        // aerosol phase
        // aerosol-phase water

        // Emissions
        const std::string Emission_key = "EMISSION";
        // also scaling factor

        // First Order Loss
        const std::string FirstOrderLoss_key = "FIRST_ORDER_LOSS";
        // also scaling factor

        // Simpol Phase Transfer
        const std::string SimpolPhaseTransfer_key = "SIMPOL_PHASE_TRANSFER";
        const std::string aerosol_phase_species = "aerosol-phase species";
        // also
        // gas phase
        // gas-phase species
        // aerosol phase
        // aserosol-phase species
        // B

        // Aqueous Equilibrium
        const std::string AqueousPhaseEquilibrium_key = "AQUEOUS_EQUILIBRIUM";
        // also
        // aerosol phase
        // aerosol-phase water
        // A
        // C
        const std::string k_reverse = "k_reverse";

        // Wet Deposition
        const std::string WetDeposition_key = "WET_DEPOSITION";
        // also
        // scaling factor
        // aerosol phase

        // Henry's Law Phase Transfer
        const std::string HenrysLaw_key = "HL_PHASE_TRANSFER";
        // also
        // gas phase
        // aerosol phase
        // aerosol-phase water
        // aerosol-phase species
      } keys;
    }  // namespace validation
  }  // namespace v1
}  // namespace mechanism_configuration