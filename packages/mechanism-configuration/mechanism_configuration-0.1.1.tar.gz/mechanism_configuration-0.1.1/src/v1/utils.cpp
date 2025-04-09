#include <mechanism_configuration/v1/parser_types.hpp>
#include <mechanism_configuration/v1/utils.hpp>
#include <mechanism_configuration/v1/validation.hpp>
#include <mechanism_configuration/validate_schema.hpp>

namespace mechanism_configuration
{
  namespace v1
  {
    std::unordered_map<std::string, std::string> GetComments(const YAML::Node& object)
    {
      std::unordered_map<std::string, std::string> unknown_properties;
      const std::string comment_start = "__";

      for (const auto& key : object)
      {
        std::string key_str = key.first.as<std::string>();

        // Check if the key starts with the comment prefix
        if (key_str.compare(0, comment_start.size(), comment_start) == 0)
        {
          // Check if the value is a YAML node
          if (key.second.IsScalar())
          {
            unknown_properties[key_str] = key.second.as<std::string>();
          }
          else
          {
            std::stringstream ss;
            ss << key.second;
            unknown_properties[key_str] = ss.str();
          }
        }
      }

      // Return the map of extracted comments
      return unknown_properties;
    }

    std::pair<Errors, std::vector<types::Phase>> ParsePhases(const YAML::Node& objects, const std::vector<types::Species> existing_species)
    {
      Errors errors;
      ConfigParseStatus status = ConfigParseStatus::Success;
      std::vector<types::Phase> all_phases;
      const std::vector<std::string> phase_required_keys = { validation::keys.name, validation::keys.species };
      const std::vector<std::string> phase_optional_keys = {};

      for (const auto& object : objects)
      {
        types::Phase phase;
        auto validate = ValidateSchema(object, phase_required_keys, phase_optional_keys);
        errors.insert(errors.end(), validate.begin(), validate.end());
        if (validate.empty())
        {
          std::string name = object[validation::keys.name].as<std::string>();

          std::vector<std::string> species{};
          for (const auto& spec : object[validation::keys.species])
          {
            species.push_back(spec.as<std::string>());
          }

          phase.name = name;
          phase.species = species;
          phase.unknown_properties = GetComments(object);

          if (RequiresUnknownSpecies(species, existing_species))
          {
            errors.push_back({ ConfigParseStatus::PhaseRequiresUnknownSpecies, "Phase requires unknown species." });
          }
          else
          {
            all_phases.push_back(phase);
          }
        }
      }

      if (!ContainsUniqueObjectsByName<types::Phase>(all_phases))
      {
        errors.push_back({ ConfigParseStatus::DuplicatePhasesDetected, "Duplicate phases detected." });
      }

      return { errors, all_phases };
    }

    std::pair<Errors, types::ReactionComponent> ParseReactionComponent(const YAML::Node& object)
    {
      Errors errors;
      ConfigParseStatus status = ConfigParseStatus::Success;
      types::ReactionComponent component;
      const std::vector<std::string> reaction_component_required_keys = { validation::keys.species_name };
      const std::vector<std::string> reaction_component_optional_keys = { validation::keys.coefficient };

      auto validate = ValidateSchema(object, reaction_component_required_keys, reaction_component_optional_keys);
      errors.insert(errors.end(), validate.begin(), validate.end());
      if (validate.empty())
        if (status == ConfigParseStatus::Success)
        {
          std::string species_name = object[validation::keys.species_name].as<std::string>();
          double coefficient = 1;
          if (object[validation::keys.coefficient])
          {
            coefficient = object[validation::keys.coefficient].as<double>();
          }

          component.species_name = species_name;
          component.coefficient = coefficient;
          component.unknown_properties = GetComments(object);
        }

      return { errors, component };
    }

    std::pair<Errors, std::vector<types::ReactionComponent>> ParseReactantsOrProducts(const std::string& key, const YAML::Node& object)
    {
      Errors errors;
      std::vector<types::ReactionComponent> result{};
      for (const auto& product : object[key])
      {
        auto component_parse = ParseReactionComponent(product);
        errors.insert(errors.end(), component_parse.first.begin(), component_parse.first.end());
        if (component_parse.first.empty())
        {
          result.push_back(component_parse.second);
        }
      }
      return { errors, result };
    }

    std::pair<Errors, types::Reactions>
    ParseReactions(const YAML::Node& objects, const std::vector<types::Species>& existing_species, const std::vector<types::Phase>& existing_phases)
    {
      Errors errors;
      types::Reactions reactions;

      std::map<std::string, std::unique_ptr<IReactionParser>> parsers;
      parsers[validation::keys.Arrhenius_key] = std::make_unique<ArrheniusParser>();
      parsers[validation::keys.HenrysLaw_key] = std::make_unique<HenrysLawParser>();
      parsers[validation::keys.WetDeposition_key] = std::make_unique<WetDepositionParser>();
      parsers[validation::keys.AqueousPhaseEquilibrium_key] = std::make_unique<AqueousEquilibriumParser>();
      parsers[validation::keys.SimpolPhaseTransfer_key] = std::make_unique<SimpolPhaseTransferParser>();
      parsers[validation::keys.FirstOrderLoss_key] = std::make_unique<FirstOrderLossParser>();
      parsers[validation::keys.Emission_key] = std::make_unique<EmissionParser>();
      parsers[validation::keys.CondensedPhasePhotolysis_key] = std::make_unique<CondensedPhasePhotolysisParser>();
      parsers[validation::keys.Photolysis_key] = std::make_unique<PhotolysisParser>();
      parsers[validation::keys.Surface_key] = std::make_unique<SurfaceParser>();
      parsers[validation::keys.Tunneling_key] = std::make_unique<TunnelingParser>();
      parsers[validation::keys.Branched_key] = std::make_unique<BranchedParser>();
      parsers[validation::keys.Troe_key] = std::make_unique<TroeParser>();
      parsers[validation::keys.CondensedPhaseArrhenius_key] = std::make_unique<CondensedPhaseArrheniusParser>();

      for (const auto& object : objects)
      {
        std::string type = object[validation::keys.type].as<std::string>();
        auto it = parsers.find(type);
        if (it != parsers.end())
        {
          auto parse_errors = it->second->parse(object, existing_species, existing_phases, reactions);
          errors.insert(errors.end(), parse_errors.begin(), parse_errors.end());
        }
        else
        {
          std::string line = std::to_string(object[validation::keys.type].Mark().line + 1);
          std::string column = std::to_string(object[validation::keys.type].Mark().column + 1);
          errors.push_back({ ConfigParseStatus::UnknownType, "Unknown type: " + type + " at line " + line + " column " + column });
        }
      }

      return { errors, reactions };
    }
  }  // namespace v1
}  // namespace mechanism_configuration
