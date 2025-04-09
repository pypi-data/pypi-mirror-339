import datetime
import os

import neo4j.exceptions
from semantic_main.autotwin_mapper import write_semantic_links
from sha_learning.autotwin_learn import learn_automaton
from skg_main.autotwin_connector import store_automaton, delete_automaton

SAVE_PATH = os.path.dirname(os.path.abspath(__file__)).split('autotwin_autlib')[0] + 'autotwin_autlib'


def start_automata_learning(pov, start, end, schema, version='V4'):
    if 'croma' in schema.lower():
        os.environ['NEO4J_SCHEMA'] = 'croma'
    elif 'pizza' in schema.lower():
        os.environ['NEO4J_SCHEMA'] = 'pizzaLineV' + version[-1]
    elif 'lego' in schema.lower():
        os.environ['NEO4J_SCHEMA'] = 'legoFactory'
    else:
        # FIXME: default value for now
        os.environ['NEO4J_SCHEMA'] = 'croma'

    # 1: Automata Learning experiment.
    try:
        start = int(start)

        try:
            learned_sha = learn_automaton(pov, start_ts=int(start), end_ts=int(end), save_path=SAVE_PATH)
        except neo4j.exceptions.ServiceUnavailable:
            return None, None
        except ValueError:
            print('No events in the specified time frame.')
            return None, None
    except ValueError:
        parsed_start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%SZ")
        parsed_end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%SZ")

        DATE_FORMAT = '{}-{}-{}-{}-{}-{}'
        start_dt = DATE_FORMAT.format(parsed_start.year, parsed_start.month, parsed_start.day,
                                      parsed_start.hour, parsed_start.minute, parsed_start.second)
        end_dt = DATE_FORMAT.format(parsed_end.year, parsed_end.month, parsed_end.day,
                                    parsed_end.hour, parsed_end.minute, parsed_end.second)
        try:
            learned_sha = learn_automaton(pov, start_dt=start_dt, end_dt=end_dt, save_path=SAVE_PATH)
        except neo4j.exceptions.ServiceUnavailable:
            return None, None
        except ValueError:
            print('No events in the specified time frame.')
            return None, None

    # 2: Delete learned automaton from the SKG, if there already exists one with the same name.
    delete_automaton(learned_sha, pov, start, end)

    # 3: Store the learned automaton into the SKG.
    automaton, new_automaton_id = store_automaton(learned_sha, pov, start, end, SAVE_PATH)

    # 4: Create semantic links between learned model and existing SKG nodes.
    write_semantic_links(learned_sha, pov, start, end, SAVE_PATH)

    return learned_sha, new_automaton_id
