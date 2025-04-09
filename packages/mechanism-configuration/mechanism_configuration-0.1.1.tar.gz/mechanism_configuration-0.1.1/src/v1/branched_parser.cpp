#include <mechanism_configuration/constants.hpp>
#include <mechanism_configuration/v1/parser.hpp>
#include <mechanism_configuration/v1/parser_types.hpp>
#include <mechanism_configuration/v1/utils.hpp>
#include <mechanism_configuration/validate_schema.hpp>

namespace mechanism_configuration
{
  namespace v1
  {
    Errors BranchedParser::parse(
        const YAML::Node& object,
        const std::vector<types::Species>& existing_species,
        const std::vector<types::Phase>& existing_phases,
        types::Reactions& reactions)
    {
      Errors errors;
      types::Branched branched;

      auto required_keys = { validation::keys.nitrate_products,
                             validation::keys.alkoxy_products,
                             validation::keys.reactants,
                             validation::keys.type,
                             validation::keys.gas_phase };
      auto optional_keys = { validation::keys.name, validation::keys.X, validation::keys.Y, validation::keys.a0, validation::keys.n };

      auto validate = ValidateSchema(object, required_keys, optional_keys);
      errors.insert(errors.end(), validate.begin(), validate.end());
      if (validate.empty())
      {
        auto alkoxy_products = ParseReactantsOrProducts(validation::keys.alkoxy_products, object);
        errors.insert(errors.end(), alkoxy_products.first.begin(), alkoxy_products.first.end());
        auto nitrate_products = ParseReactantsOrProducts(validation::keys.nitrate_products, object);
        errors.insert(errors.end(), nitrate_products.first.begin(), nitrate_products.first.end());
        auto reactants = ParseReactantsOrProducts(validation::keys.reactants, object);
        errors.insert(errors.end(), reactants.first.begin(), reactants.first.end());

        branched.X = object[validation::keys.X].as<double>();
        branched.Y = object[validation::keys.Y].as<double>();
        branched.a0 = object[validation::keys.a0].as<double>();
        branched.n = object[validation::keys.n].as<double>();

        if (object[validation::keys.name])
        {
          branched.name = object[validation::keys.name].as<std::string>();
        }

        std::vector<std::string> requested_species;
        for (const auto& spec : nitrate_products.second)
        {
          requested_species.push_back(spec.species_name);
        }
        for (const auto& spec : alkoxy_products.second)
        {
          requested_species.push_back(spec.species_name);
        }
        for (const auto& spec : reactants.second)
        {
          requested_species.push_back(spec.species_name);
        }

        if (RequiresUnknownSpecies(requested_species, existing_species))
        {
          std::string line = std::to_string(object.Mark().line + 1);
          std::string column = std::to_string(object.Mark().column + 1);
          errors.push_back({ ConfigParseStatus::ReactionRequiresUnknownSpecies, line + ":" + column + ": Reaction requires unknown species" });
        }

        std::string gas_phase = object[validation::keys.gas_phase].as<std::string>();
        auto it = std::find_if(existing_phases.begin(), existing_phases.end(), [&gas_phase](const auto& phase) { return phase.name == gas_phase; });
        if (it == existing_phases.end())
        {
          std::string line = std::to_string(object[validation::keys.gas_phase].Mark().line + 1);
          std::string column = std::to_string(object[validation::keys.gas_phase].Mark().column + 1);
          errors.push_back({ ConfigParseStatus::UnknownPhase, line + ":" + column + ": Unknown phase: " + gas_phase });
        }

        branched.gas_phase = gas_phase;
        branched.nitrate_products = nitrate_products.second;
        branched.alkoxy_products = alkoxy_products.second;
        branched.reactants = reactants.second;
        branched.unknown_properties = GetComments(object);
        reactions.branched.push_back(branched);
      }

      return errors;
    }
  }  // namespace v1
}  // namespace mechanism_configuration
