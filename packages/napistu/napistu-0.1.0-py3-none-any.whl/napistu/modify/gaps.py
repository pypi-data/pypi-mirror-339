from __future__ import annotations

import copy
import logging

import igraph as ig
import numpy as np
import pandas as pd

from napistu import identifiers
from napistu import sbml_dfs_core
from napistu import sbml_dfs_utils
from napistu import source
from napistu import utils
from napistu.network import net_create

from napistu.constants import SBML_DFS
from napistu.constants import COMPARTMENTS
from napistu.constants import IDENTIFIERS
from napistu.constants import MINI_SBO_FROM_NAME
from napistu.constants import SBOTERM_NAMES
from napistu.constants import SOURCE_SPEC

logger = logging.getLogger(__name__)


def add_transportation_reactions(
    sbml_dfs: sbml_dfs_core.SBML_dfs,
    exchange_compartment: str = COMPARTMENTS["CYTOSOL"],
) -> sbml_dfs_core.SBML_dfs:
    """
    Add Transportation Reactions

    Identifies proteins whose various compartmentalized forms cannot reach one
    another via existing transportation reactions and then adds transportation
    reactions which connect all forms of a protein.

    sbml_dfs: sbml_dfs_core.SBML_dfs
        A mechanistic model containing a set of molecular species which exist
        in multiple compartments and are interconverted by reactions
    exchange_compartment: str
        The name of an exchange compartment matching a c_name from sbml_dfs.compartments

    Returns:

    sbml_df_with_exchange: sbml_dfs_core.SBML_dfs
        The input sbml_dfs with additional transport reactions and compartmentalized species
        (in the exchange compartment) added.

    """

    # validate arguments
    if not any(sbml_dfs.compartments[SBML_DFS.C_NAME] == exchange_compartment):
        raise ValueError(
            f"{exchange_compartment} is not a compartment defined in sbml_dfs.compartments"
        )

    # find species which need transport reactions
    species_needing_transport_rxns = _identify_species_needing_transport_reactions(
        sbml_dfs=sbml_dfs
    )

    sbml_df_with_exchange = update_sbml_df_with_exchange(
        species_needing_transport_rxns=species_needing_transport_rxns,
        sbml_dfs=sbml_dfs,
        exchange_compartment=exchange_compartment,
    )

    return sbml_df_with_exchange


def update_sbml_df_with_exchange(
    species_needing_transport_rxns: np.ndarray,
    sbml_dfs: sbml_dfs_core.SBML_dfs,
    exchange_compartment: str = COMPARTMENTS["CYTOSOL"],
) -> sbml_dfs_core.SBML_dfs:
    """

    Update SBML_dfs With Exchange

    Add transportation reactions between all locations of a set of molecular species by
    including bidirectional exchange reactions through an exchange compartment.

    Parameters:

    species_needing_transport_rxns: np.ndarray
        Vector of molecular species (s_ids) with no or insufficient transportation reactions
    sbml_dfs: sbml_dfs_core.SBML_dfs
        A mechanistic model containing a set of molecular species which exist
        in multiple compartments and are interconverted by reactions
    exchange_compartment: str
        The name of an exchange compartment matching a c_name from sbml_dfs.compartments

    Returns:

    update_sbml_df_with_exchange: sbml_dfs_core.SBML_dfs
        The input sbml_dfs with additional transport reactions and compartmentalized species
        (in the exchange compartment) added.

    """

    exchange_compartment_id = sbml_dfs.compartments[
        sbml_dfs.compartments[SBML_DFS.C_NAME] == exchange_compartment
    ].index.tolist()
    if len(exchange_compartment_id) != 1:
        raise ValueError(
            "The provided exchange compartment matched "
            f"{len(exchange_compartment_id)} compartments - this is unexpected behavior"
        )
    exchange_compartment_id = exchange_compartment_id[0]

    # create a source object with provenance information for the entities that we'll add to the sbml_dfs
    gap_filling_source_obj = source.Source(
        pd.Series(
            {
                SOURCE_SPEC.MODEL: "gap filling",
                SOURCE_SPEC.PATHWAY_ID: "gap_filling",
                SOURCE_SPEC.NAME: "Gap filling to enable transport between all compartments where species is present",
            }
        )
        .to_frame()
        .T
    )

    # initialize an empty identifiers object for gap filled reactions
    gap_filling_id_obj = identifiers.Identifiers([])

    # find species which need exchange reactions but which are not currently present in the exchange compartment
    existing_exchange_cspecies = sbml_dfs.compartmentalized_species[
        sbml_dfs.compartmentalized_species[SBML_DFS.C_ID] == exchange_compartment_id
    ]
    new_exchange_cspecies = set(species_needing_transport_rxns).difference(
        set(existing_exchange_cspecies[SBML_DFS.S_ID].tolist())
    )

    logger.info(
        f"{len(new_exchange_cspecies)} new compartmentalized species must "
        f"be added to the {exchange_compartment} to add protein transportation gap filling"
    )

    # since compartmentalized species are defined by their sid and cid
    # add the defining foreign keys for all new exchange species
    # then we'll add the primary key by autoincrementing existing keys
    new_exchange_cspecies_fks = (
        pd.DataFrame({SBML_DFS.S_ID: list(new_exchange_cspecies)})
        .assign(c_id=exchange_compartment_id)
        .merge(
            sbml_dfs.species[SBML_DFS.S_NAME],
            how="left",
            left_on=SBML_DFS.S_ID,
            right_index=True,
        )
    )
    new_exchange_cspecies_fks[SBML_DFS.SC_NAME] = [
        f"{s_name} [{exchange_compartment}]"
        for s_name in new_exchange_cspecies_fks[SBML_DFS.S_NAME]
    ]
    new_exchange_cspecies_fks = new_exchange_cspecies_fks.drop(SBML_DFS.S_NAME, axis=1)
    new_exchange_cspecies_fks[SBML_DFS.SC_SOURCE] = gap_filling_source_obj

    # update index by incrementing existing keys
    existing_sc_ids = sbml_dfs_utils.id_formatter_inv(
        sbml_dfs.compartmentalized_species.index.tolist()
    )
    # filter np.nan which will be introduced if the key is not the default format
    existing_sc_ids = [x for x in existing_sc_ids if x is not np.nan]
    current_max_sc_id = max(existing_sc_ids)

    new_int_ids = [
        1 + current_max_sc_id + x for x in new_exchange_cspecies_fks.index.tolist()
    ]
    new_exchange_cspecies_fks[SBML_DFS.SC_ID] = sbml_dfs_utils.id_formatter(
        new_int_ids, id_type=SBML_DFS.SC_ID
    )
    new_exchange_cspecies_df = new_exchange_cspecies_fks.set_index(SBML_DFS.SC_ID)

    # add new compartmentalized species to sbml_dfs model
    updated_sbml_dfs = copy.deepcopy(sbml_dfs)
    updated_sbml_dfs.compartmentalized_species = pd.concat(
        [updated_sbml_dfs.compartmentalized_species, new_exchange_cspecies_df]
    )

    # define all new transport reactions as an edgelist

    # pull out all cspecies of species needing transport
    cspecies_needing_transport = (
        updated_sbml_dfs.compartmentalized_species[
            updated_sbml_dfs.compartmentalized_species[SBML_DFS.S_ID].isin(
                species_needing_transport_rxns
            )
        ]
        .reset_index()
        .drop(SBML_DFS.SC_SOURCE, axis=1)
    )

    exchange_cspecies = cspecies_needing_transport[
        cspecies_needing_transport[SBML_DFS.C_ID] == exchange_compartment_id
    ].drop(SBML_DFS.C_ID, axis=1)
    non_exchange_cspecies = cspecies_needing_transport[
        cspecies_needing_transport[SBML_DFS.C_ID] != exchange_compartment_id
    ].drop(SBML_DFS.C_ID, axis=1)

    transport_rxn_edgelist = pd.concat(
        [
            # exchange compartment -> non-exchange compartment
            exchange_cspecies.rename(
                {SBML_DFS.SC_ID: "sc_id_from", SBML_DFS.SC_NAME: "sc_name_from"}, axis=1
            ).merge(
                non_exchange_cspecies.rename(
                    {SBML_DFS.SC_ID: "sc_id_to", SBML_DFS.SC_NAME: "sc_name_to"}, axis=1
                )
            ),
            # non-exchange compartment -> exchange compartment
            non_exchange_cspecies.rename(
                {SBML_DFS.SC_ID: "sc_id_from", SBML_DFS.SC_NAME: "sc_name_from"}, axis=1
            ).merge(
                exchange_cspecies.rename(
                    {SBML_DFS.SC_ID: "sc_id_to", SBML_DFS.SC_NAME: "sc_name_to"}, axis=1
                )
            ),
        ]
    )

    # we should add two reactions for each non-exchange compartment cspecies
    # one transporting from the exchange compartment and one transporting into the
    # exchange compartment
    assert transport_rxn_edgelist.shape[0] == 2 * non_exchange_cspecies.shape[0]

    # the rows in this edgelist correspond to new reactions that we'll add
    # to the model
    transport_rxn_edgelist[SBML_DFS.R_NAME] = [
        f"{x} -> {y} gap-filling transport"
        for x, y in zip(
            transport_rxn_edgelist["sc_name_from"], transport_rxn_edgelist["sc_name_to"]
        )
    ]
    transport_rxn_edgelist = transport_rxn_edgelist.reset_index(drop=True)

    # create new reactions, update index by incrementing existing keys

    existing_r_ids = sbml_dfs_utils.id_formatter_inv(sbml_dfs.reactions.index.tolist())
    # filter np.nan which will be introduced if the key is not the default format
    existing_r_ids = [x for x in existing_r_ids if x is not np.nan]
    current_max_r_id = max(existing_r_ids)

    new_int_ids = [
        1 + current_max_r_id + x for x in transport_rxn_edgelist.index.tolist()
    ]
    transport_rxn_edgelist[SBML_DFS.R_ID] = sbml_dfs_utils.id_formatter(
        new_int_ids, id_type=SBML_DFS.R_ID
    )
    new_reactions = (
        transport_rxn_edgelist[[SBML_DFS.R_ID, SBML_DFS.R_NAME]]
        .set_index(SBML_DFS.R_ID)
        .assign(r_Identifiers=gap_filling_id_obj)
        .assign(r_Source=gap_filling_source_obj)
    )

    logger.info(
        f"{len(new_reactions)} new reactions must "
        f"be added to the {exchange_compartment} to add molecular species transportation reactions"
    )

    # add new reactions
    updated_sbml_dfs.reactions = pd.concat([updated_sbml_dfs.reactions, new_reactions])

    # create new reaction species
    # each reaction adds two reaction species - the from and to compartmentalized species
    new_reaction_species = pd.concat(
        [
            transport_rxn_edgelist[["sc_id_from", SBML_DFS.R_ID]]
            .rename({"sc_id_from": SBML_DFS.SC_ID}, axis=1)
            .assign(stoichiometry=-1)
            # substrate
            .assign(sbo_term=MINI_SBO_FROM_NAME[SBOTERM_NAMES.REACTANT]),
            transport_rxn_edgelist[["sc_id_to", SBML_DFS.R_ID]]
            .rename({"sc_id_to": SBML_DFS.SC_ID}, axis=1)
            .assign(stoichiometry=1)
            # product
            .assign(sbo_term=MINI_SBO_FROM_NAME[SBOTERM_NAMES.PRODUCT]),
        ]
    ).reset_index(drop=True)

    existing_rsc_ids = sbml_dfs_utils.id_formatter_inv(
        sbml_dfs.reaction_species.index.tolist()
    )
    # filter np.nan which will be introduced if the key is not the default format
    existing_rsc_ids = [x for x in existing_rsc_ids if x is not np.nan]
    current_max_rsc_id = max(existing_rsc_ids)

    new_int_ids = [
        1 + current_max_rsc_id + x for x in new_reaction_species.index.tolist()
    ]
    new_reaction_species[SBML_DFS.RSC_ID] = sbml_dfs_utils.id_formatter(
        new_int_ids, id_type=SBML_DFS.RSC_ID
    )
    new_reaction_species = new_reaction_species.set_index(SBML_DFS.RSC_ID)

    updated_sbml_dfs.reaction_species = pd.concat(
        [updated_sbml_dfs.reaction_species, new_reaction_species]
    )

    updated_sbml_dfs = sbml_dfs_utils.check_entity_data_index_matching(
        updated_sbml_dfs, SBML_DFS.REACTIONS
    )

    updated_sbml_dfs.validate()

    return updated_sbml_dfs


def _identify_species_needing_transport_reactions(
    sbml_dfs: sbml_dfs_core.SBML_dfs,
) -> np.ndarray:
    """
    Identify Molecular Species Needing Transport Reactions

    Determine whether each molecular species has sufficient transport reactions
    so all of the compartments where it exists are connected.

    Parameters:

    sbml_dfs: sbml_dfs_core.SBML_dfs
        A mechanistic model containing a set of molecular species which exist
        in multiple compartments and are interconverted by reactions

    Returns:

    species_needing_transport_rxns: np.ndarray
        Vector of molecular species (s_ids) with no or insufficient transportation reactions

    """

    # ensure that all genic reaction species can be produced and transported to each
    # compartment where they should exist.
    # we should be able to follow a directed path from a synthesized protein
    # (by default in the nucleoplasm) possibly through multiple complexes and to every
    # other compartmentalized species
    #
    # if a path does not exist then we can create one assuming a path which
    # look like nucleoplasm > cytoplasm > other compartment

    species_ids = sbml_dfs.get_identifiers(SBML_DFS.SPECIES)

    # identify all pure protein species - all of there cspecies should be connected
    pure_protein_species = (
        species_ids.query("ontology == 'uniprot' and bqb in ('BQB_IS')")[
            [SBML_DFS.S_ID, IDENTIFIERS.IDENTIFIER]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # identify all species containing protein - these are the species which can be used
    # as links for evaluating whether cspecies are connected

    partial_protein_cspecies = (
        species_ids.query(
            "ontology == 'uniprot' and bqb in ('BQB_IS', 'BQB_HAS_PART')"
        )[[SBML_DFS.S_ID, IDENTIFIERS.IDENTIFIER]]
        .drop_duplicates()
        .merge(
            sbml_dfs.compartmentalized_species.reset_index()[
                [SBML_DFS.SC_ID, SBML_DFS.S_ID, SBML_DFS.C_ID]
            ]
        )
        .set_index(IDENTIFIERS.IDENTIFIER)
        .sort_index()
    )

    # create a directed graph
    directed_graph = net_create.create_cpr_graph(
        sbml_dfs, directed=True, graph_type="bipartite"
    )

    # consider each s_id and protein separately
    # if one s_id matches multiple proteins then
    # ideally they should have the same paths but this
    # may not be true if they are part of different protein complexes
    #
    # as a result we can identify compartmentalized species and transport reactions
    # that must exist to support each s_id - identifier pair and then
    # take the union of new entities over proteins matching a given s_id

    cspecies_path_tuple_dict = dict()
    for row in pure_protein_species.itertuples():
        s_id = row.s_id
        uniprot = row.identifier

        comp_specs = sbml_dfs.compartmentalized_species[
            sbml_dfs.compartmentalized_species[SBML_DFS.S_ID] == s_id
        ]

        if comp_specs.shape[0] == 1:
            # the species only exists in one compartment so no transport reactions are needed
            cspecies_path_tuple_dict[(s_id, uniprot)] = {"type": "single-compartment"}
        else:
            # find whether there are valid transportation routes between all a proteins' compartments
            existing_cspecies_paths = _find_existing_inter_cspecies_paths(
                comp_specs, uniprot, directed_graph, partial_protein_cspecies
            )
            if existing_cspecies_paths is not None:
                cspecies_path_tuple_dict[(s_id, uniprot)] = (
                    _eval_existing_inter_cspecies_paths(
                        comp_specs, existing_cspecies_paths
                    )
                )
            else:
                cspecies_path_tuple_dict[(s_id, uniprot)] = {
                    "type": "unreachable cspecies - no transport reactions"
                }

    # reformat dict as a pd.DataFrame
    species_transport_status_dict_list = list()
    for k, v in cspecies_path_tuple_dict.items():
        entry = {SBML_DFS.S_ID: k[0], IDENTIFIERS.IDENTIFIER: k[1], **v}

        species_transport_status_dict_list.append(entry)

    species_transport_status_df = pd.DataFrame(species_transport_status_dict_list)

    # optional logging
    # logger.info(_log_protein_transport_gapfilling(species_transport_status_df))

    # define proteins which whose compartmentalized forms are not connected
    proteins_needing_transport_rxns = species_transport_status_df[
        species_transport_status_df["type"].isin(
            [
                "unreachable cspecies - no transport reactions",
                "unreachable cspecies - inadequate transport reactions",
            ]
        )
    ]

    # convert from proteins needing gap filling to species that they match
    # multiple proteins may match a single species so if any of them
    # need gap filling then gap filling will be added for the whole species
    species_needing_transport_rxns = proteins_needing_transport_rxns[
        SBML_DFS.S_ID
    ].unique()

    return species_needing_transport_rxns


def _eval_existing_inter_cspecies_paths(
    comp_specs: pd.DataFrame, existing_cspecies_paths: pd.DataFrame
) -> dict:
    """
    Evaluate Existing Inter Compartmentalized Species Paths

    Determine whether paths between compartments found in
    _find_existing_inter_cspecies_paths()
        cover all of the compartments where the protein exists.

    Parameters:

    comp_specs: pd.DataFrame
        Compartmentalized species for a single s_id
    existing_cspecies_paths: pd.DataFrame
        An edgelist of a from and to compartmentalized species
        and a label of the path connecting them.

    Returns:

    species_tranpsort_status: dict
        type: the status category the species falls in
        ?msg: an optional message describing the type

    """

    # If the largest connected component includes all compartmentalized species
    # then we can assume that the transportation reactions which exist are adequate. Note that
    # because the subgraph is directed its topology may still be kind of funky.

    # find the largest connected component
    largest_connected_component = (
        ig.Graph.TupleList(
            existing_cspecies_paths.itertuples(index=False), directed=False
        )
        .clusters()
        .giant()
    )
    largest_connected_component_vertices = [
        v["name"] for v in largest_connected_component.vs
    ]

    if not isinstance(largest_connected_component_vertices, list):
        raise TypeError("largest_connected_component must be a list")

    missing_cspecies = set(comp_specs.index.tolist()).difference(
        set(largest_connected_component_vertices)
    )

    existing_trans_msg = " & ".join(existing_cspecies_paths["paths_str"].tolist())
    if len(missing_cspecies) != 0:
        msg = f"{', '.join(comp_specs['sc_name'][missing_cspecies].tolist())} "  # type: ignore
        "compartmentalized species were not part of transport reactions though "
        f"some transport paths could be found {existing_trans_msg}. Bidirectional "
        "transport reactions with cytoplasm will be added for this species in "
        "all other compartments"
        return {
            "type": "unreachable cspecies - inadequate transport reactions",
            "msg": msg,
        }

    else:
        msg = f"transportation paths between compartmentalized species already exist {existing_trans_msg}"
        return {"type": "valid transportation paths", "msg": msg}


def _find_existing_inter_cspecies_paths(
    comp_specs: pd.DataFrame,
    uniprot_id: str,
    directed_graph: ig.Graph,
    partial_protein_cspecies: pd.DataFrame,
) -> pd.DataFrame | None:
    """
    Find Existing Inter Compartmentalized Species Paths

    Determine which compartments a protein exists in can be reached from one another by
        traversing a directed graph of reactions and molecular species including the protein
        (i.e., paths can involve complexes of the protein of interest).

    Parameters:

    comp_specs: pd.DataFrame
        Compartmentalized species for a single s_id
    uniprot_id: str
        The Uniprot ID for the protein of interest
    directed_graph: ig.Graph
        An igraph version of the sbml_dfs model
    partial_protein_cspecies: pd.DataFrame
        A table of proteins included in each species ID (this includes BQB_HAS_PART
        qualifiers in addition to the BQB_IS qualifiers which generally define
        distinct species

    Returns:

    existing_cspecies_paths: pd.DataFrame or None
        An edgelist of a from and to compartmentalized species and a label of the path
        connecting them.

    """

    reaction_vertices = np.where(
        [x == "reaction" for x in directed_graph.vs["node_type"]]
    )[0]

    # find all species which include the protein of interest
    valid_links = set(partial_protein_cspecies.loc[uniprot_id][SBML_DFS.SC_ID].tolist())

    # define a subgraph which only uses reactions & species which include the protein of interest
    protein_match_vec = [x in valid_links for x in directed_graph.vs["name"]]
    protein_vertices = np.where(protein_match_vec)[0]
    combined_vertices = np.concatenate((reaction_vertices, protein_vertices), axis=None)

    proteinaceous_subgraph = directed_graph.subgraph(vertices=combined_vertices)

    # find paths along subgraph

    paths_df_dict = dict()
    for a_cspecies in comp_specs.index.tolist():
        to_cspecies = list(set(comp_specs.index.tolist()).difference({a_cspecies}))

        # find a path from a_cspecies to each to_cspecies
        paths = proteinaceous_subgraph.get_shortest_paths(
            v=a_cspecies, to=to_cspecies, output="vpath"
        )

        # create a tabular summary of possible paths (whether or not a valid path was found)
        paths_df = pd.DataFrame(
            {"from": [a_cspecies] * len(to_cspecies), "to": to_cspecies, "paths": paths}
        )

        # filter to valid paths
        paths_df = paths_df.iloc[np.where([p != [] for p in paths_df["paths"]])[0]]
        paths_df["paths_str"] = [
            " -> ".join([proteinaceous_subgraph.vs[x]["node_name"] for x in p])
            for p in paths_df["paths"]
        ]
        paths_df = paths_df.drop("paths", axis=1)

        paths_df_dict[a_cspecies] = paths_df

    existing_cspecies_paths = pd.concat(paths_df_dict.values())

    if existing_cspecies_paths.shape[0] == 0:
        return None
    else:
        return existing_cspecies_paths


def _log_protein_transport_gapfilling(
    species_transport_status_df: pd.DataFrame,
) -> None:
    print(
        utils.style_df(
            species_transport_status_df.value_counts("type").to_frame().reset_index(),
            headers=["Transport Category", "# of Entries"],
            hide_index=True,
        )
    )

    transport_messages_fails = species_transport_status_df[
        species_transport_status_df["type"].isin(
            ["unreachable cspecies - inadequate transport reactions"]
        )
    ]
    if transport_messages_fails.shape[0] > 0:
        print(
            f"Example messages for {transport_messages_fails.shape[0]} species with "
            "some transportation reactions but where not all compartments can be reached\n"
        )

        n_messages = min(5, transport_messages_fails.shape[0])
        transport_message_df = transport_messages_fails.sample(n_messages)

        print("\n\n".join(transport_message_df["msg"].tolist()))

    transport_messages_successes = species_transport_status_df[
        species_transport_status_df["type"].isin(["valid transportation paths"])
    ]
    if transport_messages_successes.shape[0] > 0:
        print(
            "---------------------\nExample messages for "
            f"{transport_messages_successes.shape[0]} species where existing transportation "
            "reactions are sufficient and no gap filling will be applied\n"
        )

        n_messages = min(5, transport_messages_successes.shape[0])
        transport_message_df = transport_messages_successes.sample(n_messages)

        print("\n\n".join(transport_message_df["msg"].tolist()))

    return None
